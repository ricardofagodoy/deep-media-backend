from oauth2client.client import credentials_from_code
from connectors.base_connector import BaseConnector
from connectors.google.google_ads import GoogleAds
from connectors.google.google_analytics import GoogleAnalytics
from models.connector import Connector


class GoogleConnector(BaseConnector):
    TYPE = 'google'
    SCOPES = ['https://www.googleapis.com/auth/adwords',
              'https://www.googleapis.com/auth/analytics.readonly']

    def __init__(self, client_id, client_secret, developer_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.developer_token = developer_token

    @property
    def type(self):
        return GoogleConnector.TYPE

    def build_connector(self, connector_configuration):
        credentials = credentials_from_code(
            client_id=self.client_id,
            client_secret=self.client_secret,
            scope=GoogleConnector.SCOPES,
            code=connector_configuration['authorization_code'])

        configuration = {'refresh_token': credentials.refresh_token}
        options = self.load_options(configuration)

        return Connector(self.type, configuration, options)

    def load_options(self, connector_configuration):
        """
        Load all options fetched using this connector configurations.

        :returns Dictionary in the following format:

        {
            "ads_accounts": {
                "3013036305": [],
                "4413234797": [
                    "Website traffic-Search-1"
                ]
            },
            "ga_accounts": [{
                "111207543": {
                    'name': 'abc123',
                    'properties': {
                        "UA-111207543-1": [
                            { 'index': 1, 'name': 'abc' }
                            { 'index': 2, 'name': 'def' }
                        ]
                    }
                }
            }]
        }
        """

        # Load all Google Ads accounts and campaigns
        ads_properties = GoogleAds.load_ads_properties({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'developer_token': self.developer_token,
            'refresh_token': connector_configuration['refresh_token']
        })

        # Load all Google Analytics accounts, properties and metrics
        analytics_properties = GoogleAnalytics.load_accounts_properties({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': connector_configuration['refresh_token']
        })

        return {
            'ads_accounts': ads_properties,
            'ga_accounts': analytics_properties
        }
