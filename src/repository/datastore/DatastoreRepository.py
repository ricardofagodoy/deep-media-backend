import uuid
from datetime import datetime
from typing import List
from google.cloud import datastore
from models.configuration import Configuration
from models.connector import Connector
from models.optimization import Optimization
from models.tick import Tick
from repository.store_repository import StoreRepository

_OPTIMIZATIONS_STORE = 'optimizations'
_CONNECTORS_STORE = 'connectors'
_CONFIGURATION_STORE = 'configurations'
_TICKS_STORE = 'ticks'


class DatastoreRepository(StoreRepository):

    def __init__(self):
        self.client = datastore.Client()

    def persist_connector(self, connector: Connector, uid) -> Connector:

        entity = datastore.Entity(self.client.key('User', uid, _CONNECTORS_STORE, connector.type))
        entity.update(connector.to_dict())

        self.client.put(entity)

        return connector

    def load_connectors(self, uid) -> List[str]:

        query = self.client.query(ancestor=self.client.key('User', uid), kind=_CONNECTORS_STORE)
        query.keys_only()

        return [conn.key.name for conn in query.fetch()]

    def load_connector(self, connector_type, uid):
        entity = self.client.get(self.client.key('User', uid, _CONNECTORS_STORE, connector_type))
        return Connector.from_dict(entity)

    def delete_connector(self, connector_type, uid):
        self.client.delete(self.client.key('User', uid, _CONNECTORS_STORE, connector_type))

    def persist_configuration(self, configuration: Configuration, uid):

        # New configuration
        if not configuration.id:
            configuration.id = uuid.uuid4().hex

        entity = datastore.Entity(self.client.key('User', uid, _CONFIGURATION_STORE, configuration.id))
        entity.update(configuration.to_dict())

        self.client.put(entity)

        return configuration

    def load_configurations(self, uid) -> List[Configuration]:
        query = self.client.query(ancestor=self.client.key('User', uid), kind=_CONFIGURATION_STORE)
        return [Configuration.from_dict(conf) for conf in query.fetch()]

    def delete_configuration(self, configuration_id, uid):
        self.client.delete(self.client.key('User', uid, _CONFIGURATION_STORE, configuration_id))

    def load_optimizations(self,
                           uid,
                           start_date: datetime = None,
                           end_date: datetime = None,
                           configuration_id=None,
                           limit=60) -> List[Optimization]:

        query = self.client.query(ancestor=self.client.key('User', uid), kind=_OPTIMIZATIONS_STORE)

        if configuration_id:
            query.add_filter('campaign_id', '=', configuration_id)

        if start_date:
            query.add_filter('date', '>=', start_date)

        if end_date:
            query.add_filter('date', '<=', end_date)

        query.order = ["-date"]

        return [Optimization.from_dict(optm) for optm in query.fetch(limit=limit)]

    def load_ticks(self, uid,
                   configuration_id: str,
                   start_date: datetime = None,
                   end_date: datetime = None,
                   limit=60) -> List[Tick]:

        query = self.client.query(
            ancestor=self.client.key('User', uid, _CONFIGURATION_STORE, configuration_id),
            kind=_TICKS_STORE)

        if start_date:
            query.add_filter('date', '>=', start_date)

        if end_date:
            query.add_filter('date', '<=', end_date)

        query.order = ["-date"]

        return [Tick.from_dict(tick) for tick in query.fetch(limit=limit)]
