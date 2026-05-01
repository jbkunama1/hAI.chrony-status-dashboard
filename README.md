# ⏱️ highfish Chrony Status Dashboard

![Chrony LAN Logo](./assets/chrony-logo.png)

Ein leichtgewichtiges Web-Dashboard für deinen **Chrony LAN NTP Server**.  
Zeigt die wichtigsten Statusinfos deines Chrony-Dienstes direkt im Browser an – ideal für Homelab, Serverraum oder Monitoring-Screen. 🚀

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
