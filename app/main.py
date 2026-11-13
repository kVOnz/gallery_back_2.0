from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import images

app = FastAPI(
    title="Gallery Back 2.0 API",
    version="1.0.0",
)

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