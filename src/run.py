from services.pdf_reader import PdfReader
import sys, pprint, time

from adapters.zoom.auth_zoom import ZoomOauth
from adapters.zoom.zoom_meeting import ZoomMeeting
from dotenv import load_dotenv
from exceptions import AuthException
from services.meeting_scheduler import MeetingScheduler
from utils import cache_utils


load_dotenv()
args = sys.argv[1:]

filename = args[0]
reader = PdfReader(filename)

course = reader.get_data()

# pprint.pprint(course.__dict__)
# print(course.start_dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"))

for i in range(2): # testing caching

    print('==================')
    print(f'Starting {i}')
    scheduler = MeetingScheduler(ZoomOauth(), ZoomMeeting())
    scheduler.authenticate_client()

    meeting = scheduler.schedule_meeting(course)
    print(meeting)

    pprint.pprint(meeting)

    print(f'end {i}')
    print('======================')
    time.sleep(5)