from pydantic import BaseModel

class FrontEnd(BaseModel):
    is_notification: bool = False
    notification_message: str = ""

