from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.image import Image
from app.schemas.image import ImageCreate

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