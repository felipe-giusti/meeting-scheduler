from abc import ABC, abstractmethod

class OAuth(ABC):
    
    def __init__(self, _client_id, _client_secret):
        self._client_id = _client_id
        self._client_secret = _client_secret
    
    @abstractmethod
    def get_device_code(self):
        pass
    
    @abstractmethod
    def verify_user(self):
        pass
    
    @abstractmethod
    def get_access_token(self):
        pass