from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import images
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.models import image, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan, title="Gallery Back 2.0 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(images.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}