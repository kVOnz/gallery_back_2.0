from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Sequence, Optional

from app.models.image import Image
from app.schemas.image import ImageCreate, ImageUpdate

async def create_image(db: AsyncSession, image_data: ImageCreate) -> Image: #orm модель
    db_image = Image(
        name=image_data.name,
        title=image_data.title,
        file_path=image_data.file_path,
        uploaded_id=image_data.uploaded_id,
        is_moderated=False,
    )
    
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image

async def get_image_by_id(db: AsyncSession, image_id: UUID) -> Optional[Image]:
    result = await db.execute(select(Image).where(Image.id == image_id))
    return result.scalars().first()

async def find_image_by_name(db: AsyncSession, name: str) -> Optional[Image]:
    result = await db.execute(select(Image).where(Image.name == name))
    return result.scalars().first()

async def get_all_images(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 10,
    is_moderated: Optional[bool] = None) -> Sequence[Image]:
    query = select(Image)
    
    if is_moderated is not None:
        query = query.where(Image.is_moderated == is_moderated)
    
    query = query.offset(skip).limit(limit).order_by(Image.created_at.desc())
    
    result = await db.execute(query)
    return result.scalars().all()

async def update_image(
    db: AsyncSession, 
    image: Image, 
    update_data: ImageUpdate) -> Image:
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(image, field, value)
    
    await db.commit()
    await db.refresh(image)
    return image