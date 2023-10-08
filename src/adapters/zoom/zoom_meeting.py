import requests
from ports.meeting_port import Meeting


class ZoomMeeting(Meeting):
    
    def create_meeting(self, token):
        pass
    
    def get_user(self, token):
        resp = requests.get('https://api.zoom.us/v2/users/me',
                     headers={'Authorization': f'Bearer {token}'})
        return resp.json()