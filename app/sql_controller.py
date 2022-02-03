from app.database import (
    Session,
    Address,
    Breed,
    Client,
    Code,
    Patient,
    PhoneNumber,
    Species,
    Transaction,
    Vaccine,
    MedicalNote
)
from app.helpers import get_logger
from typing import List, Dict, Any
import os

logger = get_logger(__name__)
current_dir = os.path.dirname(__file__)
parent_dir = os.path.split(current_dir)[0]
files_dir = os.path.join(current_dir, "files")


class SQLController(object):
    resource_name: str
    fields: List[str]

    def extract_fields(self):
        pass

    def make_object(self):
        pass

    def upsert(self, data):
        pass

    def update(self, res, data):
        pass

    def write(self, data):
        pass


class ClientSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        client: Client = Client.query.get(data['pimsId'])
        if client:
            self.update(client, data)
        else:
            self.write(data)

    def update(self, client, data):
        client.first_name = data['firstName']
        client.last_name = data['lastName']
        client.balance = data['balance']
        client.classification_code = data['classificationCode']
        client.classification_description = data['classificationDescription']
        client.entered_date = data['enteredDate']

        self.session.add(client)
        self.session.commit()

    def write(self, data):
        client = Client()
        client.pims_id = data['pimsId']
        client.first_name = data['firstName']
        client.last_name = data['lastName']
        client.balance = data['balance']
        client.classification_code = data['classificationCode']
        client.classification_description = data['classificationDescription']
        client.entered_date = data['enteredDate']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(client)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data


        # file = os.path.join(files_dir, 'client_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

class BreedSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        breed: Breed = Breed.query.get(data['id'])
        if breed:
            self.update(breed, data)
        else:
            self.write(data)

    def update(self, breed, data):
        breed.description = data['description']

        self.session.add(breed)
        self.session.commit()

    def write(self, data):
        breed = Breed()
        breed.id = data['id']
        breed.description = data['description']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(breed)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data


        # file = os.path.join(files_dir, 'breed_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

class CodeSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        code: Code = Code.query.get(data['id'])
        if code:
            self.update(code, data)
        else:
            self.write(data)

    def update(self, code, data):
        code.code = data['code']
        code.code_category = data['codeCategory']
        code.code_category_description = data['codeCategoryDescription']
        code.item_description = data['itemDescription']

        self.session.add(code)
        self.session.commit()

    def write(self, data):
        code = Code()
        code.code = data['code']
        code.code_category = data['codeCategory']
        code.code_category_description = data['codeCategoryDescription']
        code.id = data['id']
        code.item_description = data['itemDescription']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(code)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data

        # file = os.path.join(files_dir, 'code_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

class AddressSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        address: Address = Address.query.get(data['id'])
        if address:
            self.update(address, data)
        else:
            self.write(data)

    def update(self, address, data):
        address.address_line1 = data['addressLine1']
        address.address_line2 = data['addressLine2']
        address.city = data['city']
        address.client_pims_id = data['client']['pimsId']
        address.postal_code = data['postalCode']
        address.state_province = data['stateProvince']

        self.session.add(address)
        self.session.commit()

    def write(self, data):
        address = Address()
        address.address_line1 = data['addressLine1']
        address.address_line2 = data['addressLine2']
        address.city = data['city']
        address.client_pims_id = data['client']['pimsId']
        address.id = data['id']
        address.postal_code = data['postalCode']
        address.state_province = data['stateProvince']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(address)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data

        # file = os.path.join(files_dir, 'address_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

class PhoneNumberSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        phone: PhoneNumber = PhoneNumber.query.get(data['id'])
        if phone:
            self.update(phone, data)
        else:
            self.write(data)

    def update(self, phone, data):
        phone.client_pims_id = data['client']['pimsId']
        phone.is_primary = data['isPrimary']
        phone.number = data['number']
        phone.is_sms_enabled = data['sMS']

        self.session.add(phone)
        self.session.commit()

    def write(self, data):
        phone = PhoneNumber()
        phone.client_pims_id = data['client']['pimsId']
        phone.id = data['id']
        phone.is_primary = data['isPrimary']
        phone.number = data['number']
        phone.is_sms_enabled = data['sMS']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(phone)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data

        # file = os.path.join(files_dir, 'phone_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

class SpeciesSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        species: Species = Species.query.get(data['id'])
        if species:
            self.update(species, data)
        else:
            self.write(data)

    def update(self, species, data):
        species.description = data['description']
        self.session.add(species)
        self.session.commit()

    def write(self, data):
        species = Species()
        species.id = data['id']
        species.description = data['description']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(species)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data

        # file = os.path.join(files_dir, 'species_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)


class PatientSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        patient: Patient = Patient.query.get(data['id'])
        if patient:
            self.update(patient, data)
        else:
            self.write(data)

    def update(self, patient, data):
        wrote = False
        duplicate = False
        error = False

        patient.alerts = data['alerts']
        patient.allergies = data['allergies']
        patient.color = data['color']
        patient.current_weight = data['currentWeight']
        patient.date_of_birth = data['dateOfBirth']
        patient.date_of_death = data['dateOfDeath']
        patient.entered_date = data['enteredDate']
        patient.gender_description = data['genderDescription']
        patient.microchip = data['microChip']
        patient.name = data['name']
        patient.owner_pims_id = data['owner']['pimsId']
        patient.rabies = data['rabies']

        if data.get('patientBreed'):
            patient.patient_breed = data.get('patientBreed')['id']
        if data.get('patientSpecies'):
            patient.patient_species = data['patientSpecies']['id']

        self.session.commit()
        wrote = True

        return (wrote, duplicate, error)

    def write(self, data):
        patient = Patient()
        patient.id = data['id']
        patient.alerts = data['alerts']
        patient.allergies = data['allergies']
        patient.color = data['color']
        patient.current_weight = data['currentWeight']
        patient.date_of_birth = data['dateOfBirth']
        patient.date_of_death = data['dateOfDeath']
        patient.entered_date = data['enteredDate']
        patient.gender_description = data['genderDescription']
        patient.microchip = data['microChip']
        patient.name = data['name']
        patient.rabies = data['rabies']
        patient.owner_pims_id = data['owner']['pimsId']

        if data.get('patientBreed'):
            patient.patient_breed = data.get('patientBreed')['id']
        if data.get('patientSpecies'):
            patient.patient_species = data['patientSpecies']['id']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(patient)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data


        # file = os.path.join(files_dir, 'patient_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

class TransactionSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        transaction: Transaction = Transaction.query.get(data['id'])
        if transaction:
            self.update(transaction, data)
        else:
            self.write(data)

    def update(self, transaction, data):
        wrote = False
        duplicate = False
        error = False

        transaction.code_id = None

        if data.get('client'):
            transaction.client_pims_id = data['client']['pimsId']

        if data.get('patient'):
            transaction.patient_pims_id = data['patient']['id']

        transaction.amount = data['amount']
        transaction.invoice_number = data['invoiceNumber']
        transaction.quantity = data['quantity']
        transaction.date_performed = data['datePerformed']
        transaction.comments = data['comments']
        transaction.description = data['description']

        self.session.commit()
        wrote = True

        return (wrote, duplicate, error)

    def write(self, data):
        transaction = Transaction()
        transaction.id = data['id']
        transaction.code_id = None

        if data.get('client'):
            transaction.client_pims_id = data['client']['pimsId']

        if data.get('patient'):
            transaction.patient_pims_id = data['patient']['id']

        transaction.amount = data['amount']
        transaction.invoice_number = data['invoiceNumber']
        transaction.quantity = data['quantity']
        transaction.date_performed = data['datePerformed']
        transaction.comments = data['comments']
        transaction.description = data['description']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(transaction)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data

        # file = os.path.join(files_dir, 'transaction_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)


class VaccineSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        vaccine: Vaccine = Vaccine.query.get(data['id'])
        if vaccine:
            self.update(vaccine, data)
        else:
            self.write(data)

    def update(self, vaccine, data):
        wrote = False
        duplicate = False
        error = False

        vaccine.date_given = data['dateGiven']
        vaccine.description = data['description']
        vaccine.expiration_date = data['expirationDate']
        vaccine.manufacturer = data['manufacturer']

        if data.get('patient'):
            vaccine.patinet_id = data['patient']['id']
            if data.get('patient').get('owner'):
                vaccine.client_pims_id = data['patient']['owner']['pimsId']

        vaccine.tag = data['tag']
        vaccine.vaccine_description = data['vaccineDescription']

        self.session.add(vaccine)
        self.session.commit()

        wrote = True

        return (wrote, duplicate, error)

    def write(self, data):
        vaccine = Vaccine()
        vaccine.date_given = data['dateGiven']
        vaccine.description = data['description']
        vaccine.expiration_date = data['expirationDate']
        vaccine.id = data['id']
        vaccine.manufacturer = data['manufacturer']

        if data.get('patient'):
            vaccine.patinet_id = data['patient']['id']
            if data.get('patient').get('owner'):
                vaccine.client_pims_id = data['patient']['owner']['pimsId']

        vaccine.tag = data['tag']
        vaccine.vaccine_description = data['vaccineDescription']

        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(vaccine)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data

        # file = os.path.join(files_dir, 'vaccine_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

class MedicalNoteSQLController(SQLController):
    def __init__(self, session: Session, account_id: str):
        self.session = session
        self.account_id = account_id

    def upsert(self, data):
        medical_note: MedicalNote = MedicalNote.query.get(data['id'])
        if medical_note:
            self.update(medical_note, data)
        else:
            self.write(data)

    def update(self, medical_note, data):
        wrote = False
        duplicate = False
        error = False

        medical_note.date_entered = data['dateEntered']
        medical_note.deleted = data['deleted']
        medical_note.imported = data['imported']
        medical_note.note = data['note']

        if data.get('patient'):
            medical_note.note = data['patient']['id']

        medical_note.status = data['status']
        medical_note.updated = data['updated']

        self.session.add(medical_note)
        self.session.commit()

        wrote = True

        return (wrote, duplicate, error)

    def write(self, data):
        medical_note = MedicalNote()

        medical_note.id = data['id']
        medical_note.date_entered = data['dateEntered']
        medical_note.deleted = data['deleted']
        medical_note.imported = data['imported']
        medical_note.note = data['note']

        if data.get('patient'):
            medical_note.note = data['patient']['id']

        medical_note.status = data['status']
        medical_note.updated = data['updated']


        error = False
        error_data = None
        wrote = False
        duplicate = False
        try:
            self.session.add(medical_note)
            self.session.commit()
            wrote = True
        except Exception as e:
            self.session.rollback()
            error = True
            if e.orig.args[0] == 1062: # Duplicate entry
                duplicate = True
            else:
                error_data = data

        # file = os.path.join(files_dir, 'medical_note_errors.txt')
        # if error_data:
        #     with open(file, 'a') as f:
        #         f.write(f"{error_data},\n")

        return (wrote, duplicate, error)

