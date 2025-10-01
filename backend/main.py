from fastapi import FastAPI

app = FastAPI(
    title="MediTrack API",
    description="API for managing pharmacy inventory and orders.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the MediTrack API!"}