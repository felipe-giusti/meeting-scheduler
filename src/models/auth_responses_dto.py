from dataclasses import dataclass, field
from typing import Any


@dataclass
class ZoomDeviceResponse():
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int
    was_cached: bool = field(init=False) # TODO change later


@dataclass
class ZoomTokenResponse():
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int
    scope: Any
    was_cached: bool = field(init=False) # TODO change later
    
    def get_token(self):
        return self.access_token