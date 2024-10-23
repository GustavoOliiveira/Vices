from flask_login import UserMixin
from datetime import datetime
from app.extensions.firestore import db
from app.extensions.login import login_manager

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from flask_login import UserMixin

class UserSchema(UserMixin, BaseModel):
    username: str
    email: str
    password: str
    provider: str = Field(..., description="email or gmail")
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    is_confirmed: bool = Field(default=False)  
    confirmed_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

    @staticmethod
    def get(user_id):
        user_data = db.collection('users').document(user_id).get()
        if user_data.exists:
            data = user_data.to_dict()
            return UserSchema(**data) #id=user_id
        return None

@login_manager.user_loader
def load_user(user_id):
    return UserSchema.get(user_id)