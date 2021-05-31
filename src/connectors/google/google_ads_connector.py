from typing import Dict
from google.ads.googleads.client import GoogleAdsClient
from oauth2client.client import credentials_from_code
from connectors.base_connector import BaseConnector


class GoogleAdsConnector(BaseConnector):

    TYPE = 'google'
    SCOPES = ['https://www.googleapis.com/auth/adwords', 'https://www.googleapis.com/auth/analytics.readonly']

    def __init__(self, client_id, client_secret, developer_token):
        self.credentials_dict = {
            'client_id': client_id,
            'client_secret': client_secret,
            'developer_token': developer_token
        }

    @property
    def type(self):
        return GoogleAdsConnector.TYPE

    def build_connector(self, connector_configuration):

        credentials = credentials_from_code(
            client_id=self.credentials_dict['client_id'],
            client_secret=self.credentials_dict['client_secret'],
            scope=GoogleAdsConnector.SCOPES,
            code=connector_configuration['authorization_code'])

        return {'refresh_token': credentials.refresh_token}

    def load_options(self, connector_configuration):

        client = GoogleAdsClient.load_from_dict({
            **self.credentials_dict,
            'refresh_token': connector_configuration['refresh_token']
        })

        # Load all accounts
        ads_campaigns = self.__load_ads_accounts(client)

        # Load all campaigns for all accounts
        accounts_campaigns = self.__load_ads_campaigns(client, ads_campaigns)

        return {
            'ads_accounts': accounts_campaigns,
            'ga_accounts': {
                'GA Account 1': {
                    'Property 1': ['metric1', 'metric2']
                }
            }
        }

    @staticmethod
    def __load_ads_campaigns(client, accounts):

        accounts_campaigns = dict()

        query = """
                SELECT
                    campaign.id,
                    campaign.name
                FROM campaign
                ORDER BY campaign.id
            """

        for manager_id, accounts in accounts.items():

            # Header
            client.login_customer_id = str(manager_id)

            googleads_service = client.get_service("GoogleAdsService")

            for account in accounts:
                response = googleads_service.search_stream(customer_id=str(account), query=query)

                accounts_campaigns[account] = []

                for batch in response:
                    for row in batch.results:
                        accounts_campaigns[account].append(row.campaign.name)

        return accounts_campaigns

    @staticmethod
    def __load_ads_accounts(client) -> Dict[int, list]:

        # Gets instances of the GoogleAdsService and CustomerService clients.
        googleads_service = client.get_service("GoogleAdsService")
        customer_service = client.get_service("CustomerService")

        # A collection of customer IDs to handle.
        seed_customer_ids = []

        # Creates a query that retrieves all child accounts of the manager
        # specified in search calls below.
        query = """
                    SELECT
                      customer_client.client_customer,
                      customer_client.level,
                      customer_client.manager,
                      customer_client.descriptive_name,
                      customer_client.currency_code,
                      customer_client.time_zone,
                      customer_client.id
                    FROM customer_client
                    WHERE customer_client.level <= 1"""

        customer_resource_names = (
            customer_service.list_accessible_customers().resource_names
        )

        for customer_resource_name in customer_resource_names:

            try:
                customer = customer_service.get_customer(
                    resource_name=customer_resource_name
                )
                seed_customer_ids.append(customer.id)
            except Exception:
                print('Problems fetching resource %s' % customer_resource_name)

        for seed_customer_id in seed_customer_ids:
            # Performs a breadth-first search to build a Dictionary that maps
            # managers to their child accounts (customerIdsToChildAccounts).
            unprocessed_customer_ids = [seed_customer_id]
            customer_ids_to_child_accounts = dict()
            root_customer_client = None

            while unprocessed_customer_ids:
                customer_id = int(unprocessed_customer_ids.pop(0))
                response = googleads_service.search(
                    customer_id=str(customer_id), query=query
                )

                # Iterates over all rows in all pages to get all customer
                # clients under the specified customer's hierarchy.
                for googleads_row in response:
                    customer_client = googleads_row.customer_client

                    # The customer client that with level 0 is the specified
                    # customer.
                    if customer_client.level == 0:
                        if root_customer_client is None:
                            root_customer_client = customer_client
                        continue

                    # For all level-1 (direct child) accounts that are a
                    # manager account, the above query will be run against them
                    # to create a Dictionary of managers mapped to their child
                    # accounts for printing the hierarchy afterwards.
                    if customer_id not in customer_ids_to_child_accounts:
                        customer_ids_to_child_accounts[customer_id] = []

                    customer_ids_to_child_accounts[customer_id].append(
                        customer_client.id
                    )

                    if customer_client.manager:
                        # A customer can be managed by multiple managers, so to
                        # prevent visiting the same customer many times, we
                        # need to check if it's already in the Dictionary.
                        if (
                                customer_client.id not in customer_ids_to_child_accounts
                                and customer_client.level == 1
                        ):
                            unprocessed_customer_ids.append(customer_client.id)

            return customer_ids_to_child_accounts
