from use_cases.pdf_reader import PdfReader
import sys, pprint
from adapters.teams_meeting import TeamsMeeting
from dotenv import load_dotenv
import asyncio


load_dotenv()

async def r():
    args = sys.argv[1:]

    filename = args[0]
    reader = PdfReader(filename)

    course = reader.get_data()

    pprint.pprint(course.__dict__)
    # print(course.course_name)

    meeting = TeamsMeeting()
    # meeting.authenticate()

    res = await meeting.create_meeting(course)

    print(res)
    print('\n\n')
    pprint.pprint(vars(res))

if __name__ == '__main__':
    asyncio.run(r())
