import json
import requests
import socket
import base64
import urllib
import os
import urllib.request
i = 1

# GET MANIFEST OR REFERENCE
def getInformation(base,query):
    print(base)
    print(query)
    print(base+urllib.parse.quote(query,safe='')) 
    r = requests.get(base+query,headers = {'Content-Type': 'application/json+fhir'})
    try:
      result = r.json()
    except json.decoder.JSONDecodeError:
      result = "GET Error"
    return str(r.status_code) + '\n' + str(result)

# GET BINARY BY RESOURCE ID
def getContent(content_query, resourceId ):
    url = content_query + resourceId
    response = urllib.request.urlretrieve(url,resourceId)
    print(response[1])
    print(response[1]['Content-Type'])
    os.rename(resourceId, resourceId+ response[1]['Content-Type'].split('/')[1])


#POST Bundle
def postBundle(address,filename):
    f = open(filename,'rb')
    file = f.read()
    encodedFile = base64.b64encode(file)
    jsonFile = open('jsonFile.json','r')
    jsonFormat = json.load(jsonFile)
    for i in range(len(jsonFormat['entry'])):
        if jsonFormat['entry'][i]['resource']['resourceType'] == 'Binary':
            jsonFormat['entry'][i]['resource']['content'] = str(encodedFile)[2:-1]
            break
    print(jsonFormat)
    f.close()

    r = requests.post(address,headers = {'Content-Type': 'application/json+fhir'},json = jsonFormat)#address, json = a)#"  #
    print(r.status_code)
    print(r.text)

    try:
      result = "Post Success\n" 
    except :
      result = "Post Error"
    return result

# Download the file from `url` and save it locally under `file_name`:
def post(address,jsonFormatString):
    print(address + " " + jsonFormatString)
    r = requests.post(address, json = json.loads(jsonFormatString))
    print(r.json())
    try:
      result = "Post Success\n"+json.dumps(r.json())
    except :
      result = "Post Error"
    return result


#SOCKET
def transferFile(file,addr):
    r = requests.post(addr)
    print(file.name.split('/')[-1])
    print(addr)
    s = socket.socket()
    s.connect(('127.0.0.1',5004))
    try:
      f=open ('clientFolder/'+file.name.split('/')[-1], "rb")
    except IOError:
      print ("Could not open file!!")
    print('start transfering')
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
        print('sending')
    s.close()
    f.close()

def retrieveFile(addr):
    global i
    i = i+1
    r = requests.get(addr)
    s = socket.socket()
    s.connect(('127.0.0.1',5004))
    try:
      filename,extension = addr.split('/')[-1].split('.')
      print(addr)
      print(filename+'.'+extension)
      f=open ('clientFolder/'+filename+str(i)+'.'+extension, "wb")
    except IOError:
      print ("Could not open file!!")
    print('start receiving')
    l = s.recv(1024)
    statusIteration = 0
    while (l):
        f.write(l)
        l = s.recv(1024)
        print('receiving'+str(statusIteration))
    s.close()
    f.close()