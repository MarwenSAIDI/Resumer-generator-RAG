from typing import List
from pydantic import BaseModel

class ExperienceContent(BaseModel):
    companyName: str
    startDate: str
    endDate: str
    location: str
    skills: List[str]
    accomplishments: List[str]

class Experience(BaseModel):
    experienceId: str 
    experienceContent: ExperienceContent