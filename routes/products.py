from fastapi import APIRouter
from services.sheets import get_products

router = APIRouter(prefix="/products")

@router.get("/")
def products():
    return get_products()