"""This is the schema for the education"""
from pydantic import BaseModel

class Education(BaseModel):
    """This is the schema for the education"""
    schoolName: str
    location: str
    startDate: str
    endDate: str
    degree: str
    educationContent: str
