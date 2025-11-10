
# Usar uma imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner 
WORKDIR /app

# Instalar as dependências 
RUN pip install fastapi uvicorn

# Copiar o código da aplicação para o contêiner 
COPY app.py .

# Expor a porta que o Uvicorn irá rodar
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner rodar
# O host 0.0.0.0 permite conexões de fora do contêiner
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]