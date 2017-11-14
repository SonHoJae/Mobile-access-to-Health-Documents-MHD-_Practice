from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('sqlite:///mhd_database.db')

# Patient Resource Table
class PatientResource(Base):
    __tablename__ = 'patient_resource'

    value = Column(String(250), primary_key=True)
    resourceType = Column(String(250))
    system = Column(String(250))
    family = Column(String(250))
    given = Column(String(250))
    gender = Column(String(250))
    birthDate = Column(String(25))

# Resource Table : it will connect manifest/reference table
class Resource(Base):
    __tablename__ = 'resource'
    fullUrl = Column(String(250), primary_key=True)
    resourceType = Column(String(250), nullable=True)
    subject = Column(String(250), nullable=True)
    recipient = Column(String(250), nullable=True)
    custodian = Column(String(250), nullable=True)
    authenticator = Column(String(250), nullable=True)
    masterIdentifier = Column(String(250), nullable=True)
    type = Column(String(250), nullable=True)
    author = Column(String(250), nullable=True)
    value = Column(String(250), nullable=True)
    system = Column(String(250), nullable=True)
    created = Column(String(250), nullable=True)
    indexed = Column(String(250), nullable=True)
    status = Column(String(250), nullable=True)
    description = Column(String(250), nullable=True)
    securityLabel_coding_system = Column(String(250), nullable=True)
    securityLabel_coding_code = Column(String(250), nullable=True)
    securityLabel_coding_display = Column(String(250), nullable=True)
    content = Column(String(250), nullable=True)
    content_attachment_contentType = Column(String(250), nullable=True)
    content_attachment_url = Column(String(250), nullable=True)
    content_attachment_size = Column(String(250), nullable=True)
    content_attachment_hash = Column(String(250), nullable=True)
    content_format_system = Column(String(250), nullable=True)
    content_attachment_code = Column(String(250), nullable=True)
    content_attachment_display = Column(String(250), nullable=True)
    contentType = Column(String(250), nullable=True)

# Manifest Table
class Manifest(Base):
    __tablename__ = 'manifest'
    id = Column(Integer, primary_key=True)
    fullUrl = Column(String(250), ForeignKey('resource.fullUrl'), unique=True, nullable=False)
    request = Column(String(250), nullable=False)
    resource = relationship(Resource)

# Reference Table
class Reference(Base):
    __tablename__ = 'reference'
    id = Column(Integer, primary_key=True)
    fullUrl = Column(String(250), ForeignKey('resource.fullUrl'), unique=True, nullable=False)
    request = Column(String(250), nullable=False)
    resource = relationship(Resource)

# Content Table
class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    fullUrl = Column(String(250), ForeignKey('resource.fullUrl'), unique=True, nullable=False)
    request = Column(String(250), nullable=False)
    resource = relationship(Resource)


Base.metadata.create_all(engine)
