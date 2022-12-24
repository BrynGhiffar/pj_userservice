from pydantic import BaseModel, Field

class Class(BaseModel):
    class_id: str | None
    lecturer_id: str | None
    name: str
    semester: str
    year: str 
    class_code: str
    course_code: str
    projects: list[str] = []

