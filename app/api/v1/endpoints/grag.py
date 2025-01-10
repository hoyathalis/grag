from fastapi import APIRouter, Depends
from app.services.grag.grag_service import GragService

grag_router = APIRouter()

@grag_router.get("/grag")
async def get_grag_data(grag_service: GragService = Depends(GragService)):
    return await grag_service.get_grag_data()