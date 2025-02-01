from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time


class Item(BaseModel):
    shortDescription: str = Field(
        title="The Short Product Description for the item.", 
        example="Mountain Dew 12PK"
    )
    price: str = Field(
        title="The total price payed for this item.",
        example="6.49"
    )


class ReceiptIdResponse(BaseModel):
    id: str = Field(
        title="Id of the receipt", example="7fb1377b-b223-49d9-a31a-5a02701dd310"
    )


class ReceiptPointsResponse(BaseModel):
    points: str = Field(
        title="Points awarded to the receipt", example=32
    )


class ReceiptRequest(BaseModel):
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
