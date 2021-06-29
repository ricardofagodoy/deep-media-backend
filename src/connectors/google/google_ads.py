import logging
from typing import Dict
from google.ads.googleads.client import GoogleAdsClient


class GoogleAds:

    @staticmethod
    def load_ads_properties(credentials):

        client = GoogleAdsClient.load_from_dict(credentials)

        # Load all Google Ads accounts
        ads_accounts = GoogleAds.load_ads_accounts(client)

        # Load all campaigns for all accounts
        return GoogleAds.load_ads_campaigns(client, ads_accounts)

    @staticmethod
    def load_ads_campaigns(client, accounts):

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

                campaigns = []
                accounts_campaigns[f'{manager_id}:{account}'] = campaigns

                for batch in response:
                    for row in batch.results:
                        campaigns.append(row.campaign.name)

        return accounts_campaigns

    @staticmethod
    def load_ads_accounts(client) -> Dict[int, list]:
        """Gets the account hierarchy of the given MCC and login customer ID.

            Args:
              client: The Google Ads client.
              login_customer_id: Optional manager account ID. If none provided, this
              method will instead list the accounts accessible from the
              authenticated Google Ads account.
            """

        # Gets instances of the GoogleAdsService and CustomerService clients.
        googleads_service = client.get_service("GoogleAdsService")
        customer_service = client.get_service("CustomerService")

        # Response
        ads_accounts = {}

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

        customer_resource_names = customer_service.list_accessible_customers().resource_names
        logging.info("Calling list accessible customers returned %s", customer_resource_names)

        for customer_resource_name in customer_resource_names:

            try:
                customer = customer_service.get_customer(resource_name=customer_resource_name)
            except Exception as e:
                continue

            if customer.manager:
                seed_customer_ids.append(customer.id)
            else:
                ads_accounts[customer.id] = [customer.id]

        logging.info("Ads Accounts not managers %s", ads_accounts)
        logging.info("Managers to process %s", seed_customer_ids)

        # Iterate through all directly accesible accounts
        while seed_customer_ids:

            customer_id = int(seed_customer_ids.pop(0))
            ads_accounts[customer_id] = []

            response = googleads_service.search(customer_id=str(customer_id), query=query)
            logging.info("Calling manager %s", customer_id)

            # Iterates over all rows in all pages to get all customer
            # clients under the specified customer's hierarchy.
            for googleads_row in response:

                customer_client = googleads_row.customer_client

                # The customer client that with level 0 is the specified
                # customer.
                if customer_client.level == 0:
                    continue

                logging.info("Found child %s", customer_client.id)
                if customer_client.id not in ads_accounts:
                    ads_accounts[customer_id].append(customer_client.id)

                if customer_client.manager:
                    # A customer can be managed by multiple managers, so to
                    # prevent visiting the same customer many times, we
                    # need to check if it's already in the Dictionary.
                    if customer_client.id not in ads_accounts and customer_client.level == 1:
                        logging.info("Child %s is also manager - added to process", customer_client.id)
                        seed_customer_ids.append(customer_client.id)

        return ads_accounts

