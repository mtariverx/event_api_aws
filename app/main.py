from app.gql_service import (
    GQLService,
    AddressesGQLService,
    BreedsGQLService,
    ClientsGQLService,
    CodesGQLService,
    MedicalNotesGQLService,
    PatientsGQLService,
    PhoneNumbersGQLService,
    SOAPsGQLService,
    SpeciesGQLService,
    TransactionsGQLService,
    VaccinesGQLService,
)
from app.write_controllers import (
    WriteController,
    AddressesWriteController,
    BreedsWriteController,
    ClientsWriteController,
    CodesWriteController,
    PatientsWriteController,
    PhoneNumbersWriteController,
    SOAPsWriteController,
    SpeciesWriteController,
    TransactionsWriteController,
    VaccinesWriteController,
)
from app.sql_controller import (
    ClientSQLController,
    BreedSQLController,
    CodeSQLController,
    AddressSQLController,
    MedicalNoteSQLController,
    PhoneNumberSQLController,
    PatientSQLController,
    SQLController,
    SpeciesSQLController,
    TransactionSQLController,
    VaccineSQLController
)
from app.database import Session

import concurrent.futures
import time
from app.helpers import prepare_pages, get_logger
from pprint import pprint

logger = get_logger(__file__)
def pull_for_account(account_id: str):
    fetchers = [
        AddressesGQLService,
        BreedsGQLService,
        ClientsGQLService,
        CodesGQLService,
        PatientsGQLService,
        PhoneNumbersGQLService,
        SOAPsGQLService,
        SpeciesGQLService,
        TransactionsGQLService,
        VaccinesGQLService,
    ]
    writers = [
        AddressesWriteController,
        BreedsWriteController,
        ClientsWriteController,
        CodesWriteController,
        PatientsWriteController,
        PhoneNumbersWriteController,
        SOAPsWriteController,
        SpeciesWriteController,
        TransactionsWriteController,
        VaccinesWriteController,
    ]

    for f, w in zip(fetchers, writers):
        fetcher = f(account_id)
        writer = w()

        a = [
            writer.write_csv([writer.extract_data(row) for row in d])
            for d in fetcher.bulk_fetch(1, 1000)
        ]


def threaded_pull_for_account(
    account_id: str,
    fetcher_service: GQLService,
    writer_controller: WriteController,
    pages: int,
):
    stop = False
    fetcher: GQLService = fetcher_service(account_id)
    time.sleep(1.5)
    writer: WriteController = writer_controller()
    prepared_pages = prepare_pages(pages)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []

        for x, y in prepared_pages:
            if stop:
                print("BREAKINGBREAKINGBREAKINGBREAKINGBREAKING")
                break
            for page in range(x, y):
                if fetcher._access_token_is_expired():
                    fetcher.get_token()

                futures.append(executor.submit(fetcher.fetch, page))
                time.sleep(0.2)

            done_futures, other_futures = concurrent.futures.wait(
                futures, return_when=concurrent.futures.ALL_COMPLETED
            )

            for future in done_futures:
                data = []
                result = future.result()
                if not result:
                    stop = True
                    continue
                for row in result:
                    data.append(writer.extract_data(row))
                writer.write_csv(data)

            futures = []

def threaded_pull_for_account_sql(
    account_id: str,
    fetcher_service: GQLService,
    writer_controller: SQLController,
    pages: int,
    session: Session,
    updated_after,
    updated_before,
):
    stop = False
    fetcher: GQLService = fetcher_service(account_id)
    time.sleep(1.5)
    writer: WriteController = writer_controller(session, account_id)
    prepared_pages = prepare_pages(pages)
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []

        for x, y in prepared_pages:
            if stop:
                print("BREAKINGBREAKINGBREAKINGBREAKINGBREAKING")
                break
            for page in range(x, y):
                if fetcher._access_token_is_expired():
                    fetcher.get_token()

                futures.append(executor.submit(fetcher.fetch, updated_after, updated_before, page))
                time.sleep(0.2)

            done_futures, other_futures = concurrent.futures.wait(
                futures, return_when=concurrent.futures.ALL_COMPLETED
            )

            error_count = 0
            wrote_count = 0
            duplicate_count = 0
            for future in done_futures:
                result = future.result()
                if not result:
                    stop = True
                    continue
                for row in result:
                    wrote, duplicate, error = writer.write(row)
                    if error:
                        error_count += 1
                    if wrote:
                        wrote_count += 1
                    if duplicate:
                        duplicate_count += 1
            print(f'Found {error_count} errors!\nWrote {wrote_count} rows!\nDuplicate count {duplicate_count}!')
            futures = []

if __name__ == "__main__":
    from database import Client
    from database import Breed
    from database import Species
    from database import Code
    from database import Address
    from database import PhoneNumber
    from database import Patient
    '''
    clients
    breeds
    species
    codes
    addresses
    phonenumbers
    patient
    transactions
    vaccines
    '''
    team_to_account = {
        # "Team Pharma": 2850,
        # "Team 2": 2845,
        # "Team 3": 2844,
        # "Team 4": 2843,
        # "Team 5": 2842,
        # "Team 6": 2847,
        # "Team 7": 2841,
        # "Team 8": 2840,
        # "Team 9": 7423,
        # "Team 10": 2852,
        # "Team 11": 2846,
        # "Team 12": 2838,
        # "Team 13": 2851,
        # "Team 14": 2837,
        # "Team 15": 7430,
        # "Team 16": 7425,
        # "Team 17": 2839,
        # "Team 18": 2848,
        # "Team 19": 2836,
        # "Team 20": 2835,
        # "Team 21": 3269,
        # "Team 22": 7422,
        # "Team 23": 2833,
        # "Team 24": 2832,
        # "Team 25": 5964,
        # "Team 26": 7431,
        # "Team 27": 7433,
        # "Team 28": 7434,
        # "Team 29": 5967,
        # "Team 30": 7424,
        # "Team 31": 5968,
        # "Team 32": 2849,
        # "Team 33": 4206,
        # "Team 34": 7435,
        # "Team 36": 7433,
        # "Team 38": 7432,
        # "Team 39": 7436,
        # "Team 40": 7437,
        # "Team 41": 7438,
        # "Team 42": 7439,
        # "Team 43": 7440,
        # "Team 44": 7441,
        "Team 45": 7442,
    }

    session = Session()

    for team, account_id in team_to_account.items():
        logger.info(f"!!!!\nPulling for team {team}, account_id {account_id}\n!!!")
        threaded_pull_for_account_sql(
            account_id=str(account_id),
            fetcher_service=MedicalNotesGQLService,
            writer_controller=MedicalNoteSQLController,
            pages=5000,
            session=session
        )

