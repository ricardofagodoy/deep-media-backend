from abc import abstractmethod, ABC


class BaseConnector(ABC):

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError()

    @abstractmethod
    def load_options(self, connector_configuration):
        raise NotImplementedError()

    @abstractmethod
    def build_connector(self, connector_configuration):
        raise NotImplementedError()
