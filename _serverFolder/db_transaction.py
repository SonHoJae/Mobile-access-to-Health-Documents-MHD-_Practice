from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_declarative import Base, Manifest, Reference, Content, Resource, PatientResource
engine = create_engine('sqlite:///mhd_database.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance

DBSession = sessionmaker(bind=engine)
Base.metadata.bind = engine
session = DBSession()

''''''''''''''''''''''''''''''''''''''''''''''''''''INSERT'''''''''''''''''''''''''''''''''''''''''''''''''''
#Insert PatientResource
def insertPatientResource(resourceType, system, value, family, given, gender, birthDate):

    new_patient_resource = PatientResource(resourceType = str(resourceType),
                                           system = str(system),
                                           value = str(value),
                                           family = str(family),
                                           given = str(given),
                                           gender = str(gender),
                                           birthDate = str(birthDate))
    print("id "+str(value)+" added successfully")
    session.add(new_patient_resource)
    session.commit()
#insertPatientResource("Patient","urn:oid:1.2.410.19376.3","201","Watson","John","M","1933/08/22")
#insertPatientResource("Patient","urn:oid:1.2.410.19376.3","202","Park","Peter","M","1940/03/11")
#insertPatientResource("Patient","urn:oid:1.2.410.19376.3","203","Watson","John","M","1954/07/02")

#Insert Manifest
def insertManifest(resourceType = None, fullUrl = None, subject = None, recipient = None, type = None, author = None,
                   identifier = None, created = None, status = None, description = None, content = None, request = None):
    print(str(content))
    #print(content[0]['pReference']['reference'])
    print('testtest')
    print(str(recipient[0]['reference']))
    new_manifest_resource = Resource(
                            resourceType=str(resourceType),#'DocumentManifest',
                            fullUrl =str(fullUrl) ,#'urn:uuid:4e84028e-6c09-429e-998f-d8ab3c18d1a4',
                            subject =subject['reference'],#'{"reference" : "Patient/1"}',
                            recipient =recipient[0]['reference'] ,#'{"reference" : "Practitioner/1"}',
                            type = type['text'],#'{"text" : "Skull and Facial bones and Mandible X-ray for dental measurement"}',
                            author =author[0]['reference'] ,#'[ {"reference" : "Practitioner/1"} ]',
                            value = identifier[0]['value'],#'[ {"system" : "urn:oid:1.2.410.19376.3","value" : "urn:uuid:4e84028e-6c09-429e-998f-d8ab3c18d1a4"} ]',
                            system =identifier[0]['system'],
                            created = str(created),#"2016-10-19T11:03:58+09:00",
                            status =str(status) ,#"current",
                            description = str(description),#"Wisdom tooth extraction progress note",
                            content = content)#'[ {"pReference" : {"reference" : "urn:uuid:898eb19f-fea3-4fde-8af7-bd1e3234636b"}} ]')
    session.add(new_manifest_resource)
    session.commit()

    new_manifest = Manifest(fullUrl = str(fullUrl),#'urn:uuid:4e84028e-6c09-429e-998f-d8ab3c18d1a4',
                            request =str(request))#'{"method" : "POST","url" : "DocumentManifest" }')
    session.add(new_manifest)
    session.commit()

# Insert Reference
def insertReference(resourceType = None, fullUrl= None, subject = None, type = None, author = None, custodian = None,
                    authenticator = None, masterIdentifier = None, indexed = None, created = None, status = None,
                    description = None, securityLabel = None, content = None, request = None, contentUrl = None):
    new_reference_resource = Resource(
                            resourceType = str(resourceType),#'DocumentReference',
                            fullUrl = str(fullUrl),#'urn:uuid:898eb19f-fea3-4fde-8af7-bd1e3234636b',
                            subject =subject['reference'],#'{"reference" : "Patient/1"}',
                            type = type['text'],#'{"text" : "Dental X-rays and other images (not DICOM)"}',
                            author = author[0]['reference'],#'[ {"reference" : "Practitioner/1"} ]',
                            custodian = custodian['reference'],# '"reference" : "Organization/1"',
                            authenticator = authenticator['reference'],#'{"reference" : "Organization/1"}',
                            value=masterIdentifier['value'],
                            system=masterIdentifier['system'],
                            indexed = str(indexed),#'2016-10-19T11:03:58+09:00',
                            created = str(created),#"2016-10-19T11:03:58+09:00",
                            status = str(status),#"current",
                            description = str(description),#"Dental",
                            securityLabel_coding_system = securityLabel[0]['coding'][0]['system'],
                            securityLabel_coding_code = securityLabel[0]['coding'][0]['code'],
                            securityLabel_coding_display = securityLabel[0]['coding'][0]['display'],
                            content_attachment_contentType = content[0]['attachment']['contentType'],
                            content_attachment_url = contentUrl,
                            content_attachment_size = content[0]['attachment']['size'],
                            content_attachment_hash = content[0]['attachment']['hash'],
                            content_format_system = content[0]['format'][0]['system'],
                            content_attachment_code = content[0]['format'][0]['code'],
                            content_attachment_display = content[0]['format'][0]['display'])#'[ {"attachment" : {"contentType" : "application/xml","url" : "urn:uuid:d93d085f-24c5-49d6-a161-e70dd1c9f024","size" : 46001, "hash" : "ZABHIA2ZNDmA1owkjRguCMtJcNs="},"format" : [ {"system" : "urn:oid:1.3.6.1.4.1.19376.1.2.3","code" : "urn:ihe:pcc:xds-ms:2007","display" : "XDS Medical Summaries"} ]} ]',


    session.add(new_reference_resource)
    session.commit()

    new_reference = Reference(fullUrl =str(fullUrl),#'urn:uuid:898eb19f-fea3-4fde-8af7-bd1e3234636b',
                              request =str(request))
    session.add(new_reference)
    session.commit()

#insert Content
def insertContent(resourceType = None,fullUrl = None, contentType = None, content = None, request = None):
    new_content_resource = Resource(
                            resourceType = str(resourceType),#'Binary',
                            fullUrl = str(fullUrl),#'urn:uuid:d93d085f-24c5-49d6-a161-e70dd1c9f024',
                            contentType = str(contentType),#'image/jpeg',
                            content = str(content))#"base64encodedHerelocation")
    session.add(new_content_resource)
    session.commit()
    #Insert Content
    new_content = Content(fullUrl = str(fullUrl),#'urn:uuid:d93d085f-24c5-49d6-a161-e70dd1c9f024',
                            request = str(request))#'{"method" : "POST","url" : "Patient"}')
    session.add(new_content)
    session.commit()
    print("insertContent")
''''''''''''''''''''''''''''''''''''''''''''''''''''SELECT'''''''''''''''''''''''''''''''''''''''''''''''''''
# SELECT MANIFEST
def selectManifest():
    # session.query(Child).filter(#Address.person == person).one()
    manifests = session.query(Manifest).all()
    print("all reference url")
    manifestList = []
    for manifest in manifests:
        manifestList.append(manifest)
        print(manifest.fullUrl)
    return manifestList
#selectManifest()

# SELECT REFERENCE
def selectReference():
    # session.query(Child).filter(#Address.person == person).one()
    references = session.query(Reference).all()
    print("all reference url")
    referenceList = []
    for reference in references:
        referenceList.append(reference)
        print(reference.fullUrl)
    return referenceList

# SELECT CONTENT
def selectContent():
    # session.query(Child).filter(#Address.person == person).one()
    contents = session.query(Content).all()
    print("all content url")
    contentList = []
    for content in contents:
        print(content)
        contentList.append(content.fullUrl)
    return str(contentList)

# SELECT RESOURCE
def selectResource():
    # session.query(Child).filter(#Address.person == person).one()
    resources = session.query(Resource).all()
    print("all reference url")
    resourcetList = []
    i = 0
    for resource in resources:
        resourcetList.append(resource)
        print(i)
        print(resource.fullUrl)
    return resourcetList
#selectResource()
#{'reference': 'Patient/201'}
#{'reference': 'Patient/201'}


# SELECT PATIENT RESOURCE
def selectPatientResource():
    # session.query(Child).filter(#Address.person == person).one()
    patientResources = session.query(PatientResource).all()
    print("all reference url")
    patientResourceList = []
    for patientResource in patientResources:
        patientResourceList.append(patientResource)
        print(patientResource.value)
    return patientResourceList
#selectPatientResource()

# SELECT MANIFEST BY RESOURCE ID
def selectManifest_by_resource_id(resource_id):
    manifests = session.query(Manifest).filter(Manifest.fullUrl == resource_id).all()

    print("all manifest urldd")
    manifestsList = []
    for manifest in manifests:
        print(manifest.resource.fullUrl)
        resource = session.query(Resource).filter(Resource.fullUrl == resource_id).first()
        print('ttest')
        print(resource)
        print(manifest.resource.resourceType)
        print(resource.resourceType)
        resultManifest = {
            "id": manifest.fullUrl,
            "resourceType": resource.resourceType,
            "subject": {"reference": resource.subject},
            "recipient": [{"reference": resource.recipient}],
            "type": {"text": manifest.resource.type},
            "author": [{"reference": resource.author}],
            "identifier": [{  #################################################CHECK
                "system": resource.value,
                "value": resource.system
            }],
            "created": resource.created,
            "status": resource.status,
            "description": resource.description,
            "content": [{"pReference": {"reference": resource.content}}]
        }
        manifestsList.append(resultManifest)
        print(manifestsList)
        print('test')
        print(len(manifestsList))
    if len(manifestsList) == 1:
        return manifestsList[0]
    reorganizedList = []
    for manifest in manifestsList:
        reorganizedList.append({"resource": manifest})
    return {"resourceType": "Bundle",
            "type": "searchset",
            "entry": reorganizedList
            }

# SELECT MANIFEST BY PATIENT RESOURCE ID
def selectManifest_by_patient_resource_id(p_resource_id):
    print('dd')
    print(p_resource_id)
    print("{'reference': '"+p_resource_id+"'}")
    resources = session.query(Resource).filter(Resource.subject == p_resource_id)\
        .filter(Resource.resourceType == "DocumentManifest").all()
    print("all manifest url")
    manifestsList = []
    print(resources)
    for resource in resources:
        manifest = session.query(Manifest).filter(Manifest.resource == resource).first()
        resultManifest = {
                "id": manifest.fullUrl,
                "resourceType": resource.resourceType,
                "subject": {"reference": resource.subject},
                "recipient": [{"reference": resource.recipient}],
                "type": {"text": manifest.resource.type},
                "author": [{"reference": resource.author}],
                "identifier": [{  #################################################CHECK
                    "system": resource.value,
                    "value": resource.system
                }],
                "created": resource.created,
                "status": resource.status,
                "description": resource.description,
                "content": [{"pReference" : { "reference" : resource.content}}]
        }
        manifestsList.append(resultManifest)
        print(manifestsList)
        print('test')
        print(len(manifestsList))
    if len(manifestsList) == 1 :
        return manifestsList[0]
    reorganizedList = []
    for manifest in manifestsList:
        reorganizedList.append({"resource":manifest})
    return {"resourceType": "Bundle",
            "type": "searchset",
            "entry": reorganizedList
            }

# SELECT MANIFEST ALL
def selectManifest_All():
    manifests = session.query(Manifest).all()
    print("all manifest urldd")
    manifestsList = []
    for manifest in manifests:
        print(manifest.resource.fullUrl)
        resource = session.query(Resource).filter(Resource.fullUrl == manifest.fullUrl).first()
        print('ttest')
        print(resource)
        print(manifest.resource.resourceType)
        print(resource.resourceType)
        resultManifest = {
            "id": manifest.fullUrl,
            "resourceType": resource.resourceType,
            "subject": {"reference": resource.subject},
            "recipient": [{"reference": resource.recipient}],
            "type": {"text": manifest.resource.type},
            "author": [{"reference": resource.author}],
            "identifier": [{  #################################################CHECK
                "system": resource.value,
                "value": resource.system
            }],
            "created": resource.created,
            "status": resource.status,
            "description": resource.description,
            "content": [{"pReference": {"reference": resource.content}}]
        }
        manifestsList.append(resultManifest)
        print(manifestsList)
        print('test')
        print(len(manifestsList))
    if len(manifestsList) == 1:
        return manifestsList[0]
    reorganizedList = []
    for manifest in manifestsList:
        reorganizedList.append({"resource": manifest})
    return {"resourceType": "Bundle",
            "type": "searchset",
            "entry": reorganizedList
            }


# SELECT REFERENCE BY RESOURCE ID
def selectReference_by_resource_id(resource_id):
    print('reference test')
    print(resource_id)
    references = session.query(Reference).filter(Reference.fullUrl == resource_id).all()

    print("all manifest urldd")
    referencesList = []
    for reference in references:
        print(reference.resource.fullUrl)
        resource = session.query(Resource).filter(Resource.fullUrl == reference.fullUrl).first()
        print('ttest')
        print(resource)
        print(reference.resource.resourceType)
        print(resource.resourceType)
        resultReference = {
            "id": reference.fullUrl,
            "resourceType": resource.resourceType,
            "subject" : {"reference":resource.subject},
            "type": {"text": resource.type},
            "author": [{"reference": resource.author}],
            "custodian": {"reference": resource.custodian},
            "authenticator": {"reference": resource.authenticator},
            "masterIdentifier": {  #################################################CHECK
                "system": resource.system,
                "value": resource.value
            },
            "created": resource.created,
            "indexed": resource.indexed,
            "status": resource.status,
            "description": resource.description,
            "securityLabel": [{
                "coding": [{
                    "system": resource.securityLabel_coding_system,
                    "code": resource.securityLabel_coding_code,
                    "display": resource.securityLabel_coding_display
                }]
            }],
            "content": [{
                "attachment": {
                    "contentType": resource.content_attachment_contentType,
                    "url": resource.content_attachment_url,
                    "size": int(resource.content_attachment_size),
                    "hash": resource.content_attachment_hash
                },
                "format": [{
                    "system": resource.content_format_system,
                    "code": resource.content_attachment_code,
                    "display": resource.content_attachment_display
                }]
            }]
        }
        referencesList.append(resultReference)
        print(referencesList)
        print('test')
        print(len(referencesList))
    if len(referencesList) == 1:
        return referencesList[0]
    reorganizedList = []
    for reference in referencesList:
        reorganizedList.append({"resource": reference})
    return {"resourceType": "Bundle",
            "type": "searchset",
            "entry": reorganizedList
            }


# SELECT REFERENCE BY PATIENT RESOURCE ID
def selectReference_by_patient_resource_id(p_resource_id):
    print('dd')
    print(p_resource_id)
    print("{'reference': '"+p_resource_id+"'}")
    references = session.query(Resource).filter(Resource.subject == p_resource_id)\
        .filter(Resource.resourceType == "DocumentReference").all()
    print("all Reference url")
    referencesList = []
    for reference in references:
        resource = session.query(Resource).filter(Resource.fullUrl == reference.fullUrl).first()
        print('ttest')
        print(resource)
        resultReference = {
            "id": reference.fullUrl,
            "resourceType": resource.resourceType,
            "subject" : {"reference":resource.subject},
            "type": {"text": resource.type},
            "author": [{"reference": resource.author}],
            "custodian": {"reference": resource.custodian},
            "authenticator": {"reference": resource.authenticator},
            "masterIdentifier": {  #################################################CHECK
                "system": resource.system,
                "value": resource.value
            },
            "created": resource.created,
            "indexed": resource.indexed,
            "status": resource.status,
            "description": resource.description,
            "securityLabel": [{
                "coding": [{
                    "system": resource.securityLabel_coding_system,
                    "code": resource.securityLabel_coding_code,
                    "display": resource.securityLabel_coding_display
                }]
            }],
            "content": [{
                "attachment": {
                    "contentType": resource.content_attachment_contentType,
                    "url": resource.content_attachment_url,
                    "size": int(resource.content_attachment_size),
                    "hash": resource.content_attachment_hash
                },
                "format": [{
                    "system": resource.content_format_system,
                    "code": resource.content_attachment_code,
                    "display": resource.content_attachment_display
                }]
            }]
        }
        referencesList.append(resultReference)
        print(referencesList)
        print('test')
        print(len(referencesList))
    if len(referencesList) == 1:
        return referencesList[0]
    reorganizedList = []
    for reference in referencesList:
        reorganizedList.append({"resource": reference})
    return {"resourceType": "Bundle",
            "type": "searchset",
            "entry": reorganizedList
            }

# SELECT REFERENCE ALL
def selectReference_All():
    references = session.query(Reference).all()
    print("all manifest urldd")
    referencesList = []
    for reference in references:
        print(reference.resource.fullUrl)
        resource = session.query(Resource).filter(Resource.fullUrl == reference.fullUrl).first()
        print('ttest')
        print(resource)
        print(reference.resource.resourceType)
        print(resource.resourceType)
        resultReference = {
            "id": reference.fullUrl,
            "resourceType": resource.resourceType,
            "subject" : {"reference":resource.subject},
            "type": {"text": resource.type},
            "author": [{"reference": resource.author}],
            "custodian": {"reference": resource.custodian},
            "authenticator": {"reference": resource.authenticator},
            "masterIdentifier": {  #################################################CHECK
                "system": resource.system,
                "value": resource.value
            },
            "created": resource.created,
            "indexed": resource.indexed,
            "status": resource.status,
            "description": resource.description,
            "securityLabel" : [ {
                "coding" : [{
                    "system" : resource.securityLabel_coding_system,
                    "code" : resource.securityLabel_coding_code,
                    "display" :resource.securityLabel_coding_display
                }]
            }],
            "content": [{
                "attachment": {
                    "contentType": resource.content_attachment_contentType,
                    "url" :resource.content_attachment_url,
                    "size" : int(resource.content_attachment_size),
                    "hash" : resource.content_attachment_hash
                },
                "format" : [ {
                    "system" : resource.content_format_system,
                    "code": resource.content_attachment_code,
                    "display" : resource.content_attachment_display
                }]
            }]
        }
        referencesList.append(resultReference)
        print(referencesList)
        print('test')
        print(len(referencesList))
    if len(referencesList) == 1:
        return referencesList[0]
    reorganizedList = []
    for reference in referencesList:
        reorganizedList.append({"resource": reference})
    return {"resourceType": "Bundle",
            "type": "searchset",
            "entry": reorganizedList
            }

def isValidPatientResourceId(value):
    patientResource = session.query(PatientResource).filter(PatientResource.value == value).first()
    print(patientResource)
    if patientResource == None:
        return False
    return True

