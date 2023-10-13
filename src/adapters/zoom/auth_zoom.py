import requests, os, logging, time
import webbrowser
from ports.oauth_port import OAuth
from models.auth_responses_dto import ZoomDeviceResponse, ZoomTokenResponse
from exceptions import AuthException
from utils import cache_utils
from enums.cache_keys import CacheKeys
# import cachetools


cache = cache_utils.load_pickle(reset=True)

log = logging.getLogger(__name__)

class ZoomOauth(OAuth):
    
    def __init__(self) -> None:
        super().__init__(
            _client_id=os.environ['ZOOM_CLIENT_ID'],
            _client_secret=os.environ['ZOOM_CLIENT_SECRET']
        )
    
    
    @cache_utils.cached(cache, str(CacheKeys.ZOOM_DEVICE))
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
        
        device = ZoomDeviceResponse(**resp_json)
        return device, device.expires_in
    
    def verify_user(self, device_resp: ZoomDeviceResponse):
        log.info('Opening browser, verify')
        # time.sleep(device_resp.interval)
        webbrowser.open(device_resp.verification_uri_complete, new=2)
        return 

    @cache_utils.cached(cache, str(CacheKeys.ZOOM_TOKEN))
    def _get_access_token(self, device_resp: ZoomDeviceResponse):
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
        
        token_resp = ZoomTokenResponse(**resp_json)
        return token_resp, token_resp.expires_in
    
    def request_access_token(self, device_resp, timeout=30, interval=5):
        token_resp = None
        
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            try:
                time.sleep(interval)
                token_resp = self._get_access_token(device_resp)
                break
            except AuthException:
                pass
        return token_resp
    