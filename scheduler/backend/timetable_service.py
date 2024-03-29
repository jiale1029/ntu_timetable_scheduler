import json
import logging
import os
from copy import deepcopy
from datetime import datetime, timedelta
from pprint import pprint
from typing import Dict, List, Tuple

import numpy as np

from scheduler.backend.constants import (
    COMMUNICATION_COURSES,
    DAY_MAPPING,
    ONLINE_GENERAL_COURSES,
    TIME_MAPPING,
)

log_dir = os.path.join(os.path.dirname(os.path.abspath("timetable_service.py")), "logs")
FORMAT = "%(asctime)-15s : %(message)s"

logger = logging.getLogger(__file__)
file_handler = logging.FileHandler(os.path.join(log_dir, "timetable_service.log"))
formatter = logging.Formatter(FORMAT)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class TimetableService:
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
                "The class timetable json file does "
                "not exist, please do indexing first."
            )
        with open(class_json_path, "r") as f:
            class_timetables: List[Dict] = json.load(f)
        exam_timetables = {}
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

    @staticmethod
    def parse_time(time_range: str) -> List[int]:
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

    @staticmethod
    def parse_remark(remarks: str) -> str:
        """
        Convert remarks to weeks
        """
        splitted_weeks = []
        if "-" in remarks:
            # range
            week_range = remarks.split("Wk")[1].split("-")
            splitted_weeks = [
                j for j in range(int(week_range[0]), int(week_range[-1]) + 1, 1)
            ]
        elif "," in remarks:
            splitted_weeks = remarks.split("Wk")[1].split(",")
            splitted_weeks = [int(j) for j in splitted_weeks]

        return splitted_weeks

    def parse_day_time(self, time_range: str, day: str) -> List[Tuple[int]]:
        """
        Parses the day time into coordinates in Tuple.
        """
        if not time_range or not day:
            return []
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

    def add_index(self, class_timetable_matrix, index_infos: Dict):
        weeks = [i for i in range(1, 14)]
        for index_info in index_infos:
            coordinates = self.parse_day_time(index_info["Time"], index_info["Day"])
            remarks = index_info["Remark"]
            if remarks:
                parsed_remarks = self.parse_remark(remarks)
                weeks = parsed_remarks
            for week in weeks:
                for coord in coordinates:
                    class_timetable_matrix[week][coord] += 1
        return class_timetable_matrix

    def remove_index(self, class_timetable_matrix, index_infos: Dict):
        weeks = [i for i in range(1, 14)]
        for index_info in index_infos:
            coordinates = self.parse_day_time(index_info["Time"], index_info["Day"])
            remarks = index_info["Remark"]
            if remarks:
                parsed_remarks = self.parse_remark(remarks)
                weeks = parsed_remarks
            for week in weeks:
                for coord in coordinates:
                    class_timetable_matrix[week][coord] -= 1

        return class_timetable_matrix

    def filter_online_courses(self, course_codes: List[str]):
        """
        Filter out the online courses.
        """
        return [cc for cc in course_codes if cc not in ONLINE_GENERAL_COURSES]

    def filter_by_group(self, indexes: List[Dict], group: str):
        """
        Filter the indexes based on group.
        Only filter communication courses.
        """
        filtered = []

        if group == "": # if no group specified, return all indexes
            return indexes

        for index in indexes:
            infos = index["Info"]
            for info in infos:
                # if info["Group"][0] == "A" or info["Group"][0] == "B":
                #     continue
                if group.upper() not in info["Group"]: # break does not run the else statement, so if doesn't match then you don't add
                    break
            else:
                filtered.append(index)

        return filtered

    def generate_class_timetable(
        self, course_codes: List, user_group: str
    ) -> List[Dict]:
        """
        Use the course codes to retrieve all the possible indexes,
        generate all possible configuration for every courses.
        During the generation process, check if there's a clash
        in the newly added index, if there is one, stop and try next.
        """
        course_codes = self.filter_online_courses(course_codes)
        class_timetable_matrix = {i: np.zeros((32, 6), dtype=int) for i in range(1, 14)}
        solution: List = []
        solutions: List = []

        def generate_solution(
            course_codes: List,
            class_timetable_matrix,
            solutions: List[Dict],
            solution: Dict,
        ) -> List[Dict]:

            if len(course_codes) == 0:
                # return dictionary that contains a single possibility
                if len(solution) == count:
                    solutions.append(deepcopy(solution))
                return solution
            else:
                course_code = course_codes[0]
                indexes: List[Dict] = self.class_timetables[course_code]["Indexes"]
                if course_code == "HW0188" or course_code == "HW0288":
                    indexes = self.filter_by_group(indexes, user_group)

                for index_info in indexes:
                    if self.check_class_clash(
                        self.add_index(class_timetable_matrix, index_info["Info"])
                    ):
                        # if clash, try the next index
                        self.remove_index(class_timetable_matrix, index_info["Info"])
                        continue
                    index_num = index_info["Index"]
                    index_info["Code"] = course_code
                    solution.append(index_info)
                    solution = generate_solution(
                        course_codes[1:], class_timetable_matrix, solutions, solution
                    )
                    solution.pop()
                    self.remove_index(class_timetable_matrix, index_info["Info"])
                return solution

        if len(course_codes) == 0:
            return solutions

        course_code: str = course_codes[0]
        indexes: List[Dict] = self.class_timetables[course_code]["Indexes"] # read the indexes of this course
        if course_code in COMMUNICATION_COURSES:
            indexes = self.filter_by_group(indexes, user_group)
        logger.debug("Generating timetable...")
        for index_info in indexes:
            # starting point of adding index of first course
            class_timetable_matrix = self.add_index(
                class_timetable_matrix, index_info["Info"]
            )
            index_info["Code"] = course_code
            solution.append(index_info)
            # using first course as anchor, expand upon it
            generate_solution(
                course_codes=course_codes[1:],
                class_timetable_matrix=class_timetable_matrix,
                solutions=solutions,
                solution=solution,
            )
            class_timetable_matrix = self.remove_index(
                class_timetable_matrix, index_info["Info"]
            )
            solution.pop()
        logger.debug(f"Count        : {len(solutions)}")

        day_solutions = []

        # each solution is in array that contains a dictionary
        for sol in solutions:
            # multiple courses in each solution
            day_solution = {
                "solutions": {
                    "mon": [],
                    "tue": [],
                    "wed": [],
                    "thu": [],
                    "fri": [],
                    "sat": [],
                },
                "stats": {},
            }
            for course in sol:
                index_num = course["Index"]
                course_code = course["Code"]
                if course_code not in day_solution["stats"]:
                    day_solution["stats"][course_code] = index_num
                for info in course["Info"]:
                    info["Code"] = course_code
                    info["Index"] = index_num
                    day_solution["solutions"][info["Day"].lower()].append(info)
            # sort the day class by time
            for day in day_solution["solutions"].keys():
                day_solution["solutions"][day] = sorted(
                    day_solution["solutions"][day], key=lambda x: x["Time"]
                )

            day_solutions.append(day_solution)

        return day_solutions

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
                start_exam_datetime = datetime.strptime(
                    date + "T" + time, "%d%B%YT%I.%M%p"
                )
                end_exam_datetime = start_exam_datetime + timedelta(
                    minutes=duration_minute
                )
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
                    title=exam_info.get("Title", ""),
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

    def check_class_clash(self, timetable_matrixes) -> bool:
        """
        Check if there's a conflict in the index.
        """
        for key, timetable_matrix in timetable_matrixes.items():
            timetable_clashes = timetable_matrix >= 2
            if timetable_clashes.any():
                return True
        return False
