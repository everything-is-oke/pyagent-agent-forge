import json
import os
import requests

def handler(request, response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    
    if request.method == "OPTIONS":
        response.status_code = 204
        return response
    
    if request.method != "POST":
        response.status_code = 405
        response.body = json.dumps({"error": "Method not allowed"})
        response.headers["Content-Type"] = "application/json"
        return response
    
    try:
        body = json.loads(request.body)
        user_input = body.get("input", "")
        
        mimo_key = os.environ.get("MIMO_API_KEY", "")
        mimo_url = os.environ.get("MIMO_BASE_URL", "https://llm.tbuglabs.com/v1")
        mimo_model = os.environ.get("MIMO_MODEL", "mimo/mimo-v2.5")
        
        api_response = requests.post(
            f"{mimo_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {mimo_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": mimo_model,
                "messages": [
                    {"role": "system", "content": "You are AgentForge, an AI agent creation assistant. Help users design custom AI agents by suggesting personality traits, tool configurations, memory strategies, and goal hierarchies. Ask clarifying questions and provide structured agent blueprints."},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.8,
                "max_tokens": 1500,
                "stream": False
            },
            timeout=60
        )
        
        data = api_response.json()
        reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
        
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({"response": reply})
    except Exception as e:
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps({"error": str(e)})
    
    return response