# ⏱️ highfish Chrony Status Dashboard[![Buy me a coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://www.buymeacoffee.com/highfish)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)](https://github.com/jbkunama1/hAI.chrony-status-dashboard)
[![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/jbkunama1/hAI.chrony-status-dashboard)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://github.com/jbkunama1/hAI.chrony-status-dashboard)
[![GHCR](https://img.shields.io/badge/GHCR-published-blue?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jbkunama1/hAI.chrony-status-dashboard/pkgs/container/hAI.chrony-status-dashboard)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)




![Chrony LAN Logo](chrony-logo.png)

Ein leichtgewichtiges Web-Dashboard für deinen **Chrony LAN NTP Server**.  
Zeigt die wichtigsten Statusinfos deines Chrony-Dienstes direkt im Browser an – ideal für Homelab, Serverraum oder Monitoring-Screen. 🚀

---

## 🚀 Deployment

### Docker
```bash
docker run -d \
  --name chrony-status-dashboard \
  -p 1234:5000 \
  ghcr.io/jbkunama1/hai.chrony-status-dashboard:latest
```

### Portainer Stack
```yaml
version: '3.8'
services:
  chrony-status-dashboard:
    image: ghcr.io/jbkunama1/hai.chrony-status-dashboard:latest
    container_name: chrony-status-dashboard
    restart: unless-stopped
    ports:
      - "5000:5000"
    networks:
      - highfishNetwork
networks:
  highfishNetwork:
    external: true
```

### GitHub Actions (automatic)
- Build & Push to GHCR on push to `main`
- Build on PR merge

---

## ✨ Features

- 🔁 Automatisch aktualisierte Statusseite (konfigurierbares Reload-Intervall)
- ⏳ Anzeige der aktuellen lokalen Zeit (Europe/Berlin) und UTC
- 📊 Darstellung zentraler Chrony-Kommandos:
  - `chronyc tracking`
  - `chronyc sources -v`
  - `chronyc activity`
  - `chronyc clients`
- 💻 Einfache, dunkle UI mit monospaced Ausgabe – perfekt zum Lesen von NTP-Daten
- 🧩 Minimaler Tech-Stack: Python + Flask + Chrony

---

## 🧠 Was ist Chrony?

[Chrony](https://chrony-project.org/) ist eine moderne Implementierung des **Network Time Protocol (NTP)** und synchronisiert die Systemzeit deines Servers mit externen Zeitquellen (z. B. PTB, Google, Cloudflare).[web:9]  
Über die Kommandoschnittstelle `chronyc` lassen sich Statusinformationen wie Offset, Stratum, verwendete Server und Aktivität auslesen.[web:4]

Dieses Dashboard stellt genau diese Informationen übersichtlich im Browser dar.

---

## 🏗️ Architektur

```text
Browser ──HTTP──> Flask-App ──shell──> chronyc (tracking, sources, activity, clients)
         <─HTML──             <─Text─
