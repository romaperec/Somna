from pydantic import BaseModel, Field


class AudioCreate(BaseModel):
    title: str = Field(min_length=6, max_length=150)
    category: str = Field(min_length=3, max_length=100)
