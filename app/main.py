from fastapi import FastAPI
from app.api.v1.endpoints.grag import grag_router
from app.core.logging import logger
import uvicorn


# Create FastAPI app instance
app = FastAPI(
    title="Grag API",
    description="API for Grag service",
    version="1.0.0")

# Include routers
app.include_router(grag_router, prefix="/api/v1", tags=["grag"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Welcome to Grag API",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)