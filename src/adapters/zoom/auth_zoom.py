import requests, os, logging, time
import webbrowser
from ports.oauth_port import OAuth
from models.auth_responses_dto import ZoomDeviceResponse, ZoomTokenResponse
from exceptions import AuthException


log = logging.getLogger(__name__)

class ZoomOauth(OAuth):
    
    def __init__(self) -> None:
        super().__init__(
            _client_id=os.environ['ZOOM_CLIENT_ID'],
            _client_secret=os.environ['ZOOM_CLIENT_SECRET']
        )
        
    
    def get_device_code(self) -> ZoomDeviceResponse:
        response = requests.post(
            'https://zoom.us/oauth/devicecode',
            data={"grant_type": "device_code",
                  'client_id': self._client_id},
            auth=(self._client_id, self._client_secret),
        )
        resp_json = response.json()
        
        if response.status_code != 200:
            log.error(f'Error while requesting device code: {response.status_code} - {resp_json}')
            raise AuthException
        
        #TODO implement expiration
        return ZoomDeviceResponse(**resp_json)
    
    def verify_user(self, device_resp):
        log.info('Opening browser, verify')
        # time.sleep(device_resp.interval)
        webbrowser.open(device_resp.verification_uri_complete, new=2)
        return 

    def get_access_token(self, device_resp: ZoomDeviceResponse):
        response = requests.post(
            'https://zoom.us/oauth/token',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            auth=(self._client_id, self._client_secret),
            data={'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
                  'device_code': device_resp.device_code}
        )
        resp_json = response.json()
        
        if response.status_code != 200:
            log.error(f'Error while requesting access token: {response.status_code} - {resp_json}')
            raise AuthException
        
        #TODO implement expiration / cache
        return ZoomTokenResponse(**resp_json)
    