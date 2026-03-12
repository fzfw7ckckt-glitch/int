from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def health_check():
    return {
        "status": "ok",
        "service": "OSINT Platform API",
        "version": "1.0.0"
    }

@router.get("/live")
async def liveness():
    return {"status": "alive"}

@router.get("/ready")
async def readiness():
    return {"status": "ready"}
