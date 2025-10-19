from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import date, datetime

class OncologyDates(BaseModel):
    diagnosis_date: Optional[date] = None
    staging_date: Optional[date] = None  # a base não tem, fica None
    treatment_start_date: Optional[date] = None  # menor entre quimio/radio/cirurgia

class CancerInfo(BaseModel):
    type: Optional[str] = None       # tipo_cancer
    stage: Optional[str] = None      # estadiamento

class CareInfo(BaseModel):
    last_visit: Optional[date] = None      # ultima_consulta
    next_visit: Optional[date] = None      # proxima_consulta
    status: Optional[str] = None           # status_jornada

class Flags(BaseModel):
    atraso_diagnostico_estadiamento: bool = False
    atraso_estadiamento_tratamento: bool = False
    dias_atraso_diagnostico_estadiamento: Optional[int] = None
    dias_atraso_estadiamento_tratamento: Optional[int] = None

class Patient(BaseModel):
    id: str = Field(..., description="patient_id")
    name: str = Field(..., description="nome_paciente")
    sex: Optional[str] = None
    age: Optional[int] = None
    oncology: OncologyDates
    cancer: CancerInfo
    care: CareInfo
    flags: Flags
    notes: Optional[str] = None
    meta: dict = {}

class Alert(BaseModel):
    id: str
    patient_id: str
    type: Literal["DIAGNOSIS_TO_STAGING","STAGING_TO_TREATMENT","OTHER"]
    status: Literal["OPEN","ACK","RESOLVED"] = "OPEN"
    days_overdue: Optional[int] = None
    created_at: datetime
    last_check: datetime

class Message(BaseModel):
    patient_id: str
    sender: Literal["patient","doctor"]
    text: str
    ts: datetime

class ChatSummary(BaseModel):
    patient_id: str
    symptoms: List[str]
    highlights: List[str]
    suggested_questions: List[str]
    last_messages_preview: List[Message]
