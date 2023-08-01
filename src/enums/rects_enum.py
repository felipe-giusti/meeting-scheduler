from enum import Enum

class Rects(Enum):
    NAMES = (198, 590, 600, 784)
    EMAILS = (198, 380, 600, 581)
    DURATION = (93, 90, 114, 161)
    COURSE_CODE = (65, 50, 88, 145)
    COURSE_NAME = (65, 245, 88, 742)
    COMPANY_NAME = (90, 245, 115, 764)
    INSTRUCTOR_NAME = (118, 245, 135, 767)
    
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1