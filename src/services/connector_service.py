from typing import List
from connectors.base_connector import BaseConnector
from repository.DatastoreRepository import DatastoreRepository


class ConnectorService:

    def __init__(self, repository: DatastoreRepository, connectors: List[BaseConnector]):
        self.repository = repository
        self.connectors = {conn.type: conn for conn in connectors}

    def get_connector_options(self, connector_type, uid):

        connector_configuration = self.repository.load_connector(connector_type, uid)

        if not connector_configuration:
            return {}

        return self.__get_connector_by_type(connector_type).load_options(connector_configuration)

    def configure_connector(self, connector_type, configuration, uid):

        connector_configuration = self.__get_connector_by_type(connector_type).build_connector(configuration)

        return self.repository.persist_connector(connector_type, connector_configuration, uid)

    def get_user_connectors(self, uid):
        return self.repository.load_connectors(uid)

    def __get_connector_by_type(self, connector_type) -> BaseConnector:
        return self.connectors[connector_type]
