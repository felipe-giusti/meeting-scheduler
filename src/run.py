from use_cases.pdf_reader import PdfReader
import sys, pprint, time

from adapters.zoom.auth_zoom import ZoomOauth
from adapters.zoom.zoom_meeting import ZoomMeeting
from dotenv import load_dotenv
from exceptions import AuthException


load_dotenv()
args = sys.argv[1:]

filename = args[0]
reader = PdfReader(filename)

course = reader.get_data()

pprint.pprint(course.__dict__)
print(course.start_dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))

auth = ZoomOauth()

device_resp = auth.get_device_code()
print(f'device resp: {device_resp}')
auth.verify_user(device_resp)

token_resp = None
timeout = 30
timeout_start = time.time()
time.sleep(5)
while time.time() < timeout_start + timeout:
    try:
        time.sleep(device_resp.interval)
        token_resp = auth.get_access_token(device_resp)
        break
    except AuthException:
        pass

if token_resp is None:
    print('error getting token')
    raise Exception

print('TOKEN ============')
print(vars(token_resp))
print('==============')

zoom = ZoomMeeting()
meeting = zoom.create_meeting(token_resp.access_token, course)

pprint.pprint(meeting)
