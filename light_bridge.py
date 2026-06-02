from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

# Config - Change to your printer IP
PRINTER_IP = os.environ.get("PRINTER_IP", "192.168.1.44")
SSH_PASS = "rockchip"

def run_ssh(cmd):
    full_cmd = f"sshpass -p '{SSH_PASS}' ssh -o StrictHostKeyChecking=no root@{PRINTER_IP} \"{cmd}\""
    try:
        return subprocess.run(full_cmd, shell=True, capture_output=True, text=True, timeout=10).stdout.strip()
    except:
        return ""

@app.route("/light/on")
def on():
    run_ssh("echo 117 > /sys/class/gpio/export 2>/dev/null; echo out > /sys/class/gpio/gpio117/direction; echo 1 > /sys/class/gpio/gpio117/value")
    return jsonify({"result": "on"})

@app.route("/light/off")
def off():
    run_ssh("echo 0 > /sys/class/gpio/gpio117/value")
    return jsonify({"result": "off"})

@app.route("/light/status")
def status():
    val = run_ssh("cat /sys/class/gpio/gpio117/value")
    return jsonify({"result": "on" if val == "1" else "off"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
