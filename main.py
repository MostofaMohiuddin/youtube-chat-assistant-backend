from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from src.youtube_transcript.routes import router as youtube_transcript_router
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
)

# Include YouTube transcript router
app.include_router(youtube_transcript_router)

# # Initialize Redis connection on startup
# @app.on_event("startup")
# async def startup_event():
#     """Initialize connections and resources on startup"""
#     RedisConnection.initialize()
#     print("Redis connection established")

# # Close Redis connection on shutdown
# @app.on_event("shutdown")
# async def shutdown_event():
#     """Close connections and free resources on shutdown"""
#     RedisConnection.close()
#     print("Redis connection closed")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7788, reload=True)
