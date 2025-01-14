from fastapi import APIRouter, Depends
from app.services.grag.grag_service import GragService
from fastapi import UploadFile, File

grag_router = APIRouter()

@grag_router.post("/grag")
async def create_grag_data(file: UploadFile = File(...), grag_service: GragService = Depends(GragService)):
    return await grag_service.create_grag_request(file)

@grag_router.get("/grag/{request_id}")
async def get_grag_data(request_id: str, grag_service: GragService = Depends(GragService)):
    return await grag_service.get_grag_request(request_id)