FROM python:3.9

# 1. Imposta la cartella di lavoro
WORKDIR /app

# 2. Copia solo il file dei requisiti (per ottimizzare la cache)
COPY requirements.txt .

# 3. ESEGUI l'installazione (Fase di BUILD)
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia il resto del codice
COPY ./main.py .

# 5. Comando di avvio (Fase di RUNTIME)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
