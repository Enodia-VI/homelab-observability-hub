import subprocess
import requests
import os
from dotenv import load_dotenv

webhook = os.getenv('DISCORD_WEBHOOK_URL')
port = os.getenv('HTTP_PORT')

def get_ip_bash():
    try:
        # 'hostname -I' restituisce solo gli indirizzi IP separati da spazi
        # È più pulito di 'ip addr' da elaborare in Python
        output = subprocess.check_output(["hostname", "-I"]).decode('utf-8')
        # Prendiamo il primo IP della lista (solitamente quello della eth0 o wlan0)
        ip_principale = output.split()[0]
        return ip_principale
    except Exception as e:
        return f"Errore nel recupero IP: {e}"


def invia_a_discord():
    # Chiamiamo la tua funzione per avere l'IP
    mio_ip = get_ip_bash()

    # Prepariamo il "pacchetto" (JSON) da mandare a Discord
    # Puoi usare il Markdown di Discord (es. il grassetto ** o il codice `)
    data = {
        "content": f" **Raspberry Pi Online!**\nL'indirizzo IP locale è: http://{mio_ip}:{port}",
        "username": "Araldo del Lab"
    }

    # 2. Inviamo fisicamente l'informazione
    try:
        response = requests.post(webhook, json=data)
        if response.status_code == 204:
            print("Messaggio inviato con successo!")
        else:
            print(f"Errore Discord: {response.status_code}")
    except Exception as e:
        print(f"Errore di connessione: {e}")

if __name__ == "__main__":
    invia_a_discord()
