import fitz
from enums.rects_enum import Rects
from models.course import Course


#TODO consider not using a class
class PdfReader:
    
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        
    def get_data(self):
        with fitz.open(self.file_path) as doc:
            page = doc[0]
            
            names = self.get_list(page, Rects.NAMES.value)
            emails = self.get_list(page, Rects.EMAILS.value)
            duration = self.get_value(page, Rects.DURATION.value)
            course_code = self.get_value(page, Rects.COURSE_CODE.value)
            course_name = self.get_value(page, Rects.COURSE_NAME.value)
            company_name = self.get_value(page, Rects.COMPANY_NAME.value)
            instructor_name = self.get_value(page, Rects.INSTRUCTOR_NAME.value)
            dates = self.get_list(page, Rects.DATES.value)
            
            return Course(participant_names=names, participant_emails=emails, course_code=course_code, 
                          course_name=course_name, company_name=company_name, instructor_name=instructor_name, 
                          duration_hours=duration, dates=dates)

                
    def get_value(self, page, rect):
        value_str = page.get_textbox(rect)
        return ''.join(s.strip() for s in value_str.splitlines()) # in case there are multiple lines
                
    def get_list(self, page, rect):
        values_str = page.get_textbox(rect)
        return [s.strip() for s in values_str.splitlines()]
        