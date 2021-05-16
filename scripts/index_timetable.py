"""
index_timetable
~~~~~~~~~~~~~~~~
Parses the html retrieved from NTU's public server and
save them as json file for easy processing.

"""
import json
import os
import re
import time
from typing import Dict, List

import pandas as pd

import constants

# parse the class timetable here first
start = time.time()
proj_root_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
timetable_dir: str = os.path.join(proj_root_dir, "timetable")
class_timetable_dir: str = os.path.join(timetable_dir, "class")
class_timetables: str = sorted(os.listdir(class_timetable_dir))

exam_timetable_dir: str = os.path.join(timetable_dir, "exam")
exam_timetables: str = sorted(os.listdir(exam_timetable_dir))

latest_class_timetable = class_timetables[-1]
latest_exam_timetable = exam_timetables[-1]

modules_json = dict()


def parse_course_code(course_code: str) -> str:
    course_code = course_code.replace('<TD WIDTH="100"><B><FONT COLOR=#0000FF>', "")
    course_code = course_code.replace("</FONT></B></TD>", "")
    return course_code


def parse_course_title(course_title: str) -> str:
    course_title = course_title.replace('<TD WIDTH="500"><B><FONT COLOR=#0000FF>', "")
    course_title = course_title.replace("</FONT></B></TD>", "")
    return course_title


def parse_course_au(course_au: str) -> str:
    course_au = course_au.replace('<TD WIDTH="50"><B><FONT COLOR=#0000FF>', "")
    course_au = course_au.replace("</FONT></B></TD>", "")
    return course_au.strip(" ")


def parse_course_remark(course_remark: str) -> str:
    course_remark = course_remark.replace(
        '<TD WIDTH="500"><B><FONT SIZE=2 COLOR=#FF00FF>', ""
    )
    course_remark = course_remark.replace("</FONT></B></TD>", "")
    return course_remark


def parse_index(indexes: List) -> List[Dict]:
    parse_indexes = []
    for index in indexes:
        for ci in re.split("</tr>", index)[1:-1]:
            for idx, content in enumerate(ci.split("\n")[2:-1]):
                content = content.replace("<td><b>", "").replace("</b></td>", "")
                content = content.replace("&nbsp;", "").replace("<td></td>", "")
                if idx == 0 and content == "":  # If no index, group with previous index
                    parse_indexes[-1]["Info"].append({})
                    continue
                if idx == 0:  # Index Number, add a new index element
                    index_template = {"Index": "", "Info": []}
                    parse_indexes.append(index_template)
                    parse_indexes[-1]["Index"] = content
                    parse_indexes[-1]["Info"] = [{}]
                if idx == 1:
                    parse_indexes[-1]["Info"][-1]["Type"] = content
                elif idx == 2:
                    parse_indexes[-1]["Info"][-1]["Group"] = content
                elif idx == 3:
                    parse_indexes[-1]["Info"][-1]["Day"] = content
                elif idx == 4:
                    parse_indexes[-1]["Info"][-1]["Time"] = content
                elif idx == 5:
                    parse_indexes[-1]["Info"][-1]["Venue"] = content
                elif idx == 6:
                    parse_indexes[-1]["Info"][-1]["Remark"] = content
    return parse_indexes


with open(os.path.join(class_timetable_dir, latest_class_timetable), "r") as f:
    module_count = 0
    content = f.read()
    course_codes = re.findall(constants.COURSE_CODE, content)
    course_titles = re.findall(constants.COURSE_TITLE, content)
    course_remarks = re.findall(constants.COURSE_REMARK, content)
    course_aus = re.findall(constants.COURSE_AU, content)


# parse the class index here
courses = re.split(r"<\/table>\n<P><HR>", content)[:-1]
cleaned_course_codes = [parse_course_code(x) for x in course_codes]
cleaned_course_titles = [parse_course_title(x) for x in course_titles]
cleaned_course_aus = [parse_course_au(x) for x in course_aus]
cleaned_course_remarks = [parse_course_remark(x) for x in course_remarks]
course_index_mapping = dict()
for idx, course in enumerate(courses):
    course_code = cleaned_course_codes[idx]
    print(f"Indexing course: {course_code}")
    course_index_mapping[course_code] = dict()
    course_index_mapping[course_code]["Code"] = course_code
    course_index_mapping[course_code]["Title"] = cleaned_course_titles[idx]
    index_contents = re.split("<table  border>", course)[1:]
    course_index_mapping[course_code]["Indexes"] = parse_index(index_contents)
    course_index_mapping[course_code]["AU"] = cleaned_course_aus[idx]

with open(os.path.join(timetable_dir, "latest_class_timetable.json"), "w") as file:
    file.write(json.dumps(course_index_mapping))
print("Course Dumping completed...")
with open(os.path.join(exam_timetable_dir, latest_exam_timetable), "r") as f:
    content = f.read()
    contents = re.split("<BR>\n<BR>\n<BR>\n", content)
    dfs = pd.read_html(contents[0])
    df = dfs[2]
    exam_course_mapping = dict()
    for idx in range(len(df)):
        code = df[3][idx]
        print(f"Indexing exam: {code}")
        if code not in course_index_mapping:
            continue
        exam_course_mapping[code] = dict()
        exam_course_mapping[code]["Date"] = df[0][idx]
        exam_course_mapping[code]["Day"] = df[1][idx]
        exam_course_mapping[code]["Time"] = df[2][idx]
        exam_course_mapping[code]["Title"] = df[4][idx]
        exam_course_mapping[code]["Duration"] = df[5][idx]

with open(os.path.join(timetable_dir, "latest_exam_timetable.json"), "w") as f:
    f.write(json.dumps(exam_course_mapping))

print("Parsing Results")
print("================================")
print(f"Module Count : {len(course_codes)}")
print(f"Title Count  : {len(course_titles)}")
print(f"Exam Count   : {len(exam_course_mapping)}")
print(f"Remark Count : {len(course_remarks)}")
print(f"AU Count     : {len(course_aus)}")
print(f"Time taken   : {time.time()-start}")
