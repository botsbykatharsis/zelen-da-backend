from fastapi import APIRouter

from models.user import UserLaunch
from services.sheets import register_user


router = APIRouter(prefix="/users")


@router.post("/launch")
def launch(user: UserLaunch):
    return register_user(user.dict())