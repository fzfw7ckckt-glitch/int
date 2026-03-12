from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Investigation, User
from app.schemas import InvestigationCreate, InvestigationResponse
from app.routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_token_from_header(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    return parts[1]

@router.post("/", response_model=InvestigationResponse)
async def create_investigation(
    inv: InvestigationCreate,
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    
    new_investigation = Investigation(
        owner_id=user.id,
        title=inv.title,
        description=inv.description,
        target_identifier=inv.target_identifier,
        status="pending"
    )
    db.add(new_investigation)
    db.commit()
    db.refresh(new_investigation)
    
    logger.info(f"Investigation {new_investigation.id} created by {user.username}")
    return new_investigation

@router.get("/", response_model=list[InvestigationResponse])
async def list_investigations(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    investigations = db.query(Investigation).filter(Investigation.owner_id == user.id).all()
    return investigations

@router.get("/{investigation_id}", response_model=InvestigationResponse)
async def get_investigation(
    investigation_id: str,
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db)
):
    user = get_current_user(token, db)
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id,
        Investigation.owner_id == user.id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    return investigation
