from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Investigation, Evidence
from app.reporting import (
    ReportGenerator, ReportFormat
)
from fastapi.responses import StreamingResponse
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{investigation_id}/summary")
async def get_investigation_summary(
    investigation_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Отримати резюме розслідування"""
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence = db.query(Evidence).filter(
        Evidence.investigation_id == investigation_id
    ).all()
    
    return {
        "investigation": {
            "id": investigation.id,
            "title": investigation.title,
            "target": investigation.target_identifier,
            "status": investigation.status,
            "created_at": investigation.created_at.isoformat()
        },
        "evidence_count": len(evidence),
        "tools_used": list(set(e.source for e in evidence))
    }

@router.post("/{investigation_id}/generate-report")
async def generate_investigation_report(
    investigation_id: str,
    format: str = Query("json"),
    include_analysis: bool = Query(True),
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    """Згенерувати ЗАГАЛЬНИЙ ЗВІТ розслідування"""
    
    investigation = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()
    
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found")
    
    evidence_list = db.query(Evidence).filter(
        Evidence.investigation_id == investigation_id
    ).all()
    
    # Ініціалізувати звіт
    report = ReportGenerator(investigation_id)
    report.add_executive_summary(
        target=investigation.target_identifier,
        findings=investigation.description or "OSINT дослідження",
        risk_level="UNKNOWN"
    )
    
    # Додати докази до звіту
    for evidence in evidence_list:
        try:
            data = json.loads(evidence.data) if isinstance(evidence.data, str) else evidence.data
        except:
            data = {"raw": evidence.data}
        
        # Автоматичний розподіл за категоріями в звіті
        if evidence.source in ["maigret", "sherlock"]:
            report.add_osint_search_results(investigation.target_identifier, [data])
        elif evidence.source in ["shodan", "censys"]:
            report.add_network_intelligence([data])
        elif evidence.source in ["geospy", "google_earth"]:
            report.add_geolocation_data([data])
    
    # Генерація виводу
    if format == "pdf":
        pdf_bytes = report.to_pdf()
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=report_{investigation_id}.pdf"}
        )
    
    return report.report_data
