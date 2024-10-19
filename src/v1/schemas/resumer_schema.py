"""This is the schema for the resumer"""
from typing import List
from pydantic import BaseModel, Field

class Resumer(BaseModel):
    completion: str = Field(description="Generated resumer")

class JobOfferDetails(BaseModel):
    jobOfferExperiences: str = Field(description="The experiences/hard-skills required")
    jobOfferSofSkills: str = Field(description="The softskill required")