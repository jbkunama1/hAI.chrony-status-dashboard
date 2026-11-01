#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Python 3.9+
from flask import Flask, render_template

app = Flask(__name__)
ERROR_PREFIXES = ("Error running '", "Unexpected error running '")

# Chrony-Daemon laeuft im eigenen Container (hAI.Chrony) im selben Netzwerk
CHRONY_HOST = os.environ.get("CHRONY_HOST", "highfish1_chrony")
CHRONYC = f"chronyc -h {CHRONY_HOST}" if CHRONY_HOST else "chronyc"

# 'clients' ist per Netzwerk nicht erlaubt (501 Not authorised) -> Unix-Socket des Daemons
CHRONY_SOCKET = os.environ.get("CHRONY_SOCKET", "/run/chrony/chronyd.sock")

def run_command(cmd):
    try:
        output = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True,
            timeout=5
        )
    except subprocess.CalledProcessError as e:
        output = f"Error running '{cmd}':\n{e.output}"
    except Exception as e:
        output = f"Unexpected error running '{cmd}': {e}"
    return output.strip()

def command_failed(output):
    return not output or output.startswith(ERROR_PREFIXES)

# Template ruft command_failed(x) als Funktion auf -> Global noetig, Filter allein reicht nicht
app.jinja_env.globals['command_failed'] = command_failed
app.jinja_env.filters['command_failed'] = command_failed

def get_clients():
    if CHRONY_SOCKET and os.path.exists(CHRONY_SOCKET):
        clients = run_command(f"chronyc -h {CHRONY_SOCKET} -n clients")
        if not command_failed(clients):
            return clients
    clients = run_command(f"{CHRONYC} -n clients")
    if not command_failed(clients):
        return clients
    return (
        "Keine Client-Daten verfügbar.\n"
        "'clients' erlaubt chronyd nur über den lokalen Unix-Socket.\n"
        f"Socket-Volume nach {CHRONY_SOCKET} einhängen (siehe README).\n"
        "Außerdem in chrony.conf: 'noclientlog' deaktivieren und 'clientloglimit' > 0.\n\n"
        f"{clients or ''}"
    ).strip()

@app.route("/")
def index():
    # Zeiten
    now_local = datetime.now(ZoneInfo("Europe/Berlin"))
    now_utc = datetime.now(timezone.utc)

    # Chrony-Kommandos
    tracking = run_command(f"{CHRONYC} tracking")
    sources = run_command(f"{CHRONYC} sources -v")
    activity = run_command(f"{CHRONYC} activity")
    clients = get_clients()

    return render_template(
        "index.html",
        now_local=now_local.strftime("%A, %d.%m.%Y %H:%M:%S %Z"),
        now_utc=now_utc.strftime("%a %d.%m.%Y %H:%M:%S %Z"),
        tracking=tracking,
        sources=sources,
        activity=activity,
        clients=clients,
        refresh_seconds=60
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234, debug=False)
