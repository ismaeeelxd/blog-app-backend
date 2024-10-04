from abc import ABC, abstractmethod

class AbstractDatabase(ABC):
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def execute_query(self, query, params=None):
        pass
    
    @abstractmethod
    def fetch_all(self, query, params=None):
        pass
    
    @abstractmethod
    def fetch_one(self, query, params=None):
        pass
    
    @abstractmethod
    def create_record(self, model, **kwargs):
        pass
    @abstractmethod
    def update_record(self, model,filters=None, **kwargs):
        pass
