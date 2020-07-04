import os
import json
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

from scheduler.backend.constants import TIME_MAPPING, DAY_MAPPING

class TimetableService:

    class_timetable_matrix = np.zeros((32,6), dtype=int)

    def __init__(self):
        self.class_timetables, self.exam_timetables = self.load_timetable()

    @staticmethod
    def load_timetable() -> Tuple[Dict]:
        """
        Load the json file that contains the
        class & exam timetable.
        """
        root_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        class_json_path: str = os.path.join(root_dir, "timetable", "latest_class_timetable.json")
        if not os.path.exists(class_json_path):
            raise FileNotFoundError(
                "The class timetable json file does not exist, please do indexing first."
            )
        with open(class_json_path, "r") as f:
            class_timetables: List[Dict] = json.load(f)
        exam_json_path: str = os.path.join(root_dir, "timetable", "latest_exam_timetable.json")
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

        minutes = hour*60 + minute
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
            course = self.class_timetables[course_codes]
            for indexes in course["indexes"]:
                pass

        return None

    def generate_exam_timetable(self, course_codes: List) -> List[Dict]:
        """
        Each course has only one exam schedule, line them up
        and check if their timing clashes.
        """
        exam_timetable_dict = {}
        for course_code in course_codes:
            if course_code not in self.exam_timetables:
                continue
            exam_info = self.exam_timetables[course_code]
            date = exam_info["Date"].replace(" ", "")
            time = exam_info["Time"].replace(" ", "")
            duration = exam_info["Duration"].replace(" ", "")
            duration_minute = self.parse_duration(duration)
            start_exam_datetime = datetime.strptime(date+"T"+time, "%d%B%YT%H.%M%p")
            end_exam_datetime = start_exam_datetime + timedelta(minutes=duration_minute)
            if date not in exam_timetable_dict:
                exam_timetable_dict[date] = []
            exam_timetable_dict[date].append((start_exam_datetime, end_exam_datetime))
            if self.check_exam_clash(exam_timetable_dict):
                return False

        return exam_timetable_dict

    def check_exam_clash(self, exam_timetable: Dict) -> bool:
        for date in exam_timetable:
            low = 0
            for time in exam_timetable[date]:
                print(time)
        return False

    def check_class_clash(self, timetable_matrix) -> bool:
        """
        Check if there's a conflict in the index.
        """
        timetable_clashes = timetable_matrix >= 2
        return timetable_clashes.any()
