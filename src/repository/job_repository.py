from abc import abstractmethod, ABC


class JobRepository(ABC):

    @abstractmethod
    def get_scheduled_optimizations(self, uid):
        raise NotImplementedError()

    @abstractmethod
    def schedule_optimization(self, connector_type: str, uid):
        raise NotImplementedError()

    @abstractmethod
    def delete_scheduled_optimization(self, connector_type: str, uid):
        raise NotImplementedError()
