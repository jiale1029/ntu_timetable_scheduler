import os
import time
import random
import logging
import string

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

log_dir = os.path.join(os.path.dirname(os.path.abspath("timetable_service.py")), "logs")
FORMAT = "%(asctime)-15s : %(message)s"

logger = logging.getLogger(__file__)
file_handler = logging.FileHandler(os.path.join(log_dir, "timetable_service.log"))
formatter = logging.Formatter(FORMAT)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        logger.info(f"rid={idem} start request path={request.url.path}")
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)
        logger.info(
            f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response


# class CourseFilterMiddleware:
#    async def dispatch(self, request, call_next):
# TODO: Add a course filtering middleware
#        pass
