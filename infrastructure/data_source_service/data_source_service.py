from abc import ABC, abstractmethod


class DataSourceService(ABC):
    @abstractmethod
    def get_data(self):
        pass


class ExternalDataSourceService(DataSourceService):
    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def gauge(self):
        pass

    @abstractmethod
    def basin(self):
        pass
