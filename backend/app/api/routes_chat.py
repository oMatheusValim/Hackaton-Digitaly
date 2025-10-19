from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.db.local_store import get_patient_by_id
from app.chat_bot import gerar_resumo_medico
import os

router = APIRouter(prefix="/chat", tags=["chat"])

# ---------- Schemas ----------
class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str

class ChatRequest(BaseModel):
    patient_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    answer: str
    used_llm: bool = True

# ---------- Util ----------
def _patient_context(patient_id: Optional[str]) -> str:
    if not patient_id:
        return ""
    p = get_patient_by_id(patient_id)
    if not p:
        raise HTTPException(404, "patient not found")
    return (
        f"Paciente: {p.name or '-'} | Sexo: {p.sex or '-'} | Idade: {p.age or '-'} | "
        f"Câncer: {getattr(p.cancer, 'type', None) or '-'} | Estágio: {getattr(p.cancer, 'stage', None) or '-'} | "
        f"Diagnóstico: {getattr(p.oncology, 'diagnosis_date', None) or '-'} | "
        f"Início tratamento: {getattr(p.oncology, 'treatment_start_date', None) or '-'} | "
        f"Última consulta: {getattr(p.care, 'last_visit', None) or '-'} | "
        f"Próxima consulta: {getattr(p.care, 'next_visit', None) or '-'} | "
        f"Status: {getattr(p.care, 'status', None) or '-'}"
    )

# ---------- Rota principal ----------
@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    patient_ctx = _patient_context(req.patient_id)

    system_prompt = (
        "Você é um assistente para jornada oncológica. Responda de forma clara, curta e útil. "
        "Se a pergunta exigir opinião médica, lembre que isso não substitui o médico responsável.\n"
    )
    if patient_ctx:
        system_prompt += f"\nContexto do paciente: {patient_ctx}\n"

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            messages = [{"role": "system", "content": system_prompt}]
            if req.history:
                for m in req.history:
                    if m.role in ("system", "user", "assistant") and m.content:
                        messages.append({"role": m.role, "content": m.content})
            messages.append({"role": "user", "content": req.message})

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.2,
                max_tokens=400,
            )
            answer = resp.choices[0].message.content.strip()
            return ChatResponse(answer=answer, used_llm=True)
        except Exception:
            pass  # fallback abaixo

    return ChatResponse(
        answer=(
            "Resposta (stub): backend ok! "
            + (f"[Contexto paciente: {patient_ctx}] " if patient_ctx else "")
            + f"Você perguntou: “{req.message}”."
        ),
        used_llm=False,
    )

# ---------- Geração de resumo ----------
@router.post("/summary")
def gerar_resumo(req: ChatRequest):
    if not req.patient_id:
        raise HTTPException(400, "patient_id obrigatório")

    p = get_patient_by_id(req.patient_id)
    if not p:
        raise HTTPException(404, "patient not found")

    summary_dict = gerar_resumo_medico(p.model_dump(), req.message)
    
    if "erro" in summary_dict:
        raise HTTPException(500, f"Falha ao gerar o resumo: {summary_dict['erro']}")

    return {"summary": summary_dict}

@router.post("/analisar")
def analisar_mensagem(req: ChatRequest):
    paciente = get_patient_by_id(req.patient_id)
    
    if not paciente:
        raise HTTPException(404, f"Paciente {req.patient_id} não encontrado")

    # A função já retorna um dicionário, então podemos retorná-lo diretamente.
    resultado_dict = gerar_resumo_medico(paciente.model_dump(), req.message)

    if "erro" in resultado_dict:
        raise HTTPException(500, f"Falha ao analisar a mensagem: {resultado_dict['erro']}")
    
    return resultado_dict
