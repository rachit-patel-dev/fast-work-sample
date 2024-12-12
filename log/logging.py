import builtins
import datetime
import json
import sys
import uuid

# from logging.handlers import TimedRotatingFileHandler
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from loguru import logger
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

# Create a file handler for the logs
# path = os.path.join("log", "logs")
# os.makedirs(path, exist_ok=True)
# log_file = os.path.join(path, f'{datetime.datetime.now().strftime("%Y-%m-%d")}.log')
# file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=30)
# file_handler.setLevel(logging.DEBUG)
# file_handler.setFormatter(formatter)

# Add the file handler to the logger
# logger.addHandler(file_handler)
logger.remove(0)
logger.add(sys.stdout, format="{time:%Y-%m-%d %H:%M:%S} | {level} | {message}")

# Save backup for default print function
_print = builtins.print


# Override the print function to also log messages
def custom_print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    logger.info(message)

    # Call the original print function
    _print(*args, **kwargs)


# Replace the print function with the custom_print function
builtins.print = custom_print


# Define a function to log request body and response body
async def log_info(request, request_body, response, response_body, elapsed_time):
    try:
        request_id = uuid.uuid4()

        # Log the request information
        api_call = (
            f"API Called: {request.method} {request.url.path}?{request.url.query}\n"
        )
        api_request = f"API Request Body: {request_body.decode()}\n"

        # Log the response information
        api_status_code = f"API Response Status Code: {response.status_code}\n"
        # api_response = f"API Response Body: {response_body.decode()}\n"
        api_response = f"API Response Body:\n{json.dumps(json.loads(response_body.decode()), indent=4)}\n"

        # Log the elapsed time
        api_call_duration = (
            f"API Call Duration: {elapsed_time.total_seconds():.2f} seconds\n"
        )

        # Log the API call, response and duration
        logger.info(f"({request_id}) - Request started.")
        logger.info(f"({request_id}) - {api_call}")
        logger.info(f"({request_id}) - {api_request}")
        logger.info(f"({request_id}) - {api_status_code}")
        logger.info(f"({request_id}) - {api_response}")
        logger.info(f"({request_id}) - {api_call_duration}")
        logger.info(
            f"({request_id}) - Request ended.\n" + "-" * 50 + "END" + "-" * 50 + "\n"
        )
    except Exception as e:
        print(f"Exception while logging: {e}")


# Custom APIRoute class for logging request and response
class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        # Get the original route handler
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # Get the request body
            req_body = await request.body()

            start_time = datetime.datetime.now()

            # Call the original route handler
            response = await original_route_handler(request)

            # Calculate the elapsed time
            end_time = datetime.datetime.now()
            elapsed_time = end_time - start_time

            if isinstance(response, StreamingResponse):
                # If the response is StreamingResponse, stream and log the response body
                res_body = b""
                async for item in response.body_iterator:
                    if isinstance(item, str):
                        item = item.encode()
                    res_body += item

                # Create a background task to log the request and response
                task = BackgroundTask(
                    log_info, request, req_body, response, res_body, elapsed_time
                )

                # Return a Response with the streamed body and background task
                return Response(
                    content=res_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                    background=task,
                )
            else:
                # If the response is not StreamingResponse, log the response body
                res_body = response.body

                # Add a background task to log the request and response
                response.background = BackgroundTask(
                    log_info, request, req_body, response, res_body, elapsed_time
                )

                # Return the response
                return response

        return custom_route_handler
