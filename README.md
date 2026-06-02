# Anycubic Kobra S1 Chamber Light Bridge

This tool allows you to control the chamber/nozzle light of an Anycubic Kobra S1 when running Klipper on a remote host (like a laptop or Raspberry Pi) via a network tunnel.

## How it works
The Kobra S1 chamber light is controlled by **GPIO 117** on the printer's SoC. Standard Klipper running on a remote host cannot access this pin. This bridge creates a small Flask API on your Klipper host that sends SSH commands to the printer to toggle the GPIO.

## Installation
1. Clone this repo to your Klipper host:
   ```bash
   git clone https://github.com/YOUR_USERNAME/kobra-s1-light-bridge.git
   cd kobra-s1-light-bridge
   ```
2. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
3. Follow the instructions to update your `moonraker.conf` and `printer.cfg`.

## Configuration

### Moonraker
Add the following to your `moonraker.conf` to get a toggle button in Mainsail:
```ini
[power ChamberLight]
type: http
on_url: http://localhost:5001/light/on
off_url: http://localhost:5001/light/off
status_url: http://localhost:5001/light/status
response_template:
  {% set resp = http_request.last_response().json() %}
  {resp["result"]}
```

### Klipper Macros
Add these to your `printer.cfg` to use the light in G-code:
```cfg
[gcode_macro CHAMBER_LIGHT_ON]
gcode:
  {action_call_remote_method("set_device_power", device="ChamberLight", state="on")}

[gcode_macro CHAMBER_LIGHT_OFF]
gcode:
  {action_call_remote_method("set_device_power", device="ChamberLight", state="off")}
```

## Credits
Special thanks to the Anycubic Klipper community for identifying GPIO 117.
