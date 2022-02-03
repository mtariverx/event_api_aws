from database import Session, Client, Breed, Species, Code, Address, PhoneNumber, Patient
from gql_service import SpeciesGQLService

session = Session()


# breeds = session.query(Breed).all()

# clean_breeds = []
# for breed in breeds:
#     is_duplicate = False

#     for clean_breed in clean_breeds:
#         if clean_breed.description == breed.description:
#             is_duplicate = True
#             print(f"Found duplicate: {breed}")
#             for patient in breed.patients:
#                 patient.patient_breed = clean_breed.id
#                 session.add(patient)

#             session.commit()   
#         else:
#             pass

#     if is_duplicate:
#         session.delete(breed)
#         session.commit()
#     else:
#         clean_breeds.append(breed)

def remove_duplicate_breeds():
    for n in range(1, 181):
        for breed in session.query(Breed).limit(1000).offset(1 if n==1 else n*1000):
            query_by_description = session.query(Breed).filter(Breed.description==breed.description)
            duplicate_count = query_by_description.count()
            if duplicate_count > 1:
                print(f"Found {duplicate_count} duplicates of {breed}")
                duplicates = query_by_description.filter(Breed.id!=breed.id).all()

                fixed_patients_count = 0
                for duplicate in duplicates:
                    for patient in duplicate.patients:
                        patient.patient_breed = breed.id
                        session.add(patient)
                        fixed_patients_count += 1
                    session.commit()
                    session.delete(duplicate)
                    session.commit()
                print(f"Fixed {fixed_patients_count} patients!")
            else:
                print(f"No duplicates of {breed}")
        
def remove_duplicate_species():
    for n in range(1, 181):
        for species in session.query(Species).limit(1000).offset(1 if n==1 else n*1000):
            query_by_description = session.query(Species).filter(Species.description==species.description)
            duplicate_count = query_by_description.count()
            if duplicate_count > 1:
                print(f"Found {duplicate_count} duplicates of {species}")
                duplicates = query_by_description.filter(Species.id!=species.id).all()

                fixed_patients_count = 0
                for duplicate in duplicates:
                    for patient in duplicate.patients:
                        patient.patient_species = species.id
                        session.add(patient)
                        fixed_patients_count += 1
                    session.commit()
                    session.delete(duplicate)
                    session.commit()
                print(f"Fixed {fixed_patients_count} patients!")
            else:
                print(f"No duplicates of {species}")


def remove_duplicate_addresses():
    for n in range(1, 5_700):
        for address in session.query(Address).limit(1000).offset(1 if n==1 else n*1000):
            query_by_address_line1 = session.query(Address).filter(
                Address.address_line1==address.address_line1,
                Address.client_pims_id==address.client_pims_id,    
            )
            duplicate_count = query_by_address_line1.count()
            if duplicate_count > 1:
                print(f"Found {duplicate_count} duplicates of {address.id} - {address.address_line1}")
                duplicates = query_by_address_line1.filter(Address.id!=address.id).all()
                for duplicate in duplicates:
                    session.delete(duplicate)
                    session.commit()
            else:
                print(f"No duplicates of {address.id} - {address.address_line1}")
                
def remove_duplicate_phone_numbers():
    for n in range(1, 8_400):
        for phone_number in session.query(PhoneNumber).limit(1000).offset(1 if n==1 else n*1000):
            query_by_number_and_client = session.query(PhoneNumber).filter(
                PhoneNumber.number==phone_number.number,
                PhoneNumber.client_pims_id==phone_number.client_pims_id,
                PhoneNumber.id!=phone_number.id,
            )
            duplicate_count = query_by_number_and_client.count()
            if duplicate_count > 1:
                print(f"Found {duplicate_count} duplicates of {phone_number.id} - {phone_number.number}")
                duplicates = query_by_number_and_client.all()
                for duplicate in duplicates:
                    session.delete(duplicate)
                    session.commit()
            else:
                print(f"No duplicates of {phone_number.id} - {phone_number.number}")
                

if __name__ == "__main__":
    remove_duplicate_phone_numbers()