from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleAnalytics:

    @staticmethod
    def load_accounts_properties(credentials):

        analytics_properties = dict()

        # Construct service
        service = build('analytics', 'v3', credentials=Credentials(
            **credentials,
            token_uri='https://oauth2.googleapis.com/token',
            token=''
        ))

        # Get a list of all Google Analytics accounts for this user
        accounts = service.management().accounts().list().execute()

        if accounts.get('items'):
            for account in accounts.get('items'):

                account_id = account.get('id')

                # To store response
                properties_map = dict()
                analytics_properties[account_id] = properties_map

                # Get a list of all the properties for the account
                properties = service.management().webproperties().list(
                    accountId=account_id).execute()

                if properties.get('items'):
                    for property in properties.get('items'):

                        property_id = property.get('id')

                        # To store response
                        custom_metrics_list = []
                        properties_map[property_id] = custom_metrics_list

                        # Get a list of all custom metrics for this property
                        custom_metrics = service.management().customMetrics().list(
                            accountId=account_id,
                            webPropertyId=property_id).execute()

                        if custom_metrics.get('items'):
                            custom_metrics_list.extend([e.get('index') for e in custom_metrics.get('items')])

        return analytics_properties
