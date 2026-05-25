import json
import os
import requests
from http.server import BaseHTTPRequestHandler


SYSTEM_PROMPT = "You are AgentForge, an AI agent creation assistant. Help users design custom AI agents by suggesting personality traits, tool configurations, memory strategies, and goal hierarchies. Ask clarifying questions and provide structured agent blueprints."


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body) if body else {}
        user_input = data.get("input", "")

        try:
            mimo_key = os.environ.get("MIMO_API_KEY", "")
            mimo_url = os.environ.get("MIMO_BASE_URL", "https://llm.tbuglabs.com/v1")
            mimo_model = os.environ.get("MIMO_MODEL", "mimo/mimo-v2.5")

            resp = requests.post(
                f"{mimo_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {mimo_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": mimo_model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.8,
                    "max_tokens": 1500,
                    "stream": False
                },
                timeout=60
            )

            result = resp.json()
            reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No response.")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"response": reply}).encode())
        except Exception as e:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "agent": "AgentForge"}).encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
