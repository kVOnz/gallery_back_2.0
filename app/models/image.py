from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base 
import uuid


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    file_path = Column(String(500), nullable=False)
    is_moderated = Column(Boolean, nullable=False, default=False, index=True)
    moderation_code = Column(String(10), nullable=True) # True потому что если все норм, то кода не будет
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    uploaded_id = Column(
    UUID(as_uuid=True),
    ForeignKey("users.id", ondelete="SET NULL"),
    nullable=True,
    index=True,
    )

    uploader = relationship("User", back_populates="images")

    __table_args__ = (
        Index("ix_images_moderation_queue", "is_moderated", "created_at"),
    )