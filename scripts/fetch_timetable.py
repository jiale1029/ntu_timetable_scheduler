# /bin/sh
"""
fetch_timetable
~~~~~~~~~~~~~~~~
This scripts fetches the class and exam timetable from
NTU's public server and save as a html file for
further parsing and processing.
"""

import logging
import os
from datetime import datetime as dt

import requests

CLASS_SCHEDULE_URL = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"
EXAM_SCHEDULE_URL = "https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.get_detail"

proj_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_dir = os.path.join(proj_root_dir, "logs")
timetable_dir = os.path.join(proj_root_dir, "timetable")
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(log_dir, "fetch_timetable.log"),
    format=FORMAT,
)
logger = logging.getLogger(__name__)

current_timestamp = str(dt.now())

try:
    logger.info("Fetching the class timetable from NTU's public server...")
    request_data = dict()
    request_data["r_search_type"] = "F"
    request_data["boption"] = "Search"
    request_data["acadsem"] = "2020;1"
    request_data["r_subj_code"] = ""
    request_data["staff_access"] = "false"
    resp = requests.post(url=CLASS_SCHEDULE_URL, data=request_data)
    with open(
        os.path.join(
            timetable_dir, "class", current_timestamp + "_class_timetable.html"
        ),
        "w",
    ) as f:
        f.write(resp.text)
except requests.RequestException as e:
    logger.critical(f"Failed to fetch timetable: {e}")
    raise
except Exception as e:
    logger.critical(f"Failed to fetch timetable: {e}")
    raise

try:
    logger.info("Fetching the exam timetable from NTU's public server...")
    request_data = dict()
    request_data["p_exam_dt"] = ""
    request_data["p_start_time"] = ""
    request_data["p_dept"] = ""
    request_data["p_subj"] = ""
    request_data["p_venue"] = ""
    request_data["p_matric"] = ""
    request_data["p_plan_no"] = "103"
    request_data["p_exam_yr"] = "2020"
    request_data["p_semester"] = "1"
    request_data["p_type"] = "UE"
    request_data["academic_session"] = "Semester 1 Academic Year 2020-2021"
    request_data["bOption"] = "Next"
    resp = requests.post(url=EXAM_SCHEDULE_URL, data=request_data)
    with open(
        os.path.join(timetable_dir, "exam", current_timestamp + "_exam_timetable.html"),
        "w",
    ) as f:
        f.write(resp.text)
except requests.RequestException as e:
    logger.critical(f"Failed to fetch timetable: {e}")
    raise
except Exception as e:
    logger.critical(f"Failed to fetch timetable: {e}")
    raise
