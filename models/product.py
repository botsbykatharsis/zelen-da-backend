from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    image: str
    description: str
    is_promo: bool