import os
import logging
from logging import config
# from typing import 
from fastapi import (
    FastAPI
)
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# custom imports
from controllers.routes import get_router
from config.logging_setup import initialize_log_location, LOG_CONFIG_FILE_STARTUP
from config.app_setup import get_app_config


"""Entry point into the program that gets app and log config and starts
Uvicorn server"""
if __name__ == "__main__":
    print(f"Trying to start up app environment and configurations....")
    app_config = get_app_config()
    try:
        # Create log directory and file, if not present from log config
        config.dictConfig(initialize_log_location(app_config))
        logger = logging.getLogger(__name__)
        print(f"Starting FastAPI application for receipt processing")
    except Exception as error:
        print("Fatal Error: Unable initialize app and logging. Exiting...")
        raise

    # FastAPI app
    app = FastAPI(title = "Receipt Processor",
                 description = "API for receipt processing")

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
        expose_headers = ["content-disposition"]
    )

    app.include_router(get_router())

    logger.info("Starting FastAPI Uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, 
    log_config=os.path.join(app_config["log_location"], LOG_CONFIG_FILE_STARTUP))

