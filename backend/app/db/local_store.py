import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from app.models.schemas import Patient, OncologyDates, CancerInfo, CareInfo, Flags

CSV_PATH = Path(__file__).parents[2] / "data" / "base_ficticia_jornada_oncologica_500.csv"

_patients: Dict[str, Patient] = {}

def _min_date(*vals):
    vals = [v for v in vals if pd.notna(v)]
    return min(vals).date() if vals else None

def load_patients():
    global _patients
    
    # leitura do arquivo csv
    df = pd.read_csv(
    CSV_PATH,
    sep=None,            # <- autodetecta ; , ou \t
    engine="python",
    encoding="utf-8-sig" # trata BOM
    )
    
    # só por segurança: remove espaços/bom nos nomes das colunas
    df.columns = [str(c).strip() for c in df.columns]
    
    # normaliza datas
    for col in ["diagnostico_data","cirurgia_data","quimioterapia_inicio","radioterapia_inicio","ultima_consulta","proxima_consulta"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", format="%Y-%m-%d")

    loaded = {}
    for _, r in df.iterrows():
        treatment_start = _min_date(r.get("quimioterapia_inicio"), r.get("radioterapia_inicio"), r.get("cirurgia_data"))
        alerta = str(r.get("alerta_atraso")).strip().lower() in ["1","true","sim","yes","y"]

        p = Patient(
            id=str(r["patient_id"]),
            name=str(r["nome_paciente"]),
            sex=str(r["sexo"]) if pd.notna(r["sexo"]) else None,
            age=int(r["idade"]) if pd.notna(r["idade"]) else None,
            oncology=OncologyDates(
                diagnosis_date=r["diagnostico_data"].date() if pd.notna(r["diagnostico_data"]) else None,
                staging_date=None,
                treatment_start_date=treatment_start,
            ),
            cancer=CancerInfo(type=str(r["tipo_cancer"]) if pd.notna(r["tipo_cancer"]) else None,
                              stage=str(r["estadiamento"]) if pd.notna(r["estadiamento"]) else None),
            care=CareInfo(
                last_visit=r["ultima_consulta"].date() if pd.notna(r["ultima_consulta"]) else None,
                next_visit=r["proxima_consulta"].date() if pd.notna(r["proxima_consulta"]) else None,
                status=str(r["status_jornada"]) if pd.notna(r["status_jornada"]) else None,
            ),
            flags=Flags(alerta_atraso=alerta, atraso_etapa=str(r["atraso_etapa"]) if pd.notna(r["atraso_etapa"]) else None),
            notes=str(r["notas_clinicas"]) if pd.notna(r["notas_clinicas"]) else None,
            meta={"source":"csv","ingested_at": datetime.utcnow().isoformat()+"Z"},
        )
        loaded[p.id] = p
    _patients = loaded

def all_patients() -> List[Patient]:
    return list(_patients.values())

def get_patient(pid: str) -> Patient | None:
    return _patients.get(pid)

def update_patient(pid: str, patch: dict) -> Patient | None:
    p = _patients.get(pid)
    if not p: return None
    # aplicar patch simples em campos conhecidos (aqui só oncologia e care para demo)
    if "oncology" in patch:
        for k, v in patch["oncology"].items():
            setattr(p.oncology, k, v)
    if "care" in patch:
        for k, v in patch["care"].items():
            setattr(p.care, k, v)
    _patients[pid] = p
    return p
