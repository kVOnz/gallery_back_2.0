from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence, Optional
from uuid import UUID

from app.database import get_session
from app.schemas.image import ImageCreate, ImageResponse, ImageUpdate
from app.repositories.images import (
    create_image, get_image_by_id, find_image_by_name, 
    get_all_images, update_image, delete_image
)

router = APIRouter(prefix="/images", tags=["Images"])

@router.post("/", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_new_image(image_data: ImageCreate, db: AsyncSession = Depends(get_session)):
    existing = await find_image_by_name(db, image_data.name)
    if existing:
        raise HTTPException(status_code=409, detail="Картинка с таким именем уже существует")
    return await create_image(db, image_data)

@router.get("/", response_model=Sequence[ImageResponse])
async def list_images(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100),
    is_moderated: Optional[bool] = Query(None), db: AsyncSession = Depends(get_session)
):
    return await get_all_images(db, skip=skip, limit=limit, is_moderated=is_moderated)

@router.get("/{image_id}", response_model=ImageResponse)
async def get_image(image_id: UUID, db: AsyncSession = Depends(get_session)):
    image = await get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Картинка не найдена")
    return image

@router.put("/{image_id}", response_model=ImageResponse)
async def update_existing_image(image_id: UUID, image_data: ImageUpdate, db: AsyncSession = Depends(get_session)):
    image = await get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Картинка не найдена")
    return await update_image(db, image, image_data)

@router.delete("/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_image(image_id: UUID, db: AsyncSession = Depends(get_session)):
    image = await get_image_by_id(db, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Картинка не найдена")
    await delete_image(db, image)