from fastapi import FastAPI


class CourseNotFoundException(Exception):
    def __init__(self, **kwargs: str):
        self.message = {}
        self.message.update(kwargs)
