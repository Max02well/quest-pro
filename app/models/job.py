from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Job(BaseModel):
    title: str
    description: str
    company: str
    location: str
    type: str
    experience: str
    salaryRange: str
    posted_date: Optional[str]
