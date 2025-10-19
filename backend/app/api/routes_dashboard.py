from fastapi import APIRouter
from app.db.local_store import all_patients

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/alertas")
def listar_alertas():
    pts = all_patients()
    total = len(pts)
    atrasos = [p for p in pts if p.flags.atraso_estadiamento_tratamento]
    return {
        "total_pacientes": total,
        "pacientes_com_atraso": len(atrasos),
        "percentual_atraso": round(len(atrasos) / total * 100, 2) if total else 0
    }
