import os
import re
from typing import Dict

import CONSTANTS

# parse the class timetable here first
proj_root_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
timetable_dir: str = os.path.join(proj_root_dir, "timetable")
class_timetable_dir: str = os.path.join(timetable_dir, "class")
class_timetables: str = sorted(os.listdir(class_timetable_dir))

latest_class_timetable = class_timetables[-1]

modules_json = dict()

with open(os.path.join(class_timetable_dir, latest_class_timetable), "r") as f:
    module_count = 0
    content = f.read()
    course_codes = re.findall(CONSTANTS.COURSE_CODE, content)
    course_titles = re.findall(CONSTANTS.COURSE_TITLE, content)
    course_remarks = re.findall(CONSTANTS.COURSE_REMARK, content)
    course_au = re.findall(CONSTANTS.COURSE_AU, content)

    #for i in range(len(course_au)):
    #    print(course_codes[i])
    #    print(course_titles[i])
    #    print(course_au[i])
    #    print("############################")

    print("Parsing Results")
    print("================================")
    print(f"Module Count : {len(course_codes)}")
    print(f"Title Count  : {len(course_titles)}")
    print(f"Remark Count : {len(course_remarks)}")
    print(f"AU Count     : {len(course_au)}")

# parse the class index here
with open(os.path.join(class_timetable_dir, latest_class_timetable), "r") as f:
    index = 0
    found_course = False
    for i in f:
        #if found_course and i != "</table>":

        #elif found_course and i == "</table>":
        #    found_course = False
        if index < len(course_codes) and re.search(course_codes[index], i):
            found_course = True
            index += 1
