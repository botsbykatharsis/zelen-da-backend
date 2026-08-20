from pydantic import BaseModel
from typing import List, Optional

class OrderItem(BaseModel):
    id: int
    qty: int

class Order(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = "unknown"
    items: List[OrderItem]
    name: str
    phone: str