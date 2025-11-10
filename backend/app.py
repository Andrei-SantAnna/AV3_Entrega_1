
from fastapi import FastAPI, Request
import os
import time
from datetime import datetime

app = FastAPI()

# Pega o nome do servidor do variável de ambiente
SERVER_NAME = os.environ.get('SERVER_NAME', 'default-server')

@app.get("/")
def read_root(request: Request):
    
    # Simular alguma latência (ex: 10ms)
    start_time = time.time()
    time.sleep(0.01) # Simula 10ms de trabalho
    end_time = time.time()
    
    latency_ms = (end_time - start_time) * 1000

    return {
        "server": SERVER_NAME,
        "timestamp": datetime.now().isoformat(),
        "latency": f"{latency_ms:.2f} ms",
        "client_ip": request.client.host
    }