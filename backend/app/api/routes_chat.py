# backend/app/api/routes_chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.db.local_store import get_patient
import os

router = APIRouter(prefix="/chat", tags=["chat"])

# ---------- Schemas ----------
class ChatMessage(BaseModel):
    role: str  # "user" | "assistant" | "system"
    content: str

class ChatRequest(BaseModel):
    message: str
    patient_id: Optional[str] = None
    history: Optional[List[ChatMessage]] = None  # opcional, para manter contexto no front

class ChatResponse(BaseModel):
    answer: str
    used_llm: bool = False

# ---------- Util ----------
def _patient_context(patient_id: Optional[str]) -> str:
    if not patient_id:
        return ""
    p = get_patient(patient_id)
    if not p:
        raise HTTPException(404, "patient not found")
    # Reduza o que você envia pro modelo (contexto enxuto)
    return (
        f"Paciente: {p.name or '-'} | Sexo: {p.sex or '-'} | Idade: {p.age or '-'} | "
        f"Câncer: {getattr(p.cancer, 'type', None) or '-'} | Estágio: {getattr(p.cancer, 'stage', None) or '-'} | "
        f"Diagnóstico: {getattr(p.oncology, 'diagnosis_date', None) or '-'} | "
        f"Início tratamento: {getattr(p.oncology, 'treatment_start_date', None) or '-'} | "
        f"Última consulta: {getattr(p.care, 'last_visit', None) or '-'} | "
        f"Próxima consulta: {getattr(p.care, 'next_visit', None) or '-'} | "
        f"Status: {getattr(p.care, 'status', None) or '-'}"
    )

# ---------- Rota ----------
@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Se OPENAI_API_KEY estiver configurada e o pacote 'openai' instalado,
    usa LLM. Caso contrário, devolve uma resposta stub para testes.
    """
    patient_ctx = _patient_context(req.patient_id)

    # Mensagem que vai para o modelo
    system_prompt = (
        "Você é um assistente para jornada oncológica. Responda de forma clara, curta e útil. "
        "Se a pergunta exigir opinião médica, lembre que isso não substitui o médico responsável.\n"
    )
    if patient_ctx:
        system_prompt += f"\nContexto do paciente (somente para referência): {patient_ctx}\n"

    # ---- Tenta usar LLM (opcional) ----
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            # Import local para não quebrar se lib não estiver instalada
            from openai import OpenAI
            client = OpenAI(api_key=api_key)

            # Monte o histórico (se vier do front) + mensagem atual
            messages = [{"role": "system", "content": system_prompt}]
            if req.history:
                for m in req.history:
                    if m.role in ("system", "user", "assistant") and m.content:
                        messages.append({"role": m.role, "content": m.content})
            messages.append({"role": "user", "content": req.message})

            # Você pode usar chat.completions ou responses; aqui uso chat.completions por simplicidade
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.2,
                max_tokens=400,
            )
            answer = resp.choices[0].message.content.strip()
            return ChatResponse(answer=answer, used_llm=True)
        except Exception as e:
            # Cai para stub se houver qualquer erro de dependência/config
            return ChatResponse(
                answer=(
                    "Não consegui acessar o modelo de IA agora, mas posso responder no modo de teste.\n"
                    f"Pergunta: {req.message}\n"
                    + (f"Contexto: {patient_ctx}\n" if patient_ctx else "")
                    + "Resposta (stub): Recebi sua pergunta e o backend está funcionando. 👍"
                ),
                used_llm=False,
            )


    # ---- Stub (sem LLM) ----
    return ChatResponse(
        answer=(
            "Resposta (stub): backend ok! "
            + (f"[Contexto paciente: {patient_ctx}] " if patient_ctx else "")
            + f"Você perguntou: “{req.message}”."
        ),
        used_llm=False,
    )
    
