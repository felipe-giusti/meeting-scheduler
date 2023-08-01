from dataclasses import dataclass
from typing import List, Union
from datetime import time

@dataclass
class Course:
    participant_names: List
    participant_emails: List
    duration: Union[str, time]
    course_code: str
    course_name: str
    company_name: str
    instructor_name: str
