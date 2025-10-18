from fastapi import FastAPI
from app.db.local_store import load_patients
from app.api import routes_patients  # <-- importa o router

app = FastAPI(title="Chat Backend Oncologia")

@app.on_event("startup")
def _startup():
    load_patients()  # carrega o CSV na memória ao iniciar

# registra as rotas de pacientes
app.include_router(routes_patients.router)

@app.get("/health")
def health():
    return {"ok": True}
