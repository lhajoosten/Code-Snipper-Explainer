from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Code Assistant", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

api_v1 = APIRouter(prefix="/api/v1")


class ExplainRequest(BaseModel):
    code: str


class ExplainResponse(BaseModel):
    explanation: str
    line_count: int
    placeholder: bool = True


@api_v1.post("/explain", response_model=ExplainResponse)
async def explain(req: ExplainRequest):
    lines = req.code.count("\n") + 1 if req.code else 0
    return ExplainResponse(
        explanation="Hello World: This is a placeholder explanation. Replace with real handler later.",
        line_count=lines,
    )


@app.get("/api/ping")
async def ping():
    return {"status": "ok", "message": "pong"}


app.include_router(api_v1)
