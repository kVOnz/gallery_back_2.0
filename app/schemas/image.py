from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ImageBase(BaseModel):
    name: str=Field(..., min_length=3, max_length=100)
    title: str=Field(..., min_length=3, max_length=200)
    file_path: str=Field(..., max_length=500)

class ImageCreate(ImageBase):
    uploaded_id: UUID

class ImageResponse(ImageBase):
    id: UUID
    is_moderated: bool = False
    moderation_code: Optional[str] = None
    uploaded_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class ImageUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    file_path: Optional[str] = Field(None, max_length=500)
    is_moderated: Optional[bool] = Field(None, description="Статус модерации")
    moderation_code: Optional[str] = Field(None, max_length=10)