from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from datetime import date
from app.db.local_store import all_patients, get_patient, update_patient
from app.models.schemas import Patient

router = APIRouter(prefix="/patients", tags=["patients"])

# Schemas de PATCH para validação/conversão automática:
class OncologyPatch(BaseModel):
    diagnosis_date: Optional[date] = None
    staging_date: Optional[date] = None
    treatment_start_date: Optional[date] = None

class CarePatch(BaseModel):
    last_visit: Optional[date] = None
    next_visit: Optional[date] = None
    status: Optional[str] = None

class PatientPatch(BaseModel):
    oncology: Optional[OncologyPatch] = None
    care: Optional[CarePatch] = None

@router.get("", response_model=List[Patient])
def list_patients(
    q: Optional[str] = Query(None, description="Busca por nome (contém)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    pts = all_patients()
    if q:
        ql = q.lower()
        pts = [p for p in pts if p.name and ql in p.name.lower()]
    return pts[offset: offset + limit]

@router.get("/{pid}", response_model=Patient)
def read_patient(pid: str):
    p = get_patient(pid)
    if not p:
        raise HTTPException(404, "patient not found")
    return p

@router.patch("/{pid}", response_model=Patient)
def patch_patient(pid: str, patch: PatientPatch):
    # Converte Pydantic -> dict enxuto
    data = patch.model_dump(exclude_none=True)
    p = update_patient(pid, data)
    if not p:
        raise HTTPException(404, "patient not found")
    return p

@router.get("/search", response_model=List[Patient])
def search_patients(
    q: Optional[str] = Query(None, description="Busca por nome (contém)"),
    cancer_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    only_delayed: bool = Query(False, description="Apenas com alerta_atraso=True"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    pts = all_patients()
    if q:
        ql = q.lower()
        pts = [p for p in pts if p.name and ql in p.name.lower()]
    if cancer_type:
        pts = [p for p in pts if (getattr(p.cancer, "type", None) or "").lower() == cancer_type.lower()]
    if status:
        pts = [p for p in pts if (getattr(p.care, "status", None) or "").lower() == status.lower()]
    if only_delayed:
        pts = [p for p in pts if getattr(p.flags, "alerta_atraso", False)]
    return pts[offset: offset + limit]

@router.get("/cancer-types", response_model=List[str])
def list_cancer_types():
    tipos = set()
    for p in all_patients():
        t = getattr(getattr(p, "cancer", None), "type", None)
        if t:
            tipos.add(str(t).strip())
    return sorted(tipos, key=str.casefold)