"""Configuration Management Module for the project."""

import json
import os
from typing import Dict

import boto3
from dotenv import load_dotenv
from fastapi import HTTPException, status

from log import logger

AWS_CONFIG_PATH = "aws.json"
DOT_ENV_PATH = ".env"


def load_config(config_path: str) -> Dict[str, str]:
    # sourcery skip: move-assign-in-block, use-fstring-for-concatenation
    """Load the configuration from the config file.

    Args:
        config_path (str): Path to the config file

    Returns:
        Dict[str, str]: Configurations
    """

    try:
        with open(file=config_path, mode="r", encoding="utf-8") as config_file:
            configurations: Dict[str, str] = json.load(config_file)

    except Exception as e:

        message = "Error while loading the configuration file."
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        raise HTTPException(
            status_code=status_code,
            detail={
                "message": str(e) if message is None else message,
                "path": (
                    "Check Logs"
                    if e is None or e.__traceback__ is None
                    else e.__traceback__.tb_frame.f_code.co_filename
                    + ":"
                    + str(e.__traceback__.tb_lineno)
                ),
            },
        ) from e

    return configurations


def set_env_variables(env_variables: Dict[str, str]) -> None:
    """Set the environment variables.

    Args:
        env_variables (Dict[str, str]): Environment variables
    """

    for key, value in env_variables.items():
        os.environ[key] = value


def get_aws_secret() -> None:
    """Get the AWS secret from the environment variables and set it in the environment variables."""

    secret_name = str(os.getenv("AWS_SECRET_NAME"))
    region_name = str(os.getenv("AWS_REGION_NAME"))
    service_name = str(os.getenv("AWS_SERVICE_NAME"))
    aws_access_key_id = str(os.getenv("AWS_ACCESS_KEY_ID"))
    aws_secret_access_key = str(os.getenv("AWS_SECRET_ACCESS_KEY"))

    try:
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name=service_name,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        get_secret_value_response = client.get_secret_value(SecretId=secret_name)

        # Decrypts secret using the associated KMS key.
        set_env_variables(
            env_variables=json.loads(get_secret_value_response["SecretString"])
        )

    except Exception:
        logger.info("Error while getting the AWS secret.\n" + "Exiting Program...\n")
        exit()


class ConfigLoader:
    """Configuration Loader Class for the project."""

    def __init__(self):
        """Initialize the ConfigLoader class."""

        # check if aws.json exists
        if os.path.isfile(AWS_CONFIG_PATH):
            logger.info("Loading Environment Variables from AWS Secrets Manager...")

            aws_config = load_config(config_path=AWS_CONFIG_PATH)
            set_env_variables(env_variables=aws_config)
            get_aws_secret()

        elif os.path.isfile(DOT_ENV_PATH):
            logger.info("Loading Environment Variables from .env file...")
            load_dotenv(override=True)

        else:
            logger.info("***No configuration file found.***")
            logger.info("Trying to load aws environment variables from the system...\n")
            get_aws_secret()

        self.endpoint_config = {
            "fastapi_endpoint": os.getenv("FASTAPI_ENDPOINT"),
            "nestjs_endpoint": os.getenv("NESTJS_ENDPOINT"),
        }

        assert self.endpoint_config.get(
            "nestjs_endpoint"
        ), "No nestjs_endpoint found in environment variables"
        print(
            f"######## NestJS Endpoint: {self.endpoint_config.get('nestjs_endpoint')}"
        )

        self.env_config = {
            "cronjob_env": os.getenv("CRONJOB_ENV"),
            "fastapi_env": os.getenv("FASTAPI_ENV"),
            "mongodb_env": os.getenv("MONGODB_ENV"),
            "nestjs_env": os.getenv("NESTJS_ENV"),
        }
        self.firebase_service_account_key = {
            "type": os.getenv("FIREBASE_TYPE"),
            "project_id": os.getenv("FIREBASE_PROJECT_ID"),
            "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": str(os.getenv("FIREBASE_PRIVATE_KEY")).replace(r"\n", "\n"),
            "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.getenv("FIREBASE_CLIENT_ID"),
            "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
            "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv(
                "FIREBASE_AUTH_PROVIDER_X509_CERT_URL"
            ),
            "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
        }
        self.firebase_base_config = {
            "apiKey": os.getenv("FIREBASE_API_KEY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
            "appId": os.getenv("FIREBASE_APP_ID"),
            "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID"),
            "serviceAccount": self.firebase_service_account_key,
        }
        self.mongo_db_config = {
            "database_name": str(os.getenv("MONGODB_DATABASE_NAME")),
            "database_url": str(os.getenv("MONGODB_DATABASE_URL")),
            "username": str(os.getenv("MONGODB_USERNAME")),
            "password": str(os.getenv("MONGODB_PASSWORD")),
        }

        assert self.mongo_db_config.get(
            "database_name"
        ), "No database name found in environment variables"
        print(f"######## Database Name: {self.mongo_db_config.get('database_name')}")

        self.send_grid_config = {
            "api_key": os.getenv("SENDGRID_API_KEY"),
            "from_email": os.getenv("SENDGRID_FROM_EMAIL"),
            "server": os.getenv("SENDGRID_SERVER_EMAIL"),
            "port": os.getenv("SENDGRID_PORT"),
            "username": os.getenv("SENDGRID_USERNAME"),
            "password": os.getenv("SENDGRID_PASSWORD"),
            "no_reply_email": os.getenv(
                "SENDGRID_NO_REPLY_EMAIL", "no-reply@padelmates.se"
            ),
        }


config_loader = ConfigLoader()


if __name__ == "__main__":
    from pprint import pprint

    pprint(config_loader.firebase_service_account_key)
    pprint(config_loader.env_config)
    pprint(config_loader.firebase_base_config)
    pprint(config_loader.mongo_db_config)
    pprint(config_loader.send_grid_config)
