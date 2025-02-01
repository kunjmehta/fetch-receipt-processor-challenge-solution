import json
import os
import pathlib

def get_app_config() -> dict:
    app_config_file_name = "app_config.json"
    APP_CONFIG_FILE = os.path.join(str(pathlib.Path(__file__).parent), 
    app_config_file_name)

    app_config = json.load(open(APP_CONFIG_FILE))

    return app_config
