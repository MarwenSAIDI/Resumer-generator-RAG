"""This is the schema for the education"""
from typing import List
from pydantic import BaseModel, Field

class School(BaseModel):
    school: str = Field(description="The school or university name")
    location: str = Field(description="The -city, country- where the school is located")
    firstYear: str = Field(description="The initial year of education")
    lastYear: str = Field(description="The last year of education")
    degree: str = Field(description="The degree title")
    specialty: str = Field(description="The descipline or scpecialty studied")

class Education(BaseModel):
    schools: List[School] = Field(description="A list of schools")

