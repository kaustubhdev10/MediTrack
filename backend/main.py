from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection
from routers import medicines


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle startup and shutdown events.
    Connects to the database on startup and closes the connection on shutdown.
    """
    await connect_to_mongo()
    print("Successfully connected to MongoDB.")
    yield
    await close_mongo_connection()
    print("MongoDB connection closed.")


app = FastAPI(
    title="MediTrack API",
    description="API for managing pharmacy inventory and orders.",
    version="1.0.0",
    lifespan=lifespan,
)

# Include the medicines router
app.include_router(medicines.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the MediTrack API!"}