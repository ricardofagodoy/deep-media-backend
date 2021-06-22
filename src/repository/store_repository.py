from abc import abstractmethod, ABC
from typing import List

from models.configuration import Configuration
from models.connector import Connector
from models.optimization import Optimization


class StoreRepository(ABC):

    @abstractmethod
    def persist_connector(self, connector: Connector, uid) -> Connector:
        raise NotImplementedError()

    @abstractmethod
    def load_connector(self, connector_type, uid) -> Connector:
        raise NotImplementedError()

    @abstractmethod
    def load_connectors(self, uid) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def delete_connector(self, connector_type, uid):
        raise NotImplementedError()

    @abstractmethod
    def persist_configuration(self, configuration: Configuration, uid) -> Configuration:
        raise NotImplementedError()

    @abstractmethod
    def load_configurations(self, uid) -> List[Configuration]:
        raise NotImplementedError()

    @abstractmethod
    def delete_configuration(self, configuration_id, uid):
        raise NotImplementedError()

    @abstractmethod
    def load_optimizations(self, uid, limit=None) -> List[Optimization]:
        raise NotImplementedError()
