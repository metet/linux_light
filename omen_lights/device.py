"""HP Omen HID device discovery and I/O."""

import hid

HP_VIDS = {0x103C, 0x03F0}

# Known lighting-controller PIDs (add new ones here)
KNOWN_PIDS = {
    0x84FD,  # Omen 25L / 30L
    0x7397,  # Omen 35L (GT16-1xxx) "LCD-PUMP"
}


class DeviceNotFoundError(Exception):
    pass


def enumerate_hp_hid() -> list[dict]:
    """List all HP HID devices (VID 0x103C)."""
    return [d for d in hid.enumerate() if d["vendor_id"] in HP_VIDS]


def find_and_open() -> hid.Device:
    """Auto-discover and open the first matching Omen lighting controller.

    Tries known PIDs first, then falls back to any HP HID device.
    Raises DeviceNotFoundError with actionable guidance on failure.
    """
    # Try known PIDs first
    for info in hid.enumerate():
        if info["vendor_id"] in HP_VIDS and info["product_id"] in KNOWN_PIDS:
            dev = hid.Device(path=info["path"])
            return dev

    # Fall back: open any HP HID device (helps on unknown-PID hardware)
    hp_devices = enumerate_hp_hid()
    if hp_devices:
        dev = hid.Device(path=hp_devices[0]["path"])
        return dev

    raise DeviceNotFoundError(
        "No HP Omen lighting controller found.\n"
        "  1. Run 'omen-lights scan' to check detected devices.\n"
        "  2. Ensure the udev rule is installed:\n"
        "       sudo cp udev/99-hp-omen-lights.rules /etc/udev/rules.d/\n"
        "       sudo udevadm control --reload-rules && sudo udevadm trigger\n"
        "  3. Unplug and replug the USB header (or reboot)."
    )


def send(dev: hid.Device, packet: bytes) -> None:
    """Send a HID report to the device."""
    dev.write(packet)
