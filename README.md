# Raspberry Pi Home-Lab: Containerized Infrastructure Stack

Un'infrastruttura containerizzata su Raspberry Pi con reverse proxy, backend applicativo, database isolato e observability stack completo.

---

## Overview

Questo progetto nasce come lab personale per mettere in pratica architetture reali in ambiente domestico. L'obiettivo non era solo "far girare qualcosa", ma prendere decisioni architetturali consapevoli: network isolation, service discovery interno, separazione dei layer applicativi.

Lo stack è interamente definito via Docker Compose e gira su Raspberry Pi (ARM64).

---

## Stack

| Layer | Tecnologia |
|---|---|
| Reverse Proxy | Nginx |
| Backend | Python + Uvicorn |
| Database | Redis |
| Metrics Collection | Prometheus |
| Visualization | Grafana |
| Container Metrics | cAdvisor |
| OS Metrics | Node Exporter |
| Notifiche | Discord Bot (custom) |
| Runtime | Docker + Docker Compose |

---

## Architettura
```
                    ┌─────────────────────────────┐
    Internet ──────►│     Nginx (Reverse Proxy)   │ :3000
                    └──────────────┬──────────────┘
                                   │ network: app-net
                    ┌──────────────▼──────────────┐
                    │    Python Backend (Uvicorn) │
                    └──────────────┬──────────────┘
     ------------------------------│-network: db-net----------------
                    ┌──────────────▼──────────────┐
                    │            Redis            │
                    └─────────────────────────────┘

                    ┌─────────────────────────────┐
                    │   Prometheus + Grafana      │ :4000
                    │   cAdvisor + Node Exporter  │
                    └─────────────────────────────┘
```

**Scelte architetturali:**

- **Network isolation a due livelli** — Nginx e backend condividono `app-net`; backend e Redis condividono `db-net`. Redis non è raggiungibile dal proxy, né espone porte verso l'host.
- **Service discovery via Docker DNS** — I servizi comunicano per nome container (`http://backend:8000`, `http://cadvisor:8080`). Zero IP hardcoded, zero configurazione manuale.
- **Named volumes** — Dati di Prometheus e configurazioni Grafana persistono tra ricreazioni dei container.
- **Nessuna porta sensibile esposta sull'host** — Node Exporter gira dentro la bridge network, con `/proc` e `/sys` montati come volumi. Niente fori nel firewall.

---

## Observability

Prometheus raccoglie metriche da cAdvisor (container-level) e Node Exporter (OS-level). Grafana le visualizza su dashboard personalizzate, incluse metriche specifiche per ARM come la temperatura della CPU del Raspberry.

_Dashboard di riferimento:_ [1860](https://grafana.com/grafana/dashboards/1860)

---

## Discord Bot

Senza IP fisso, accedere ai servizi dall'esterno richiede di conoscere l'IP corrente. Il bot si connette a un server Discord e notifica l'indirizzo aggiornato in formato `http://{ip}:{porta}` ogni volta che cambia.

---

## Setup
```bash
git clone https://github.com/tuousername/rpi-homelab.git
cd rpi-homelab
docker compose up -d
```

| Servizio | URL |
|---|---|
| Applicazione | http://IP_HOST:3000 |
| Grafana | http://IP_HOST:4000 |

---

## ❗ Attenzione - Se si vuole fare uso del bot discord 
Per avviare l'infrastruttura, crea un file `.env` nella **radice del progetto** (puoi rinominare e compilare il file `.env.example` incluso, ricordati di renderlo nascosto). L'unico parametro essenziale per le notifiche è l'URL del Webhook di Discord; se preferisci non utilizzare il sistema di alert, è sufficiente commentare o rimuovere il servizio `discord_bot` dal file `compose.yaml` prima del deploy.

```text
rpi-monitoring-stack/
├── .env              <-- Crea questo file
├── env.example      <-- Oppure rinomina questo --> .env.example
├── compose.yaml
└── ...
```
---

## Problemi risolti

**Prometheus non raggiungeva Node Exporter** — Il problema era UFW che bloccava il traffico verso `localhost:9100`. Invece di aprire la porta sul firewall dell'host, ho spostato Node Exporter dentro la bridge network e montato `/proc` e `/sys` come volumi. Comunicazione container-native, superficie di attacco invariata.

---

## Roadmap

- [x] Reverse proxy con Nginx
- [x] Backend Python + Redis con network isolation
- [x] Monitoring stack (Prometheus, Grafana, cAdvisor, Node Exporter)
- [x] Discord bot per IP discovery
- [ ] Instaurare una sessione permanente con volumi Redis e dati salvati
- [ ] Mappatura dei volumi per cambiamenti applicazione in tempo reale 
- [ ] Log aggregation con Loki + Promtail
- [ ] Provisioning automatizzato con Ansible
- [ ] IaC con Terraform (per eventuale deploy cloud)
