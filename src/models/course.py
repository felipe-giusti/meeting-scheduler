from dataclasses import dataclass, field
from typing import List, Union
import datetime as dt
import logging

log = logging.getLogger('scheduler_log')

@dataclass
class Course:
    participant_names: List
    participant_emails: List
    course_code: str
    course_name: str
    company_name: str
    instructor_name: str
    duration_hours: Union[str, float]
    dates: List[str]
    _duration_hours: float = field(init=False, repr=False)
    _dates: List[dt.date] = field(init=False, repr=False)
    
    @property
    def duration_hours(self) -> float:
        return self._duration_hours
    
    @duration_hours.setter
    def duration_hours(self, value):
        if isinstance(value, str): # str example: "40:00"
            try:
                hours, minutes = value.split(':')
                value = float(hours) + float(minutes)/60
            except ValueError:
                log.error(f'Não foi possível converter a duração da reunião em horas - esperado HH:MM, recebido {value}')
        self._duration_hours = value
    
    
    @property
    def dates(self) -> List[dt.date]:
        return self._dates
    
    @dates.setter
    def dates(self, values: List[str]):
        dates = []
        for date in values:
            try:
                day, month = date.split('/')
                date = (dt.date(
                    year=dt.date.today().year,
                    month=int(month),
                    day=int(day)
                ))
                if date < dt.date.today():  # end of year / course can't be scheduled before creation
                    date = date.replace(year=date.year+1)
                    log.warning(f'Data do curso marcada para antes de hoje: alterando para {date.strftime("%d/%m/%Y")}')
                dates.append(date)
            except ValueError:
                log.error(f'Não foi possível converter a data do treinamento - esperado DD/MM, recebido {date}')
        self._dates = dates