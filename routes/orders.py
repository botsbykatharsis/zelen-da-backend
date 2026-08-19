from fastapi import APIRouter
from models.order import Order
from services.sheets import create_order

router = APIRouter(prefix="/orders")

@router.post("/")
def create(order: Order):
    return create_order(order.dict())