import requests, json, logging
from ports.meeting_port import Meeting
from models.course import Course


log = logging.getLogger(__name__)

class ZoomMeeting(Meeting):
    
    def create_meeting(self, token, course: Course):
        
        meeting_body = {
            "agenda": f'[Treinamento] {course.course_name}',
            "recurrence": {
                "end_date_time": course.end_dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "type": 1,
            },
            "settings": {
                
                "calendar_type": 2, #TODO consider later
                "email_notification": True,

                "meeting_invitees": [
                {
                    "email": email
                }
                for email in course.participant_emails
                ],

                # "private_meeting": False,
                "registrants_confirmation_email": True,
                # "registrants_email_notification": True,
                
                # "continuous_meeting_chat": {
                # "enable": True,
                # "auto_add_invited_external_users": True
                # },
            },
            "start_time": course.start_dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            # "template_id": "Dv4YdINdTk+Z5RToadh5ug==",
            "timezone": "America/Sao_Paulo",
            "topic": f'[Treinamento] {course.course_name}',
            "type": 8
            }
        
        json_body = json.dumps(meeting_body)
        resp = requests.post('https://api.zoom.us/v2/users/me/meetings',
                             data=json_body,
                             headers={'Authorization': f'Bearer {token}'})
        resp_json = resp.json()
        
        if resp.status_code != 201:
            log.error(f'Error while creating zoom meeting: {resp.status_code} - {resp_json}')
            
        return resp_json
    
    def get_user(self, token):
        resp = requests.get('https://api.zoom.us/v2/users/me',
                     headers={'Authorization': f'Bearer {token}'})
        return resp.json()