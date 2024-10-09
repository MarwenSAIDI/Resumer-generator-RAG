from pydantic import BaseModel

class Education(BaseModel):
    schoolName: str
    location: str
    startDate: str
    endDate: str
    degree: str
    educationContent: str
