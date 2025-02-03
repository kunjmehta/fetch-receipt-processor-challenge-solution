from datetime import datetime, time
import math
import re
import logging

# custom imports
from models.models import ReceiptRequest
from services.utils import *


def validate_receipt(receipt: ReceiptRequest, logger: logging.Logger) -> bool:
    """
    Function to check validity of receipt based on provided regex patterns in 
    questional yaml

    Args:
        receipt (ReceiptRequest): The receipt object
        logger (logging.Logger): The log handler object
        
    Returns:
        bool: Whether the receipt is valid or not
    """

    valid = True

    if not re.compile("^[\\w\\s\\-&]+$").match(receipt.retailer):
        valid = False
        logger.info("Checking format validity of retailer name on receipt - retailer name format not valid")

    if not re.compile("^\\d+\\.\\d{2}$").match(receipt.total):
        valid = False
        logger.info("Checking format validity of total on receipt - total price format not valid")

    for item in receipt.items:
        if not re.compile("^[\\w\\s\\-]+$").match(item.shortDescription):
            valid = False
            logger.info("Checking format validity of item description on receipt - item description format not valid")
            break
        if not re.compile("^\\d+\\.\\d{2}$").match(item.price):
            valid = False
            logger.info("Checking format validity of item price on receipt - item price format not valid")
            break

    return valid


def calculate_points(receipt: ReceiptRequest, logger: logging.Logger) -> int:
    """
    Function to calculate points awarded to the receipt

    Args:
        receipt (ReceiptRequest): The receipt object
        logger (logging.Logger): The log handler object
        
    Returns:
        int: The points awarded to the receipt
    """

    points = 0
    
    retailer_name = receipt.retailer
    total = float(receipt.total)
    items = receipt.items
    purchase_time = receipt.purchaseTime
    purchase_date = receipt.purchaseDate

    # counting alphanumeric characters
    points += count_alphanumeric(retailer_name)
    logger.info(f"Points after counting alphanumeric characters in retailer name: {points}")

    # checking round dollar amount
    if total % 1 == 0 and total >= 0:
        points += 50
    logger.info(f"Points after checking total is round dollar amount: {points}")

    # checking total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25
    logger.info(f"Points after checking total is multiple of 0.25: {points}")

    # adding points for number of items in receipt
    points += (len(items) // 2) * 5
    logger.info(f"Points after checking number of items in receipt: {points}")

    # adding points for item description
    for item in items:
        if len(item.shortDescription.strip()) % 3 == 0:
            price = math.ceil(float(item.price) * 0.2)
            points += price
    logger.info(f"Points after adding those from item description: {points}")

    # checkin day of purchase
    if purchase_date.day % 2 == 1:
        points += 6
    logger.info(f"Points after checking for day of purchase being odd: {points}")

    # checking purchase time
    if purchase_time.hour >= 14 and purchase_time.hour <= 16:
        points += 10
    logger.info(f"Points after checking for time between 2pm and 4pm: {points}")
    
    return points