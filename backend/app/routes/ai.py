from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.graph import graph

router = APIRouter(prefix="/ai", tags=["AI"])


class AIRequest(BaseModel):
    message: str




@router.post("/agent")
def run_agent(req: AIRequest):
    result = graph.invoke({"input": req.message})
    return result["output"]