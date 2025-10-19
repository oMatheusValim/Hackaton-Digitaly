from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.local_store import load_patients
from app.api import routes_patients, routes_chat, routes_dashboard

app = FastAPI(title="Chat Backend Oncologia")
app.include_router(routes_dashboard.router)

@app.on_event("startup")
def _startup():
    load_patients()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_patients.router)
app.include_router(routes_chat.router)

@app.get("/health")
def health():
    return {"ok": True}
