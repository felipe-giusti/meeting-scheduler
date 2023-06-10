from abc import ABC, abstractmethod


class Meeting(ABC):
    
    @abstractmethod
    def authenticate(self):
        pass
    
    @abstractmethod
    def create_meeting(self):
        pass
    
    @abstractmethod
    def get_particiants(self):
        pass
    
    @abstractmethod
    def add_participants(self):
        pass
    
    @abstractmethod
    def remove_participants(self):
        pass
    
    # validate -- change 
    # def edit_meeting(self):
    #     pass
    
    # validate
    # def send_custom_notification(self):
    #     pass