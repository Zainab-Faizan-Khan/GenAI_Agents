from fastapi import FastAPI, Request
from graph.agent_graph import run_agent_graph

app = FastAPI()

@app.post("/query")
async def handle_query(request: Request):
    data = await request.json()
    query = data.get("query")
    result = run_agent_graph(query)
    return {"response": result}
