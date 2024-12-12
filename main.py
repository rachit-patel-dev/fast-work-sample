import os
from typing import List

import psutil
from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_restful.tasks import repeat_every

from configs import config_loader
from internal import (
    periodic_task,
    qt_task,
    remove_expired_unscheduled_series_game_extra_bookings,
    send_reminder_notification_fo_series_match,
)
from log import logger as p_logger
from routers import statistics
from utils import raise_non_http_exception

# Set Server Mode
if config_loader.env_config["fastapi_env"] == "DEVELOPMENT":
    app = FastAPI(title="Padelmates", debug=True)
elif config_loader.env_config["fastapi_env"] == "PRODUCTION":
    app = FastAPI(title="Padelmates", debug=False, redoc_url=None)
else:
    raise ValueError("Invalid Server Mode")


# Enabling CORS permissions
allow_all = ["*"]
allow_all_origin = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all_origin,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all,
)


# Default Router
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Backend API.",
        "docs": "http://example.com/docs",
    }


# Statistics
prefix = "/club/statistics"
tag = ["My Club / Statistics"]
app.include_router(router=statistics.router, prefix=prefix, tags=tag)


@app.on_event("startup")
async def startup_tasks():  # NEED ATLEAST 2 WORKERS TO RUN ALL TASKS
    if (
        config_loader.env_config.get("cronjob_env", "DEVELOPMENT")
        == "PRODUCTION"  # "DEVELOPMENT" | "PRODUCTION"
    ):
        # Run Periodic Background Task
        await initialize_periodic_background_task()

        # Run QT Background Task
        await initialize_qt_background_task()

        # Run Remove Booking Series Game Background Task
        await initialize_remove_booking_background_task()

        # Run Send Reminder Send Reminder Notification Background Task
        await initialize_send_reminder_notification_background_task()
    else:
        p_logger.info(
            "Background Tasks are not running"
            + "\n"
            + " " * 34
            + "set CRONJOB_ENV=PRODUCTION in .env to run background tasks"
        )


# BG_TASK will run every (10 * 60.0)s = 10mins after the server starts
BG_TASK_TIMER = 10 * 60.0

BG_TASK_TIMER_ONE_HOUR = 60 * 60.0


@repeat_every(seconds=BG_TASK_TIMER, raise_exceptions=True)
async def initialize_periodic_background_task():
    WORKER_NUMBER = 1

    try:
        all_process_pids = sorted(
            [process.pid for process in psutil.Process(os.getppid()).children()]
        )
        current_process_pid = os.getpid()

        if (
            len(all_process_pids) > WORKER_NUMBER
            and current_process_pid == all_process_pids[WORKER_NUMBER]
        ):
            p_logger.info(f"1st Worker Process ID: {current_process_pid}")

            background_tasks = BackgroundTasks()
            background_tasks.add_task(await periodic_task())

    except Exception as e:
        raise_non_http_exception(e=e)


@repeat_every(seconds=BG_TASK_TIMER, raise_exceptions=True)
async def initialize_qt_background_task():
    WORKER_NUMBER = 2

    try:
        all_process_pids = sorted(
            [process.pid for process in psutil.Process(os.getppid()).children()]
        )
        current_process_pid = os.getpid()

        if (
            len(all_process_pids) > WORKER_NUMBER
            and current_process_pid == all_process_pids[WORKER_NUMBER]
        ):
            p_logger.info(f"2nd Worker Process ID: {current_process_pid}")

            background_tasks = BackgroundTasks()
            background_tasks.add_task(await qt_task())

    except Exception as e:
        raise_non_http_exception(e=e)


@repeat_every(seconds=BG_TASK_TIMER_ONE_HOUR, raise_exceptions=True)
async def initialize_remove_booking_background_task():
    WORKER_NUMBER = 3

    try:
        all_process_pids = sorted(
            [process.pid for process in psutil.Process(os.getppid()).children()]
        )
        current_process_pid = os.getpid()

        if (
            len(all_process_pids) > WORKER_NUMBER
            and current_process_pid == all_process_pids[WORKER_NUMBER]
        ):
            p_logger.info(f"3rd Worker Process ID: {current_process_pid}")

            background_tasks = BackgroundTasks()
            background_tasks.add_task(
                await remove_expired_unscheduled_series_game_extra_bookings()
            )

    except Exception as e:
        raise_non_http_exception(e=e)


@repeat_every(seconds=BG_TASK_TIMER_ONE_HOUR, raise_exceptions=True)
async def initialize_send_reminder_notification_background_task():
    WORKER_NUMBER = 4

    try:
        all_process_pids = sorted(
            [process.pid for process in psutil.Process(os.getppid()).children()]
        )
        current_process_pid = os.getpid()

        if (
            len(all_process_pids) > WORKER_NUMBER
            and current_process_pid == all_process_pids[WORKER_NUMBER]
        ):
            p_logger.info(f"4th Worker Process ID: {current_process_pid}")

            background_tasks = BackgroundTasks()
            background_tasks.add_task(
                await send_reminder_notification_fo_series_match()
            )

    except Exception as e:
        raise_non_http_exception(e=e)


if __name__ == "__main__":
    import logging
    import multiprocessing
    import sys

    from gunicorn.app.base import BaseApplication
    from gunicorn.glogging import Logger
    from loguru import logger

    # https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
    JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False

    WORKERS = multiprocessing.cpu_count() * 2 + 1
    THREADS = multiprocessing.cpu_count()

    logger.info("WORKERS:", WORKERS)
    logger.info("THREADS:", THREADS)

    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # find caller from where originated the logged message
            frame, depth = sys._getframe(6), 6
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back  # type: ignore [assignment]
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    class StubbedGunicornLogger(Logger):
        def setup(self, cfg):
            handler = logging.NullHandler()
            self.error_logger = logging.getLogger("gunicorn.error")
            self.error_logger.addHandler(handler)
            self.access_logger = logging.getLogger("gunicorn.access")
            self.access_logger.addHandler(handler)
            self.error_logger.setLevel(LOG_LEVEL)
            self.access_logger.setLevel(LOG_LEVEL)

    class StandaloneApplication(BaseApplication):
        """Our Gunicorn application."""

        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {
                key: value
                for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            }
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    intercept_handler = InterceptHandler()
    # logging.basicConfig(handlers=[intercept_handler], level=LOG_LEVEL)
    # logging.root.handlers = [intercept_handler]
    logging.root.setLevel(LOG_LEVEL)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])

    options = {
        "bind": "0.0.0.0",
        "port": 8000,
        "timeout": 5 * 60,
        "workers": WORKERS,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger,
    }

    StandaloneApplication(app, options).run()
