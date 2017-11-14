import os

from flask import Flask, jsonify, abort, request, send_file
import socket
import json
import base64
import uuid
import glob
from threading import Thread
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_declarative import Base, Manifest, Reference, Content, Resource
import db_transaction
engine = create_engine('sqlite:///mhd_database.db')
Base.metadata.bind = engine
DBSession = sessionmaker()
DBSession.bind = engine

############################################PRACTICE JSON############################################
app = Flask(__name__)
session = DBSession()
#PRACTICE JSON JSON Format
patientList =[{
  "Patient" : {
    "patientId" : 1,
    "patientName" : "Hyeongseok Jeon",
    "administrativeGenderCode" : "M",
    "birthTime" : "19870606"
  }
}]

#GET Action
@app.route('/hojae/<int:patientId>',methods=['GET'])
def getPatient(patientId):
    print(patientId)
    patient = [patient for patient in patientList if patientId == patient['Patient']['patientId']]
    if len(patient) == 0:
        print("No member in list")
        abort(404)
    return jsonify({'patient': patient[0]})

#POST Action
@app.route('/hojae/',methods=['POST'])
def postPatient():
    patient = {
    "Patient" : {
        "patientId" : patientList[-1]['Patient']['patientId']+1,
        "patientName" : request.json['Patient']['patientName'],
        "administrativeGenderCode" : request.json['Patient']['administrativeGenderCode'],
        "birthTime" : request.json['Patient']['birthTime']
         }
    }
    patientList.append(patient)
    return jsonify({'Patient':patient}),201

#POST BUNDLE DECODE HANDLING
def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.decodestring(data)


############################################POST BUNDLE############################################
@app.route('/REST/Bundle',methods=['POST'])
def Bundle():
    #json validation
    bundleJson = isJson(request.data.decode())
    if bundleJson == False:
        return 'json format invalid', 300
    print(request.headers.get('content-type'))
    #binary = binary[1:] # detach the first character 'b' and the binary string will be decoded based on 64

    #Validation
    PatientResourceId = None
    for i in range(len(bundleJson['entry'])):
        if bundleJson['entry'][i]['resource']['resourceType'] == 'DocumentManifest':
            if PatientResourceId == None:
                PatientResourceId = bundleJson['entry'][i]['resource']['subject']['reference'].split('/')[1]
            elif(PatientResourceId != bundleJson['entry'][i]['resource']['subject']['reference'].split('/')[1]):
                return 'Bundle has inconsistent patient resource id', 422
            if db_transaction.isValidPatientResourceId(bundleJson['entry'][i]['resource']['subject']['reference'].split('/')[1]) == False:
                return 'invalid patient resource id', 422
        elif bundleJson['entry'][i]['resource']['resourceType'] == 'DocumentReference':

            if PatientResourceId == None:
                PatientResourceId = bundleJson['entry'][i]['resource']['subject']['reference'].split('/')[1]
            elif(PatientResourceId != bundleJson['entry'][i]['resource']['subject']['reference'].split('/')[1]):
                return 'Bundle has inconsistent patient resource id', 422
            if db_transaction.isValidPatientResourceId(bundleJson['entry'][i]['resource']['subject']['reference'].split('/')[1]) == False:
                return 'invalid patient resource id', 422

        elif bundleJson['entry'][i]['resource']['resourceType'] == 'Binary':
            if request.headers.get('content-type') != 'application/xml+fhir' and request.headers.get('content-type') != 'application/json+fhir':
                return 'invalid content-type', 422
    manifestUrl = str(uuid.uuid4())
    referenceUrl = str(uuid.uuid4())
    contentUrl = str(uuid.uuid4())
    for i in range(len(bundleJson['entry'])):
        print(i)
        if bundleJson['entry'][i]['resource']['resourceType'] == 'DocumentManifest':
            print('asdxf')
            print(bundleJson['entry'][i]['request'])
            db_transaction.insertManifest(bundleJson['entry'][i]['resource']['resourceType'],
                                          manifestUrl,
                                          bundleJson['entry'][i]['resource']['subject'],
                                          bundleJson['entry'][i]['resource']['recipient'],
                                          bundleJson['entry'][i]['resource']['type'],
                                          bundleJson['entry'][i]['resource']['author'],
                                          bundleJson['entry'][i]['resource']['identifier'],
                                          bundleJson['entry'][i]['resource']['created'],
                                          bundleJson['entry'][i]['resource']['status'],
                                          bundleJson['entry'][i]['resource']['description'],
                                          referenceUrl,
                                          bundleJson['entry'][i]['request'])
            print(i)
        elif bundleJson['entry'][i]['resource']['resourceType'] == 'DocumentReference':

            db_transaction.insertReference(bundleJson['entry'][i]['resource']['resourceType'],
                                           referenceUrl,
                                           bundleJson['entry'][i]['resource']['subject'],
                                           bundleJson['entry'][i]['resource']['type'],
                                           bundleJson['entry'][i]['resource']['author'],
                                           bundleJson['entry'][i]['resource']['custodian'],
                                           bundleJson['entry'][i]['resource']['authenticator'],
                                           bundleJson['entry'][i]['resource']['masterIdentifier'],
                                           bundleJson['entry'][i]['resource']['indexed'],
                                           bundleJson['entry'][i]['resource']['created'],
                                           bundleJson['entry'][i]['resource']['status'],
                                           bundleJson['entry'][i]['resource']['description'],
                                           bundleJson['entry'][i]['resource']['securityLabel'],
                                           bundleJson['entry'][i]['resource']['content'],
                                           bundleJson['entry'][i]['request'],
                                           contentUrl
                                           )
            print(i)
        elif bundleJson['entry'][i]['resource']['resourceType'] == 'Binary':
            print(bundleJson['entry'][i]['resource']['resourceType'])
            binary = bundleJson['entry'][i]['resource']['content']
            if request.headers.get('content-type') == 'application/xml+fhir':
                return 'xml format', 300
            elif request.headers.get('content-type') == 'application/json+fhir':
                storeFileFormatted(contentUrl,
                                   bundleJson['entry'][i]['resource']['contentType'],
                                   binary)
            db_transaction.insertContent(bundleJson['entry'][i]['resource']['resourceType'],
                                         contentUrl,
                                         bundleJson['entry'][i]['resource']['contentType'],
                                         bundleJson['entry'][i]['resource']['content'],
                                         bundleJson['entry'][i]['request'])

            print(i)
        else:
            return "No available resourceType", 400
            break
    for i in range(len(bundleJson['entry'])):
        print(i)
        if bundleJson['entry'][i]['resource']['resourceType'] == 'DocumentManifest':
            bundleJson['entry'][i]['id'] = bundleJson['entry'][i].pop('fullUrl')
            bundleJson['entry'][i]['id'] = manifestUrl
        elif bundleJson['entry'][i]['resource']['resourceType'] == 'DocumentReference':
            bundleJson['entry'][i]['id'] = bundleJson['entry'][i].pop('fullUrl')
            bundleJson['entry'][i]['id'] = referenceUrl
    return json.dumps(bundleJson) ,200

#########################################STORE FILES#############################################################
def storeFileFormatted(filename,format, binary):
    if format == 'text/xml':
        providedDocument = open(filename+'.xml', mode='wb')
        providedDocument.write((base64.b64decode(binary)))
        providedDocument.close()
    elif format == 'application/pdf':
        providedDocument = open(filename+'.pdf', mode='wb')
        providedDocument.write((base64.b64decode(binary)))
        providedDocument.close()
    elif format == 'image/jpeg':
        print("dd")
        providedDocument = open(filename+'.jpeg', mode='wb')
        providedDocument.write((base64.b64decode(binary)))
        providedDocument.close()
        print("dasd")
    else :
        return 'No parsable file format',300
# JSON VALIDATION
def isJson(text):
    try:
        return json.loads(text)
    except ValueError as e:
        return False

############################################DOCUMENT MANIFEST############################################

@app.route('/REST/DocumentManifest/<resource_id>',methods=['GET'])
def DocumentManifest_with_resource(resource_id):
    print(resource_id)
    if resource_id != None:
        id = resource_id
    print(id)

    result = db_transaction.selectManifest_by_resource_id(resource_id)
    if result == None:
        return "No result of manifest resource id", 422
    else:
        print(result)
        return json.dumps(result), 200



@app.route('/REST/DocumentManifest/',methods=['GET'])
def DocumentManifest():
    id = request.args.get('_id')
    patient = request.args.get('patient')
    print(id)
    print(patient)
    #Error Check corresponding to query
    if id == None and patient == None:
        result = db_transaction.selectManifest_All()
        if result == None:
            return "No result of manifest resource id", 422
        else:
            print(result)
            return json.dumps(result), 200
    elif id != None:
        result = db_transaction.selectManifest_by_resource_id(id)
        if result == None:
            return "No result of manifest resource id", 422
        else:
            print(result)
            return json.dumps(result), 200
    else:
        result = db_transaction.selectManifest_by_patient_resource_id(patient)
        if result == None:
            return "No result of manifest resource patient id", 422
        else:
            return json.dumps(result), 200


############################################DOCUMENT REFERENCE############################################
@app.route('/REST/DocumentReference/',methods=['GET'])
def DocumentReference():
    id = request.args.get('_id')
    patient = request.args.get('patient')
    print(id)
    print(patient)
    #Error Check corresponding to query
    if id == None and patient == None:
        result = db_transaction.selectReference_All()
        if result == None:
            return "No result of reference resource id", 422
        else:
            print(result)
            return json.dumps(result), 200
    elif id != None:
        result = db_transaction.selectReference_by_resource_id(id)
        if result == None:
            return "No result of reference resource id", 422
        else:
            print(result)
            return json.dumps(result), 200
    else:
        result = db_transaction.selectReference_by_patient_resource_id(patient)
        if result == None:
            return "No result of reference resource patient id", 422
        else:
            return json.dumps(result), 200

@app.route('/REST/DocumentReference/<resource_id>',methods=['GET'])
def DocumentReference_with_resource(resource_id):
    print(resource_id)
    #Error Check corresponding to query
    if resource_id != None:
        id = resource_id
    print(id)
    result = db_transaction.selectReference_by_resource_id(resource_id)
    if result == None:
        return "No result of reference resource id", 422
    else:
        print(result)
        return json.dumps(result), 200

############################################FOR TESTING############################################
@app.route('/RetrieveManifest')
def selectManifests():
    return db_transaction.selectManifest()

@app.route('/RetrieveReference')
def selectReferences():
    return db_transaction.selectReference()

@app.route('/RetrieveContent')
def selectContents():
    return db_transaction.selectContent()


@app.route('/hojae/upload/<filename>',methods=['POST'])
def postFile(filename):
    print('tread created') 
    thread= Thread(target = uploadFile,args=(filename,))
    thread.start()
    return 'OK'
def uploadFile(filename):

    s = socket.socket()
    s .setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1)
    s.bind(('127.0.0.1',5004))
    s.listen(1)  
    sc, address = s.accept()
    global i
    filename, extension = filename.split('.')
    
    script_dir = os.path.dirname(__file__)
    server_folder = 'serverFolder/'  
    f = open(server_folder+filename+str(i)+'.'+extension,'wb') #open in binary
    
    i=i+1 
    l = sc.recv(1024)
    while (l):
        f.write(l)
        l = sc.recv(1024)
        print(str(i)+'receiving')
    print('socket terminated')
    f.close()
    sc.close()
    s.close()
@app.route('/hojae/retrieve/<filename>',methods=['GET'])
def getFile(filename):
    print('tread created')  
    thread= Thread(target = retrieveFile,args=(filename,))
    thread.start() 
    return 'OK'

def retrieveFile(filename):
    print(filename)
    s = socket.socket()
    s .setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR) | 1)
    s.bind(('127.0.0.1',5004))
    s.listen(1)  
    sc, address = s.accept() 
 
    server_folder = 'serverFolder/' 
    f = open(server_folder+filename,'rb') #open in binary 

    l = f.read(1024)
    statusIteration = 0
    while (l):
        sc.send(l)
        l = f.read(1024)
        print('sending'+str(statusIteration))
    print('socket terminated')
    f.close()
    sc.close()
    s.close()  

# retrieve Document
@app.route('/REST/Binary/<resource>',methods=['GET'])
def retrieveContent(resource):
    for infile in glob.glob(resource+'.*'):
        if infile.split('.')[1] == 'xml' :
            result = send_file(infile, mimetype='application/xml')
        elif infile.split('.')[1] == 'pdf':
            result = send_file(infile, mimetype='application/pdf')
        elif infile.split('.')[1] == 'jpeg':
            result = send_file(infile, mimetype='image/jpeg')

    return result


#get Patient Manifest with json format
#GET Action
@app.route('/DocumentManifest/<type>/<int:patientId>?_format=<format>',methods=['GET'])
def getManifestDocument(type,patientId,format):
    cwd = os.getcwd()  # Get the current working directory (cwd)
    files = os.listdir(cwd+'/DocumentManifest/'+type)  # Get all the files in that directory
    print("Files in '%s': %s" % (cwd, files))
    if format == 'json':
        manifestFile = open("DocumentManifest/"+type+"/Manifest.json")
        jsonText = json.loads(manifestFile.read())
        for i in range(len(jsonText['entry'])):
            foundPatientId = None
            if jsonText['entry'][i]['id'] == patientId:
                print(str(jsonText['entry'][i]))
                foundPatientId = i
                break
    elif format == 'xml':
        manifestFile = open("DocumentManifest/"+type+"/Manifest.json")
    else:
        return jsonify({"Erorr":{"Format Error":"403"}}),403
    return jsonify({"Patient":jsonText['entry'][foundPatientId]}) ,200


#Main
if __name__ == '__main__':

    app.run(host='0.0.0.0',port=8080,debug=True)

#http://192.168.0.6:8084/REST/Bundle
#http://192.168.0.9:8080/RestServer/kjh/ProvideDocument
#http://192.168.0.5:8080/MHD/Bundle