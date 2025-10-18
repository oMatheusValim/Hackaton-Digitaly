from fastapi import FastAPI

app = FastAPI(title="Chat Backend Oncologia")

@app.get("/health")
def health():
    return {"ok": True}
