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

@app.route("/")
def index():
    # Zeiten
    now_local = datetime.now(ZoneInfo("Europe/Berlin"))
    now_utc = datetime.now(timezone.utc)

    # Chrony-Kommandos
    tracking = run_command(f"{CHRONYC} tracking")
    sources = run_command(f"{CHRONYC} sources -v")
    activity = run_command(f"{CHRONYC} activity")
    clients = run_command(f"{CHRONYC} -n clients")
    if command_failed(clients):
        fallback_clients = run_command(f"{CHRONYC} clients")
        if not command_failed(fallback_clients):
            clients = fallback_clients
        else:
            clients = (
                "Keine Client-Daten verfügbar.\n"
                "Prüfe in chrony.conf: 'noclientlog' deaktivieren und 'clientloglimit' > 0.\n"
                "Stelle sicher, dass der Flask-User 'chronyc -n clients' ausführen darf.\n\n"
                f"{clients or fallback_clients or ''}"
            ).strip()

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
