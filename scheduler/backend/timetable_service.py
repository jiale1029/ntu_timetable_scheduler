import os
import logging
import json
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

from scheduler.backend.constants import TIME_MAPPING, DAY_MAPPING


log_dir = os.path.join(os.path.dirname(os.path.abspath("timetable_service.py")), "logs")
FORMAT = "%(asctime)-15s : %(message)s"
logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(log_dir, "timetable_service.log"),
    format=FORMAT,
)
logger = logging.getLogger(__file__)


class TimetableService:

    class_timetable_matrix = np.zeros((32, 6), dtype=int)

    def __init__(self):
        self.class_timetables, self.exam_timetables = self.load_timetable()

    @staticmethod
    def load_timetable() -> Tuple[Dict]:
        """
        Load the json file that contains the
        class & exam timetable.
        """
        root_dir: str = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        class_json_path: str = os.path.join(
            root_dir, "timetable", "latest_class_timetable.json"
        )
        if not os.path.exists(class_json_path):
            raise FileNotFoundError(
                "The class timetable json file does not exist, please do indexing first."
            )
        with open(class_json_path, "r") as f:
            class_timetables: List[Dict] = json.load(f)
        exam_json_path: str = os.path.join(
            root_dir, "timetable", "latest_exam_timetable.json"
        )
        if not os.path.exists(exam_json_path):
            raise FileNotFoundError(
                "The exam timetable json file does not exist, please do indexing first."
            )
        with open(exam_json_path, "r") as f:
            exam_timetables: List[Dict] = json.load(f)
        return class_timetables, exam_timetables

    def parse_time(self, time_range: str) -> List[int]:
        """
        Convert the time to coordinates on a matrix
        """
        time_ranges: List = time_range.strip(" ").split("-")
        start, end = time_ranges[0], time_ranges[1]

        return [time for time in range(TIME_MAPPING[start], TIME_MAPPING[end])]

    def parse_day(self, day: str) -> int:
        """
        Convert the day to coordinates on a matrix
        """
        return DAY_MAPPING[day]

    def parse_remark(self, remarks: str) -> str:
        return remarks

    def parse_day_time(self, time_range: str, day: str) -> List[Tuple[int]]:
        times: List[int] = self.parse_time(time_range)
        day: int = self.parse_day(day)
        return [(time, day) for time in times]

    def parse_duration(self, duration: str) -> int:
        """
        Return the duration in minute.
        <2hr30min>
        """
        hour: int = 0
        minute: int = 0

        duration = duration.lower()
        if "hr" in duration:
            hour = int(duration.split("hr")[0])
        if "min" in duration and "hr" in duration:
            minute = int(duration.split("hr")[1].split("min")[0])
        elif "hr" not in duration and "min" in duration:
            minute = int(duration.split("min")[0])

        minutes = hour * 60 + minute
        return minutes

    def generate_class_timetable(self, course_codes: List) -> List[Dict]:
        """
        Use the course codes to retrieve all the possible indexes,
        generate all possible configuration for every courses.
        During the generation process, check if there's a clash
        in the newly added index, if there is one, stop and try next.
        """
        course_added = []
        for course_code in course_codes:
            course = self.class_timetables[course_code]
            for indexes in course["Indexes"]:
                pass

        return None

    def generate_exam_timetable(self, course_codes: List) -> Dict:
        """
        Each course has only one exam schedule, line them up
        and check if their timing clashes.
        """
        date_mapping = {}
        exam_timetable_dict = {}
        for course_code in course_codes:
            logger.info(f"Generating exam timetable for {course_code}")
            try:
                if course_code not in self.exam_timetables:
                    exam_timetable_dict[course_code] = {}
                    continue
                exam_info = self.exam_timetables[course_code]
                # parse the date, time and duration here into datetime object
                date = exam_info["Date"].replace(" ", "")
                time = exam_info["Time"].replace(" ", "")
                duration = exam_info["Duration"].replace(" ", "")
                duration_minute = self.parse_duration(duration)
                start_exam_datetime = datetime.strptime(date + "T" + time, "%d%B%YT%I.%M%p")
                end_exam_datetime = start_exam_datetime + timedelta(minutes=duration_minute)
                # date mapping stores a list of exam's time in each day
                if date not in date_mapping:
                    date_mapping[date] = []
                date_mapping[date].append((start_exam_datetime, end_exam_datetime))
                # check if the schedule on that day has any clashes
                if self.check_exam_clash(date_mapping[date]):
                    return {}
                info = dict(
                    start=start_exam_datetime,
                    end=end_exam_datetime,
                    duration=duration,
                    title=exam_info.get("Title", "")
                )
                exam_timetable_dict[course_code] = info
            except Exception as e:
                logger.error(f"Failed to generate exam timetable: {e}")

        return exam_timetable_dict

    def check_exam_clash(self, time_list: List[Tuple]) -> bool:
        """
        Check if the exams overlap each other in one single day.
        """
        sorted_time_list = sorted(time_list, key=lambda x: x[0])
        sorted_time_list = sorted(time_list, key=lambda x: x[1])
        if len(sorted_time_list) <= 1:
            return False
        max_low = sorted_time_list[0]
        # check one by one if there's an overlap
        for time in sorted_time_list[1:]:
            if max(max_low[0], time[0]) < min(max_low[1], time[1]):
                return True
            else:
                max_low = time
        return False

    def check_class_clash(self, timetable_matrix) -> bool:
        """
        Check if there's a conflict in the index.
        """
        timetable_clashes = timetable_matrix >= 2
        return timetable_clashes.any()
