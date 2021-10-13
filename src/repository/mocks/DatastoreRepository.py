import uuid
from datetime import datetime, timedelta
from typing import List
from connectors.mocks.google_connector import GOOGLE_MOCK_CONNECTOR_OPTIONS
from models.configuration import Configuration
from models.connector import Connector
from models.optimization import Optimization
from models.tick import Tick
from repository.store_repository import StoreRepository

_OPTIMIZATIONS_STORE = 'optimizations'
_CONNECTORS_STORE = 'connectors'
_CONFIGURATION_STORE = 'configurations'
_TICKS_STORE = 'ticks'

# Memory ephemeral database
database = {
    _OPTIMIZATIONS_STORE: {},
    _CONNECTORS_STORE: {
        'uid': {
            'google': Connector('google', '', GOOGLE_MOCK_CONNECTOR_OPTIONS).to_dict()
        }
    },
    _CONFIGURATION_STORE: {
        'uid': {
            'd4826d41f1da4c18a52069881c97a2ee': {
                'ga_metric': 'ga:transactionRevenue',
                'active': True,
                'ads_campaign': 'Garrafa',
                'type': 'google',
                'ga_account': '122489030',
                'name': 'Tester',
                'ga_property': 'UA-122489030-1',
                'ga_profile': '178643400',
                'adcost_target': 10,
                'ga_dimension': 'ga:campaign',
                'id': 'd4826d41f1da4c18a52069881c97a2ee',
                'ads_account': '8752511022:8752511022'
            }
        }
    },
    _TICKS_STORE: {
        'uid': [
            Tick(datetime.now() - timedelta(minutes=45), 10, 10).to_dict(),
            Tick(datetime.now() - timedelta(minutes=30), 10, 16).to_dict(),
            Tick(datetime.now(), 10, 7).to_dict()
        ]
    }
}


class DatastoreRepository(StoreRepository):

    def persist_connector(self, connector: Connector, uid) -> Connector:

        connectors = database[_CONNECTORS_STORE].get(uid, {})
        connectors[connector.type] = connector.to_dict()

        return connector

    def load_connectors(self, uid) -> List[str]:

        connectors = database[_CONNECTORS_STORE].get(uid, {})

        return list(connectors.keys())

    def load_connector(self, connector_type, uid):

        connectors = database[_CONNECTORS_STORE].get(uid, {})

        return Connector.from_dict(connectors.get(connector_type))

    def delete_connector(self, connector_type, uid):
        del database[_CONNECTORS_STORE][uid][connector_type]

    def persist_configuration(self, configuration: Configuration, uid):

        # New configuration
        if not configuration.id:
            configuration.id = uuid.uuid4().hex

        database[_CONFIGURATION_STORE][uid][configuration.id] = configuration.to_dict()

        return configuration

    def load_configurations(self, uid) -> List[Configuration]:
        configs = database[_CONFIGURATION_STORE].get(uid, {})

        return [Configuration.from_dict(conf) for conf in configs.values()]

    def delete_configuration(self, configuration_id, uid):
        del database[_CONFIGURATION_STORE][uid][configuration_id]

    def load_optimizations(self,
                           uid,
                           start_date: datetime = None,
                           end_date: datetime = None,
                           configuration_id=None,
                           limit=60) -> List[Optimization]:

        opts = database[_OPTIMIZATIONS_STORE].get(uid, [])

        if configuration_id:
            opts = [opt for opt in opts if opt.campaign_id == configuration_id]

        if start_date:
            opts = [opt for opt in opts if opt.date >= start_date]

        if end_date:
            opts = [opt for opt in opts if opt.date <= end_date]

        return [Optimization.from_dict(opt) for opt in opts]

    def load_ticks(self, uid,
                   configuration_id: str,
                   start_date: datetime = None,
                   end_date: datetime = None,
                   limit=60) -> List[Tick]:

        ticks = database[_TICKS_STORE].get(uid, [])

        return [Tick.from_dict(tick) for tick in ticks]
