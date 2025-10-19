from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.local_store import load_patients
from app.api import routes_patients, routes_chat, routes_dashboard

# Cria o app FastAPI
app = FastAPI(title="Chat Backend Oncologia")

# Inclui as rotas
app.include_router(routes_patients.router)
app.include_router(routes_chat.router)
app.include_router(routes_dashboard.router)

# Carrega pacientes ao iniciar
@app.on_event("startup")
def _startup():
    print("🔄 Carregando pacientes...")
    load_patients()
    print("✅ Pacientes carregados com sucesso!")


# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste se quiser restringir domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
