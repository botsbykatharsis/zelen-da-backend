from pydantic import BaseModel

class UserLaunch(BaseModel):
    user_id: int
    chat_id: int
    username: str = "unknown"