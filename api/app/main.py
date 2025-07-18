from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .routers import products


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Initialize database on startup
    await init_db()
    yield


app = FastAPI(
    title="Cardfolio 2.0 API",
    description="Card collecting platform with price tracking and portfolio management",
    version="0.1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(products.router, prefix="/api/v1")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Cardfolio 2.0 API", "version": "0.1.0"}
