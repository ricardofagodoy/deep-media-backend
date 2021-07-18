from google.ads.googleads.errors import GoogleAdsException
from googleapiclient.errors import HttpError
from oauth2client.client import credentials_from_code
from connectors.base_connector import BaseConnector
from connectors.google.google_ads import GoogleAds
from connectors.google.google_analytics import GoogleAnalytics
from models.connector import Connector
from services.MessageException import MessageException


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
        """
        try:
            # Load all Google Ads accounts and campaigns
            ads_properties = GoogleAds.load_ads_properties({
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'developer_token': self.developer_token,
                'refresh_token': connector_configuration['refresh_token']
            })

            # Load all Google Analytics accounts, properties and metrics
            ga_properties, ga_fields = GoogleAnalytics.load_accounts_properties({
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'refresh_token': connector_configuration['refresh_token']
            })

        except HttpError as http_error:
            raise MessageException(', '.join([error.get('message') for error in http_error.error_details]))
        except GoogleAdsException as ads_error:
            raise MessageException(', '.join([error.message for error in ads_error.failure.errors]))

        return {
            'ads_accounts': ads_properties,
            'ga_accounts': ga_properties,
            'ga_fields': ga_fields
        }
