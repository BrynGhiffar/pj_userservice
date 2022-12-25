from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: str | None
    provider_id: str | None
    provider: str | None
    name: str
    email: str
    description: str = ""
    profile_pic: str
    graduation_year: str
    current_semester: str
    role: str = ""
    classes: list[str] = []
