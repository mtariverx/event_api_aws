import sqlalchemy as db

DIALECT = 'mysql'
DRIVER = 'pymysql'
USER = 'root'
PASS = 'Samostrel95!'
HOST = 'localhost'
PORT = '3306'

# engine = db.create_engine(f'sqlite:///db.sqlite')
engine = db.create_engine(f'{DIALECT}+{DRIVER}://{USER}:{PASS}@{HOST}:{PORT}/evet')

connection = engine.connect()

metadata = db.MetaData()

address = db.Table(
    "address",
    metadata,
    db.Column('pimsId', db.String(255)),
    db.Column('id', db.String(255)),
    db.Column('addressLine1', db.String(255)),
    db.Column('addressLine2', db.String(255)),
    db.Column('city', db.String(255)),
    db.Column('stateProvince', db.String(255)),
    db.Column('postalCode', db.String(255)),
    #fk client.pimsId
    #fk client.pets.pimsId
)

breed = db.Table(
    "breed",
    metadata,
    db.Column('id', db.String(255)),
    db.Column('description', db.String(255)),
    db.Column('pimsId', db.String(255)),
)

client = db.Table(
    "client",
    metadata,
    db.Column('pimsId', db.Integer()),
    db.Column('firstName', db.String(255)),
    db.Column('lastName', db.String(255)),
    db.Column('balance', db.String(255)),
    db.Column('classificationCode', db.String(255)),
    db.Column('classificationDescription', db.String(255)),
    #fk pets.pimsId
    db.Column('enteredDate', db.String(255)),
)

code = db.Table(
    "code",
    metadata,
    db.Column('pimsId', db.String(255)),
    db.Column('id', db.String(255)),
    db.Column('code', db.String(255)),
    db.Column('itemDescription', db.String(255)),
    db.Column('codeCategory', db.String(255)),
    db.Column('codeCategoryDescription', db.String(255)),
)

patient = db.Table(
    "patient",
    metadata,
    db.Column('pimsId', db.String(255)),
    db.Column('name', db.String(255)),
    db.Column('color', db.String(255)),
    db.Column('currentWeight', db.String(255)),
    db.Column('dateOfBirth', db.String(255)),
    db.Column('dateOfDeath', db.String(255)),
    db.Column('genderDescription', db.String(255)),
    db.Column('microChip', db.String(255)),
    db.Column('rabies', db.String(255)),
    db.Column('allergies', db.String(255)),
    db.Column('alerts', db.String(255)),
    db.Column('enteredDate', db.String(255)),
    #fk patientBreed.id
    #fk patientBreed.pimsId
    #fk patientSpecies.id
    #fk patientSpecies.pimsId
    #fk owner.pimsId
)

phone_number = db.Table(
    "phone_number",
    metadata,
    db.Column('pimsId', db.String(255)),
    db.Column('number', db.String(255)),
    db.Column('sMS', db.String(255)),
    db.Column('isPrimary', db.String(255)),
    #fk client.pimsId
)

soap = db.Table(
    "sOAP",
    metadata,
    db.Column('pimsId', db.String(255)),
    db.Column('subjective', db.String(255)),
    db.Column('objective', db.String(255)),
    db.Column('assessment', db.String(255)),
    db.Column('plan', db.String(255)),
    db.Column('createDate', db.String(255)),
    #fk patient.pimsId
    
)

species = db.Table(
    "species",
    metadata,
    db.Column('id', db.String(255)),
    db.Column('description', db.String(255)),
    db.Column('pimsId', db.String(255)),
)

transaction = db.Table(
    "transaction",
    metadata,
    db.Column('pimsId', db.String(255)),
    db.Column('amount', db.String(255)),
    db.Column('invoiceNumber', db.String(255)),
    db.Column('quantity', db.String(255)),
    db.Column('datePerformed', db.String(255)),
    db.Column('comments', db.String(255)),
    db.Column('description', db.String(255)),
    #fk client.pimsId
    #fk site.id
    #fk site.pimsId
    #fk code.id
    #fk code.pimsId
    #fk patient.pimsId
)

vaccine = db.Table(
    "vaccine",
    metadata,
    db.Column('expirationDate', db.String(255)),
    db.Column('dateGiven', db.String(255)),
    db.Column('tag', db.String(255)),
    db.Column('pimsId', db.String(255)),
    db.Column('manufacturer', db.String(255)),
    db.Column('vaccineDescription', db.String(255)),
    db.Column('description', db.String(255)),
    #fk patient.pimsId
    #fk patient.owner.firstName
    #fk patient.owner.lastName
    #fk patient.owner.pimsId
)

metadata.create_all(engine)