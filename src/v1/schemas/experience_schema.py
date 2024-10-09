"""This is the schema for the experience"""
from typing import List
from pydantic import BaseModel, Field

class ExperienceContent(BaseModel):
    """This is the schema for the experience content"""
    companyName: str = Field(description="The company name")
    startDate: str = Field(description="The date when the experience started")
    endDate: str = Field(description="The date when the experience ended")
    location: str = Field(description="The area and location of the company")
    skills: List[str] = Field(description="A list of skills applied or learned")
    accomplishments: List[str] = Field(description="A list of accomplishement")
class Experience(BaseModel):
    """This is the schema for the experience"""
    experienceId: int
    roleName: str = Field(description="The name of the role occupied")
    experienceContent: ExperienceContent
