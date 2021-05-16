import os
import time
import logging
from typing import Dict, List, Optional

from fastapi import FastAPI, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from scheduler.backend.exception import CourseNotFoundException
from scheduler.backend.middleware import ProcessTimeMiddleware
from scheduler.backend.timetable_service import TimetableService

log_dir = os.path.join(os.path.dirname(os.path.abspath("timetable_service.py")), "logs")
FORMAT = "%(asctime)-15s : %(message)s"

logger = logging.getLogger(__file__)
file_handler = logging.FileHandler(os.path.join(log_dir, "timetable_service.log"))
formatter = logging.Formatter(FORMAT)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def register_middleware(app) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ProcessTimeMiddleware)


def register_exception_handler(app) -> None:
    @app.exception_handler(CourseNotFoundException)
    async def course_not_found_handler(request: Request, exc: CourseNotFoundException):
        return JSONResponse(status_code=404, content=exc.message)

    app.add_exception_handler(CourseNotFoundException, course_not_found_handler)


def create_application() -> FastAPI:
    app = FastAPI()
    register_middleware(app)
    register_exception_handler(app)
    return app


app = create_application()
class_timetables, exam_timetables = TimetableService.load_timetable()


@app.get("/")
def root():
    logger.debug("abc")
    return {"message": "Hello World"}


@app.get("/api/courses", status_code=status.HTTP_200_OK)
def read_courses():
    return {"count": len(class_timetables), "results": class_timetables}


@app.get("/api/courses/{course_code}", status_code=status.HTTP_200_OK)
def read_course(course_code: str):
    if course_code not in class_timetables:
        logger.warning(f"{course_code} not available.")
        raise CourseNotFoundException(
            exist=False, message=f"{course_code} does not exist."
        )
    return {"exist": True, **class_timetables[course_code]}


@app.get("/api/exams", status_code=status.HTTP_200_OK)
def read_exams():
    return {"count": len(exam_timetables), "results": exam_timetables}


@app.get("/api/exams/{course_code}", status_code=status.HTTP_200_OK)
def read_exam(course_code: str):
    if course_code not in class_timetables:
        logger.warning(f"{course_code} not available.")
        raise CourseNotFoundException(
            exist=False, message=f"{course_code} does not exist."
        )
    if course_code not in exam_timetables:
        logger.warning(f"{course_code} exam not available.")
        raise CourseNotFoundException(
            exist=False, results={}, message=f"{course_code} does not have exams."
        )
    return {"exist": True, "code": course_code, **exam_timetables[course_code]}


@app.get("/api/parseTime/{time}", status_code=status.HTTP_200_OK)
def parse_time(time: str):
    return {"time": TimetableService.parse_time(time_range=time)}


@app.get("/api/timetables", status_code=status.HTTP_200_OK)
def read_timetables(course_code: Optional[List[str]] = Query(None)):
    for cc in course_code:
        if cc not in class_timetables:
            logger.warning(f"{cc} not available.")
            raise CourseNotFoundException(exist=False, message=f"{cc} does not exist.")

    ts = TimetableService()

    exam_possibilities = ts.generate_exam_timetable(course_code)
    if not exam_possibilities:
        return {"message": "There is a clash in the exam."}

    class_possibilities = ts.generate_class_timetable(course_code, "")
    if not class_possibilities:
        return {"message": "No possible arrangement."}

    return {
        "class": class_possibilities,
        "count": len(class_possibilities),
        "exam": exam_possibilities,
    }


@app.get("/api/course/search", status_code=status.HTTP_200_OK)
def search_course(query: Optional[str]):
    return [
        {"Code": class_timetables[key]["Code"], "Title": class_timetables[key]["Title"]}
        for key in class_timetables.keys()
        if query in key or query.lower() in class_timetables[key]["Title"].lower()
    ]
