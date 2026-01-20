FROM python:3.11-slim

WORKDIR /app

# 1) Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copiar código y modelo
COPY app ./app
COPY models ./models

# 3) Exponer puerto
EXPOSE 8000

# 4) Comando de arranque del servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
