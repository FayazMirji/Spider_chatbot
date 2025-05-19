from openai import AsyncOpenAI
import json
from agent.tools import fetch_documents_by_agency


client = AsyncOpenAI(base_url="http://localhost:11434/v1",api_key="ollama")

tools=[{
    "type":"function",
    "function":{"name":"fetch_documents_by_agency",
                "description":"Get document by agency name",
                "parameter":{
                    "type":"objects",
                    "properties":{
                        "agency":{"type":"string"}

                    },
                    "required":["agency"]
                }}
}]

async def call_agent(user_input:str):
    response=await client.chat.completions.create(
        model="qwen:0.5b",
        messages=[{"role":"user","content":user_input}],
        tools=tools,
        tool_choice="auto"
    )

    msg=response.choice[0].message

    if msg.tool_calls:
        tool_call=msg.tools_calls[0]
        func_name=tool_call.function.name
        args=json.loads(tool_call.function.arguments)

        if func_name == "fectch_documents_by_agency":
            results = await fetch_documents_by_agency(**args)
            follow_up=await client.chat.completions.create(model="qwen:0.5b",
                                                           messages=[
                                                               {"role":"user","content":user_input},
                                                               {"role":"assistant","tool_calls":[tool_call]},
                                                               {"role":"tool","tool_call_id":tool_call.id,"content":json.dumps(results)}])
        return follow_up.choices[0].message.content
    else:
        return msg.content




