"""This is the schema for the experience"""
from typing import List
from pydantic import BaseModel, Field

class ExperienceContent(BaseModel):
    """This is the schema for the experience content"""
    skills: List[str] = Field(description="A list of skills applied or learned")
    accomplishments: List[str] = Field(description="A list of accomplishement")
class Experience(BaseModel):
    """This is the schema for the experience"""
    experienceId: int
    roleName: str = Field(description="The name of the role occupied")
    companyName: str = Field(description="The company name")
    location: str = Field(description="The area and location of the company")
    datePeriod: str = Field(description="The period of work")
    experienceContent: ExperienceContent

class RetrievedExperience(BaseModel):
    contents: List[str] = Field(description="List of relevant experiences")
