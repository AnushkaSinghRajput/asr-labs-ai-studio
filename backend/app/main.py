"""FastAPI entrypoint for ASR LABS AI Content Operating System."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="ASR LABS AI Content OS",
    description="Founder control plane for multi-channel educational content.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
def root() -> dict:
    return {
        "name": settings.app_name,
        "version": __version__,
        "docs": "/docs",
        "health": "/api/health",
    }
