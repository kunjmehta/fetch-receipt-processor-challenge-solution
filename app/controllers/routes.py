import os
import logging
# from typing import 
from fastapi import (
    APIRouter,
    HTTPException
)
import uuid
import re
import logging

# custom imports
from models.models import *
from services.services import *


# create base router object for FastAPI
router = APIRouter()
logger = logging.getLogger(__name__)

receipt_cache = {}

"""Test hello world route"""
@router.get("/hello/", tags=["hello-world"])
async def hello_world():
    return {"message": "Hello World"}


@router.post("/receipts/process", 
    response_model=ReceiptIdResponse, 
    response_model_exclude_none = False,
    tags=["get-receipt-id"])

async def get_receipt_id(request: ReceiptRequest) -> ReceiptIdResponse:
    """
    Generate an ID for the given receipt.

    Args:
        receipt (ReceiptRequest): The receipt object
        
    Returns:
        ReceiptIdResponse: The response object containing id for the receipt
    """
    if not validate_receipt(request, logger):
        raise HTTPException(status_code=400, detail="The receipt is invalid.")
    
    id = uuid.uuid4()
    receipt_cache[str(id)] = request

    logger.info(f"The generated id for receipt:{request.__str__} is {str(id)}")

    return ReceiptIdResponse(id=str(id))


@router.get("/receipts/{id}/points",
    response_model=ReceiptPointsResponse,
    response_model_exclude_none = False,
    tags=["get-receipt-points"])

async def get_receipt_points(id: str) -> ReceiptPointsResponse:
    """
    Get the amount of points awarded to the receipt

    Args:
        id (str): The ID for the receipt
        
    Returns:
        ReceiptPointsResponse: The response object containing points for the receipt
    """

    if not re.compile("^\\S+$").match(id):
        raise HTTPException(status_code=400, detail="The ID is invalid")

    if id not in receipt_cache:
        raise HTTPException(status_code=404, detail="No receipt found for that ID.")

    points = calculate_points(receipt_cache[id], logger)
    logger.info(f"Receipt with ID:{id} has points awarded: {str(points)}")

    return ReceiptPointsResponse (points=str(points))


def get_router():
    return router