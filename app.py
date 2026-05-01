#!/usr/bin/env python3
import subprocess
from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Python 3.9+
from flask import Flask, render_template

app = Flask(__name__)

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
        output = f"Error running '{cmd}':
{e.output}"
    except Exception as e:
        output = f"Unexpected error running '{cmd}': {e}"
    return output.strip()

@app.route("/")
def index():
    # Zeiten
    now_local = datetime.now(ZoneInfo("Europe/Berlin"))
    now_utc = datetime.now(timezone.utc)

    # Chrony-Kommandos
    tracking = run_command("chronyc tracking")
    sources = run_command("chronyc sources -v")
    activity = run_command("chronyc activity")
    clients = run_command("chronyc clients")

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
    app.run(host="0.0.0.0", port=8000, debug=False)
