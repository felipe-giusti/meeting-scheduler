from use_cases.pdf_reader import PdfReader
import sys, pprint


args = sys.argv[1:]

filename = args[0]
reader = PdfReader(filename)

course = reader.get_data()

# pprint.pprint(course.__dict__)
print(course.course_name)
