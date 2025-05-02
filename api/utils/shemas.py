from pydantic import BaseModel

class Rotation(BaseModel):
    page: int
    degrees: float