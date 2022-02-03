from app.gql_service import (
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
from app.sql_controller import (
    ClientSQLController,
    BreedSQLController,
    CodeSQLController,
    AddressSQLController,
    MedicalNoteSQLController,
    PhoneNumberSQLController,
    PatientSQLController,
    SpeciesSQLController,
    TransactionSQLController,
    VaccineSQLController,
)

team_to_account_id = {
    "Team Pharma": 2850,
    "Team 2": 2845,
    "Team 3": 2844,
    "Team 4": 2843,
    "Team 5": 2842,
    "Team 6": 2847,
    "Team 7": 2841,
    "Team 8": 2840,
    "Team 9": 7423,
    "Team 10": 2852,
    "Team 11": 2846,
    "Team 12": 2838,
    "Team 13": 2851,
    "Team 14": 2837,
    "Team 15": 7430,
    "Team 16": 7425,
    "Team 17": 2839,
    "Team 18": 2848,
    "Team 19": 2836,
    "Team 20": 2835,
    "Team 21": 3269,
    "Team 22": 7422,
    "Team 23": 2833,
    "Team 24": 2832,
    "Team 25": 5964,
    "Team 26": 7431,
    "Team 27": 7433,
    "Team 28": 7434,
    "Team 29": 5967,
    "Team 30": 7424,
    "Team 31": 5968,
    "Team 32": 2849,
    "Team 33": 4206,
    "Team 34": 7435,
    "Team 36": 7433,
    "Team 38": 7432,
    "Team 39": 7436,
    "Team 40": 7437,
    "Team 41": 7438,
    "Team 42": 7439,
    "Team 43": 7440,
    "Team 44": 7441,
    "Team 45": 7442
}

service_to_controller = {
    ClientsGQLService: ClientSQLController,
    BreedsGQLService: BreedSQLController,
    SpeciesGQLService: SpeciesSQLController,
    CodesGQLService: CodeSQLController,
    AddressesGQLService: AddressSQLController,
    PhoneNumbersGQLService: PhoneNumberSQLController,
    PatientsGQLService: PatientSQLController,
    TransactionsGQLService: TransactionSQLController,
    VaccinesGQLService: VaccineSQLController,
    MedicalNotesGQLService: MedicalNoteSQLController,
}
