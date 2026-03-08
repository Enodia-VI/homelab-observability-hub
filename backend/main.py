from fastapi import FastAPI
from redis import Redis
import os

app = FastAPI()

# Configuriamo la connessione a Redis usando le variabili d'ambiente di Docker
# 'redis-lab' è il nome del servizio che hai scritto nel docker-compose.yml
redis_client = Redis(
    host=os.getenv("REDIS_HOST", "database"),
    port=6379,
    #password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

@app.get("/")
def read_root():
    return {"messaggio": "Benvenuto nel tuo Home-Lab!"}

@app.get("/incrementa")
def incrementa_contatore():
    # Operazione su Redis: incrementa una chiave chiamata 'visite'
    nuovo_valore = redis_client.incr("visite")
    return { "visite": nuovo_valore }
