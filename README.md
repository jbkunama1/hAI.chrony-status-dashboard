# hAI.chrony-status-dashboard
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)](https://github.com/jbkunama1/hAI.chrony-status-dashboard)
[![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/jbkunama1/hAI.chrony-status-dashboard)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://github.com/jbkunama1/hAI.chrony-status-dashboard)
[![GHCR](https://img.shields.io/badge/GHCR-published-blue?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jbkunama1/hAI.chrony-status-dashboard/pkgs/container/hai.chrony-status-dashboard)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)




[![Buy me a coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/highfish)

![Chrony Logo](chrony-logo.png)

> **Web-Dashboard für deinen Chrony-NTP-Server** – Flask-App, die `chronyc` gegen einen Chrony-Daemon ausführt und die Ausgabe im Browser darstellt. Docker-basiert, keine Datenbank.

---

## Features

- ⏳ **Uhrzeit** – lokale Zeit (Europe/Berlin) und UTC
- 📊 **Chrony-Status** – `tracking`, `sources -v`, `activity`, `clients`
- 🔁 **Auto-Refresh** – Seite lädt alle 60 Sekunden neu
- 🟥 **Fehleranzeige** – fehlgeschlagene Befehle werden rot markiert
- 🌙 **Dark/Light Mode** – per Klick umschaltbar
- 📱 **Mobil nutzbar** – responsive Oberfläche
- ⚙️ **Per Env konfigurierbar** – Chrony-Host, Socket, Volume und Port
- 🧩 **Minimaler Stack** – Python + Flask + chronyc

---

## Schnellstart

### Voraussetzungen
- Docker (+ Docker Compose oder Portainer)
- Laufender Chrony-Daemon, z. B. [hAI.Chrony](https://github.com/jbkunama1/hAI.Chrony) (Container `highfish1_chrony`)
- Docker-Netzwerk `highfishnetwork` (extern)
- Im Chrony: `bindcmdaddress` und `cmdallow` so gesetzt, dass das Dashboard zugreifen darf
- Für die Clients-Ansicht: Volume `/run/chrony` des Chrony-Containers (enthält `chronyd.sock`)

### Docker

```bash
docker run -d \
  --name chrony-status-dashboard \
  --restart unless-stopped \
  --network highfishnetwork \
  -e CHRONY_HOST=highfish1_chrony \
  -v highfish1_chrony_run:/run/chrony \
  -p 1234:1234 \
  ghcr.io/jbkunama1/hai.chrony-status-dashboard:latest
```

Danach erreichbar unter: **http://localhost:1234**

### Portainer Stack

```yaml
services:
  chrony-status-dashboard:
    image: ghcr.io/jbkunama1/hai.chrony-status-dashboard:latest
    container_name: chrony-status-dashboard
    restart: unless-stopped
    environment:
      CHRONY_HOST: ${CHRONY_HOST:-highfish1_chrony}
      CHRONY_SOCKET: ${CHRONY_SOCKET:-/run/chrony/chronyd.sock}
    ports:
      - "${DASHBOARD_PORT:-1234}:1234"
    volumes:
      - chrony_run:/run/chrony
    networks:
      - highfishnetwork

volumes:
  chrony_run:
    external: true
    name: ${CHRONY_RUN_VOLUME:-highfish1_chrony_run}

networks:
  highfishnetwork:
    external: true
```

### Lokal bauen

```bash
git clone https://github.com/jbkunama1/hAI.chrony-status-dashboard.git
cd hAI.chrony-status-dashboard
docker compose up -d --build
```

---

## Konfiguration

| Variable | Default | Beschreibung |
|---|---|---|
| `CHRONY_HOST` | `highfish1_chrony` | Hostname oder IP des Chrony-Daemons. Leer = lokales `chronyc` |
| `CHRONY_SOCKET` | `/run/chrony/chronyd.sock` | Unix-Socket für die Clients-Abfrage |
| `CHRONY_RUN_VOLUME` | `highfish1_chrony_run` | Name des externen Docker-Volumes mit `/run/chrony` des Chrony-Containers |
| `DASHBOARD_PORT` | `1234` | Host-Port des Dashboards (Container-intern immer 1234) |

In Portainer: Stack → *Environment variables* → Werte eintragen → Update the stack.

Volume-Name prüfen:

```bash
docker inspect highfish1_chrony --format '{{range .Mounts}}{{.Name}} -> {{.Destination}}{{"\n"}}{{end}}'
```

---

## Update

- **Portainer:** Stack → Update → *Re-pull image* aktivieren → Update the stack
- **Lokal:** `git pull && docker compose up -d --build`

---

## Hinweis: Zugriff auf chronyd

Das Image enthält nur den Client `chronyc`, **keinen** `chronyd`. Das Dashboard fragt den Daemon so ab:

- `tracking`, `sources`, `activity` → per Netzwerk (`chronyc -h $CHRONY_HOST`, UDP 323)
- `clients` → per Unix-Socket (`CHRONY_SOCKET`), weil `chronyd` diesen Befehl per Netzwerk mit `501 Not authorised` ablehnt

Anforderungen am Chrony-Daemon:
- Dashboard und Chrony im selben Docker-Netzwerk (`highfishnetwork`)
- In der `chrony.conf`: `bindcmdaddress 0.0.0.0` und passendes `cmdallow`
- Socket-Volume im Dashboard eingehängt (siehe Stack)
- Für die Clients-Ansicht: `noclientlog` deaktivieren und `clientloglimit` > 0 setzen

---

## Projektstruktur

```
hAI.chrony-status-dashboard/
├── app.py              # Flask-App, führt chronyc aus
├── templates/
│   └── index.html      # Dashboard-Seite
├── static/
│   ├── style.css
│   └── theme.js        # Dark/Light-Toggle
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── docs/MEMORY.md
└── .github/workflows/  # GHCR-Build, TruffleHog
```

---

## Architektur

```text
Browser ──HTTP :1234──> Flask-App ──chronyc -h CHRONY_HOST (UDP 323)──> Chrony-Container
         <─HTML─────────             └─chronyc -h chronyd.sock (Volume)──> clients
```

---

## CI / GHCR

- Push auf `main` → Build und Push nach `ghcr.io/jbkunama1/hai.chrony-status-dashboard:latest`
- Build auch nach PR-Merge und manuell (`workflow_dispatch`)
- Den tatsächlichen Status unter [Actions](https://github.com/jbkunama1/hAI.chrony-status-dashboard/actions) prüfen

---

## Troubleshooting

| Problem | Prüfen |
|---|---|
| `506 Cannot talk to daemon` | `CHRONY_HOST` korrekt? Chrony-Container läuft, selbes Netzwerk? `cmdallow`/`bindcmdaddress` gesetzt? |
| Host unbekannt / nicht auflösbar | Containername stimmt? Beide im `highfishnetwork`? |
| `501 Not authorised` bei Clients | Socket-Volume eingehängt? `CHRONY_RUN_VOLUME` = tatsächlicher Volume-Name? |
| Clients-Box zeigt Hinweistext | `ls -l /run/chrony` im Dashboard-Container: liegt dort `chronyd.sock`? |
| Clients-Box leer | `noclientlog` aus, `clientloglimit` > 0 |
| Volume `... not found` beim Deploy | Volume-Name per `docker volume ls \| grep chrony_run` prüfen |
| Seite zeigt 500 / `command_failed is undefined` | Aktuelles Image ziehen (Fix seit Commit `3fb2f32`) |
| `manifest unknown` / `denied` beim Pull | Build erfolgreich? GHCR-Paket öffentlich? |
| Port belegt | `DASHBOARD_PORT` ändern, z. B. `8234` |
| Netzwerk nicht gefunden | `docker network create highfishnetwork` |

Tests direkt im Container:

```bash
docker exec chrony-status-dashboard chronyc -h highfish1_chrony tracking
docker exec chrony-status-dashboard chronyc -h /run/chrony/chronyd.sock -n clients
```

---

## Lizenz

MIT – siehe [LICENSE](LICENSE)
