from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Evidence, Investigation
import hashlib
import json
import uuid
from datetime import datetime
from typing import List, Optional

router = APIRouter()

def calculate_hash(data: str) -> str:
    """Розрахунок SHA-256 хешу для забезпечення цілісності (Chain of Custody)"""
    return hashlib.sha256(data.encode()).hexdigest()

@router.post("/store")
async def store_evidence(
    investigation_id: str = Form(...),
    source: str = Form(...),
    data: str = Form(...),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Зберегти доказ у сховище з автоматичним хешуванням"""
    investigation = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")

    evidence_hash = calculate_hash(data)
    
    new_evidence = Evidence(
        investigation_id=investigation_id,
        source=source,
        data=data,
        metadata_json=metadata,
        hash_sha256=evidence_hash,
        created_at=datetime.utcnow()
    )
    
    db.add(new_evidence)
    db.commit()
    db.refresh(new_evidence)
    
    return {
        "id": new_evidence.id,
        "hash": evidence_hash,
        "status": "verified",
        "timestamp": new_evidence.created_at.isoformat()
    }

@router.get("/{investigation_id}/export/stix")
async def export_to_stix(investigation_id: str, db: Session = Depends(get_db)):
    """Експорт зібраних доказів в універсальному форматі STIX 2.1 (Золотий стандарт OSINT)"""
    investigation = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence_list = db.query(Evidence).filter(Evidence.investigation_id == investigation_id).all()
    
    # Створення STIX Bundle
    bundle = {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid4()}",
        "objects": []
    }
    
    # 1. Identity object (Investigator)
    identity_id = f"identity--{uuid.uuid4()}"
    bundle["objects"].append({
        "type": "identity",
        "id": identity_id,
        "name": "OSINT Platform 2026",
        "identity_class": "organization"
    })
    
    # 2. Case description
    case_id = f"report--{uuid.uuid4()}"
    bundle["objects"].append({
        "type": "report",
        "id": case_id,
        "name": investigation.title,
        "description": investigation.description,
        "published": investigation.created_at.isoformat() + "Z",
        "object_refs": [identity_id]
    })
    
    # 3. Evidence indicators
    for item in evidence_list:
        indicator_id = f"indicator--{uuid.uuid4()}"
        bundle["objects"].append({
            "type": "indicator",
            "id": indicator_id,
            "name": f"Evidence from {item.source}",
            "description": f"Raw data hash: {item.hash_sha256}",
            "indicator_types": ["malicious-activity" if "risk" in item.data.lower() else "unknown"],
            "pattern": f"[file:hashes.'SHA-256' = '{item.hash_sha256}']",
            "pattern_type": "stix",
            "valid_from": item.created_at.isoformat() + "Z"
        })
        bundle["objects"][1]["object_refs"].append(indicator_id)
        
    return bundle
