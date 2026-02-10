# omen-lights

Turn off HP Omen 35L (GT16-1xxx) chassis RGB lighting on Linux.

Sends a 58-byte USB HID command to disable the front diamond logo, interior light bar, and CPU cooler fan LEDs.

## Setup on Linux

### 1. Install system dependencies

```bash
# Debian/Ubuntu
sudo apt install python3-pip libhidapi-hidraw0

# Arch
sudo pacman -S python-pip hidapi

# Fedora
sudo dnf install python3-pip hidapi
```

### 2. Install udev rule (one-time, for non-root access)

```bash
sudo cp udev/99-hp-omen-lights.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 3. Install the tool

```bash
cd ~/claude/linux_lights
pip install --user -e .
```

## Usage

```bash
# Find your device and confirm VID:PID
omen-lights scan

# Turn off all chassis lights
omen-lights off
```

## Troubleshooting

- If `scan` finds nothing: check that `libhidapi-hidraw0` is installed and the udev rule is in place, then reboot.
- If the PID differs from `0x84FD`: `scan` will show the actual PID. Add it to `KNOWN_PIDS` in `omen_lights/device.py`.
- If permission denied: make sure the udev rule is installed and you've rebooted (or run `sudo udevadm trigger`).
