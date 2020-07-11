import time

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


# class CourseFilterMiddleware:
#    async def dispatch(self, request, call_next):
# TODO: Add a course filtering middleware
#        pass
