# backend/Dockerfile
# Usar uma imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner [cite: 1775]
WORKDIR /app

# Instalar as dependências (FastAPI e o servidor Uvicorn [cite: 830, 859])
RUN pip install fastapi uvicorn

# Copiar o código da aplicação para o contêiner [cite: 1714]
COPY app.py .

# Expor a porta que o Uvicorn irá rodar [cite: 1774]
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner rodar [cite: 1779]
# O host 0.0.0.0 permite conexões de fora do contêiner
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]