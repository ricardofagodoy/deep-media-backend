from abc import abstractmethod, ABC
from datetime import datetime

from models.configuration import Configuration


class BaseConnector(ABC):

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError()

    @abstractmethod
    def build_connector(self, connector_configuration):
        raise NotImplementedError()

    @abstractmethod
    def load_options(self, connector_configuration):
        raise NotImplementedError()