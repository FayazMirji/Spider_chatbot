from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from agent.chat_agent import call_agent
import asyncio

app=FastAPI()

@app.get("/",response_class=HTMLResponse)
async def get_ui():
    return"""<html><body>
    <form action="query" placeholder="Ask me..."/>
    <button type="submit">Send</button>
    </form>
    </body></html>
    """

@app.post("/chat")
async def chat(request:Request):
    form = await request.form()
    user_input=form["query"]
    result=await call_agent(user_input)
    return HTMLResponse(f"<p><b>Response:</b>{result}</p><br><a href='/'>Go back</a>")

@app.get("/api/chat")
async def api_chat(query:str):
    result = await call_agent(query)
    return JSONResponse({"response":result})