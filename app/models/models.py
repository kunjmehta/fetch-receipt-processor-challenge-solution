from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time


class Item(BaseModel):
    """
    A class representing an item in a receipt which inherits the Pydantic BaseModel.

    Attributes:
        shortDescription (str): The description of the item
        price (str): The price of the item
    """

    shortDescription: str = Field(
        title="The Short Product Description for the item.", 
        example="Mountain Dew 12PK"
    )
    price: str = Field(
        title="The total price payed for this item.",
        example="6.49"
    )


class ReceiptIdResponse(BaseModel):
    """
    A class representing the response object for the endpoint /receipts/process
    which inherits the Pydantic BaseModel

    Attributes:
        id (str): The generated ID for the receipt
    """
    id: str = Field(
        title="Id of the receipt", example="7fb1377b-b223-49d9-a31a-5a02701dd310"
    )


class ReceiptPointsResponse(BaseModel):
    """
    A class representing the response object for the endpoint /receipts/{id}/points
    which inherits the Pydantic BaseModel

    Attributes:
        points (str): The points awarded to the receipt with ID id
    """
    points: str = Field(
        title="Points awarded to the receipt", example=32
    )


class ReceiptRequest(BaseModel):
    """
    A class representing the receipt which inherits the Pydantic BaseModel

    Attributes:
        retailer (str): The name of the retailer
        purchaseDate (date): The date of purchase
        purchaseTime (time): The time of purchase
        items (List[Item]): List of items on the receipt
        total (str): The total amount paid on the receipt
    """

    retailer: str = Field(
        title="The name of the retailer or store the receipt is from.", 
        example="M&M Corner Market"
    )
    purchaseDate: date = Field(
        title="The date of the purchase printed on the receipt",
        example="2022-01-01"
    )
    purchaseTime: time = Field(
        title="The time of the purchase printed on the receipt. 24-hour time expected",
        example="13:01"
    )
    items: List[Item] = Field(
        title="List of items on the receipt"    
    )
    total: str = Field(
        title="The total amount paid on the receipt",
        example="6.49"
    )

    def __str__(self) -> str:
        return super().__str__()
