from ports.meeting_port import Meeting
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential
import os, json, uuid
from msgraph import GraphServiceClient
from msgraph.generated.models.event import Event
from msgraph.generated.models.date_time_time_zone import DateTimeTimeZone
from msgraph.generated.models.patterned_recurrence import PatternedRecurrence
from msgraph.generated.models.recurrence_range import RecurrenceRange
from msgraph.generated.models.attendee import Attendee
from msgraph.generated.models.email_address import EmailAddress
from msgraph.generated.models.item_body import ItemBody
from msgraph.generated.models.body_type import BodyType
from msgraph.generated.models.online_meeting_provider_type import OnlineMeetingProviderType
from msgraph.generated.users.item.events.events_request_builder import EventsRequestBuilder
from models.course import Course


class TeamsMeeting(Meeting):
    # self._graph_client
    
    def authenticate(self):
        credential = InteractiveBrowserCredential(
            tenant_id=os.environ['AZURE_TENANT_ID'],
            client_id=os.environ['AZURE_CLIENT_ID'],)
            # redirect_uri='http://localhost:5000')

        self.credential = credential
        self._graph_client = GraphServiceClient(credential)
    
    
    async def create_meeting(self, course: Course):
        # Will only work for Student/Work account
        self.authenticate()
        
        request_body = Event(
            body = ItemBody(
                    content_type = BodyType.Html,
                    content = f"{course.course_name}1",
            ), 
            subject=f"{course.course_name}1",
            start=DateTimeTimeZone(#TODO use course class
                date_time="2023-10-02T8:00:00",
                time_zone="America/Sao_Paulo"
            ),
            end=DateTimeTimeZone(
                date_time="2023-10-02T10:00:00",
                time_zone="America/Sao_Paulo"
            ),
            recurrence=PatternedRecurrence(
                range=RecurrenceRange(
                    start_date="2023-10-02",
                    type="numbered",
                    number_of_occurrences=2
                )
            ),
            attendees = [
                Attendee(
                    email_address = EmailAddress(
                        address=email,
                        name=name,
                    )
                )
            for email, name in zip(course.participant_emails, course.participant_names)
            ],
            is_online_meeting = True,
	        online_meeting_provider = OnlineMeetingProviderType.TeamsForBusiness,
            transaction_id=uuid.uuid4()
        )
        
        request_configuration = EventsRequestBuilder.EventsRequestBuilderPostRequestConfiguration(
            headers = {
                    'Prefer' : "outlook.timezone=\"America/Sao_Paulo\"",
            })

        result = await self._graph_client.me.events.post(body=request_body, request_configuration=request_configuration)
        return result
    
    def get_particiants(self):
        pass
    
    def add_participants(self):
        pass
    
    def remove_participants(self):
        pass