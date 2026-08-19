from pydantic import BaseModel
from typing import List

class OrderItem(BaseModel):
    id: int
    qty: int

class Order(BaseModel):
    user_id: int
    items: List[OrderItem]
    name: str
    phone: str