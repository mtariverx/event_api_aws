import json

import datetime
import time
from typing import Any, Dict, List, Tuple
import requests
from authlib.integrations.requests_client import OAuth2Session

from app.helpers import get_query_for, get_logger, grouped

PAGE_SIZE: int = 200

logger = get_logger(__name__)


class GQLService(object):
    """Main GQL service which is inherited by the resource services."""

    page_size: int = PAGE_SIZE
    domain: str = "https://apps.4act.net"  # "https://vsmart.vsurv.com"
    endpoint: str = "/api/data/graphql"
    url: str = f"{domain}{endpoint}"

    resource_name: str

    account_id: str
    token: str
    access_token: str
    headers: Dict[str, Any]

    query: str

    def __init__(self, account_id: str):
        """Instantiate the class for the provided `account_id`."""
        self.account_id = account_id
        self.headers = {"AccountId": account_id}
        self.token = self.get_token()

    def _set_token_header(self):
        self.headers["Authorization"] = f"Bearer {self.access_token}"

    def _make_request(self, body: dict) -> Dict[str, Any]:
        if self._access_token_is_expired():
            self.get_token()

        start_time = time.perf_counter()
        response = requests.post(
            url=self.url, headers=self.headers, data=json.dumps(body)
        )
        end_time = time.perf_counter() - start_time
        logger.info(f"Got {response.status_code} in {end_time}")

        if response.status_code == 401:
            time.sleep(1)
            self._make_request(body)

        if not response.ok:
            raise requests.HTTPError(f"{response.status_code}")

        try:
            rj = response.json()
        except Exception as e:
            logger.error(e)
            # return None

        return rj

    def fetch(self, updated_after, updated_before, page: int = 1) -> Dict[str, Any]:
        """Fetch data using the query for this service instance."""
        body = {
            "query": self.query,
            "variables": {
                "page_num": page,
                "page_size": self.page_size,
                "updated_after": updated_after,
                "updated_before": updated_before,
            },
        }

        try:
            rj = self._make_request(body)
        except requests.HTTPError as e:
            logger.error(e)
            return []

        data = rj["data"][self.resource_name]

        if len(data) != 0:
            logger.info(f"Fetched {len(data)} results from page {page}.")
            return data
        else:
            msg = "Fetched 0 results."
            logger.info(msg)
            return None

    def bulk_fetch(
        self, page_from: int = 1, page_to: int = 100, page_size: int = 250
    ):
        logger.info(f"Staring bulk fetch for {self.resource_name}")
        logger.info(f"Pages {page_from}-{page_to}")
        logger.info(f"Page size {self.page_size}")

        data: List[Dict[str, Any]] = []
        for i in range(page_from, page_to + 1):
            if self._access_token_is_expired():
                self.get_token()

            rj = self.fetch(page=i)
            if rj:
                data.append(rj)
            else:
                break

            if len(data) >= 2_500:
                yield data
                data = []

        yield data
        logger.info("Bulk fetch complete.")

    def threaded_bulk_fetch(self, page_from: int = 1, page_to: int = 100):
        import concurrent.futures

        logger.info(f"Staring bulk fetch for {self.resource_name}")
        logger.info(f"Pages {page_from}-{page_to}")
        logger.info(f"Page size {self.page_size}")

        pages = range(page_from, page_to + 1)
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []

            for i in grouped(pages, 10):
                if self._access_token_is_expired():
                    self.get_token()
                for p in i:
                    futures.append(executor.submit(self.fetch, page=p))

                for future in concurrent.futures.as_completed(futures):
                    if future.exception():
                        logger.error(
                            f"Future caught an exception: {future.exception()}"
                        )
                        break

                    result = future.result()
                    if result:
                        yield result
                        result = None
                        futures = []

        logger.info("Bulk fetch complete.")

    def _access_token_is_expired(self):
        current_time = datetime.datetime.now()

        if current_time > self.token_expires_at:
            return True
        else:
            return False

    def get_token(self):
        """Get Bearer token from the token endpoint.

        This method will update the `self.access_token` with the new token.
        """
        client_id = (
            "@!F7D1.BEFA.9D54.9D47!0001!0E97.E352!0008!2F54.47FA.2B6E.1CFE"
        )
        client_secret = "iambatman"
        token_endpoint = "https://id.4act.com/oxauth/restv1/token"
        username = "shotvet@shotvet.org"
        password = "EatPurplePota-toes"
        scope = "openid"

        client = OAuth2Session(client_id, client_secret, scope=scope)

        logger.debug("Fetching new token.")

        token = client.fetch_token(
            token_endpoint,
            username=username,
            password=password,
        )

        logger.info(f"Successfully got token {token.get('access_token')}")

        self.token_obtained_at = datetime.datetime.now()
        self.token_expires_at = (
            datetime.timedelta(seconds=token.get("expires_in"))
            + self.token_obtained_at
        )

        self.access_token = token.get("access_token")
        self._set_token_header()

        return token


class CodesGQLService(GQLService):
    resource_name = "codes"
    query = get_query_for(resource_name)


class ClientsGQLService(GQLService):
    resource_name = "clients"
    query = get_query_for(resource_name)


class TransactionsGQLService(GQLService):
    resource_name = "transactions"
    query = get_query_for(resource_name)


class AddressesGQLService(GQLService):
    resource_name = "addresses"
    query = get_query_for(resource_name)


class PhoneNumbersGQLService(GQLService):
    resource_name = "phoneNumbers"
    query = get_query_for(resource_name)


class PatientsGQLService(GQLService):
    resource_name = "patients"
    query = get_query_for(resource_name)


class BreedsGQLService(GQLService):
    resource_name = "breeds"
    query = get_query_for(resource_name)


class SpeciesGQLService(GQLService):
    resource_name = "species"
    query = get_query_for(resource_name)


class SOAPsGQLService(GQLService):
    resource_name = "sOAPs"
    query = get_query_for(resource_name)


class VaccinesGQLService(GQLService):
    resource_name = "vaccines"
    query = get_query_for(resource_name)

class MedicalNotesGQLService(GQLService):
    resource_name = "medicalNotes"
    query = get_query_for(resource_name)
