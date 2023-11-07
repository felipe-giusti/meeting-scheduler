import time, logging
from ports.oauth_port import OAuth
from ports.meeting_port import Meeting
from exceptions import AuthException
from utils import cache_utils
from enums.cache_keys import CacheKeys


log = logging.getLogger(__name__)

class MeetingScheduler():
    #self.token_resp
    
    def __init__(self, auth: OAuth, meeting: Meeting) -> None:
        self.auth = auth
        self.meeting = meeting
        
    def authenticate_client(self):
        device_resp = self.auth.get_device_code()

        if hasattr(device_resp, "was_cached") and device_resp.was_cached is False:
            self.auth.verify_user(device_resp)

        token_resp = self.auth.request_access_token(device_resp)

        if token_resp is None:
            print('error getting token - maximum retry timeout reached')
            raise Exception
        self.token_resp = token_resp
            
    def schedule_meeting(self, course):
        token = self.token_resp.get_token()
        resp = self.meeting.create_meeting(token, course)
        log.info(f'schedule meeting response: {resp}')
        return resp