from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.youtube_transcript.routes import router as youtube_transcript_router
from src.chat.routes import router as chat_router
from src.common.redis.connection import RedisConnection


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan context manager for app startup and shutdown events."""
    # Initialize Redis connection
    RedisConnection.initialize()
    print("Redis connection established")

    yield
    # Close Redis connection
    RedisConnection.close()
    print("Redis connection closed")


# Create FastAPI instance
app = FastAPI(
    title="Sample FastAPI App",
    description="A simple FastAPI application with basic CRUD operations",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/api",
)

# Include routers
app.include_router(youtube_transcript_router)
app.include_router(chat_router)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7788, reload=True)
