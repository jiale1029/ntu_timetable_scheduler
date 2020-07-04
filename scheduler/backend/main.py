from typing import List, Dict, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scheduler.backend.timetable_service import TimetableService

def register_middleware(app) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def create_application() -> FastAPI:
    app = FastAPI()
    register_middleware(app)
    return app

app = create_application()
class_timetables, exam_timetables = TimetableService.load_timetable()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/api/courses")
def read_courses():
    return {
        "count": len(class_timetables),
        "results": class_timetables
    }

@app.get("/api/courses/{course_code}")
def read_course(course_code: str):
    if course_code not in class_timetables:
        return {
            "exist": False,
            "message": "Course does not exist."
        }
    return {
        "exist": True,
        **class_timetables[course_code]
    }

@app.get("/api/exams")
def read_exams():
    return {
        "count": len(class_timetables),
        "results": exam_timetables
    }

@app.get("/api/exams/{course_code}")
def read_exams(course_code: str):
    if course_code not in class_timetables:
        return {
            "exist": False,
            "message": "Invalid course code."
        }
    if course_code not in exam_timetables:
        return {
            "exist": False,
            "results": {},
            "message": "{} does not has exam.".format(course_code)
        }
    return {
        "exist": True,
        "code": course_code,
        **exam_timetables[course_code]
    }

@app.get("/api/timetables")
def read_timetables(course_codes: Optional[List[str]] = Query(None)):
    class_possibilities = TimetableService.generate_class_timetable()
    exam_possibilities = TimetableService.generate_exam_timetable()
    return None
