import json
import os
import pathlib
import datetime

# custom imports
from .app_setup import get_app_config

LOG_CONFIG_FILE = os.path.join(str(pathlib.Path(__file__).parent), "log_config.json")
LOG_CONFIG_FILE_STARTUP = os.path.join(str(pathlib.Path(__file__).parent), "log_config_startup.json")
LOG_FILE_NAME = f"receipt_processor_log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"


def get_logger_config() -> dict:
    if os.path.exists(LOG_CONFIG_FILE):
        with open(LOG_CONFIG_FILE) as config:
            return json.load(config)
    raise FileNotFoundError(f"{LOG_CONFIG_FILE} log config file does not exist")


def initialize_log_location(app_config: dict) -> dict:
    if not os.path.exists(app_config["log_location"]):
        print(f'{app_config["log_location"]} does not exist and trying to create now...')
        os.makedirs(app_config["log_location"], exist_ok=True)

    log_file_location = os.path.join(app_config["log_location"], )
    logger_config = get_logger_config()
    logger_config["handlers"]["log_file_handler"]["filename"] = os.path.join(app_config["log_location"], LOG_FILE_NAME)

    with open(LOG_CONFIG_FILE_STARTUP, "w") as log_file:
        json.dump(logger_config, log_file)

    return logger_config