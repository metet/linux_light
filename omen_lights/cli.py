"""CLI entry point for omen-lights."""

import argparse
import sys

from omen_lights.device import DeviceNotFoundError, enumerate_hp_hid, find_and_open, send
from omen_lights.protocol import build_off_packet


def cmd_off(args: argparse.Namespace) -> None:
    """Turn off all chassis lights."""
    try:
        dev = find_and_open()
    except DeviceNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        packet = build_off_packet()
        send(dev, packet)
        print("Lights turned off.")
    finally:
        dev.close()


def cmd_scan(args: argparse.Namespace) -> None:
    """List detected HP USB HID devices."""
    devices = enumerate_hp_hid()
    if not devices:
        print("No HP HID devices found.")
        print("Check that libhidapi is installed and udev rules are in place.")
        return

    print(f"Found {len(devices)} HP HID device(s):\n")
    for d in devices:
        pid = d["product_id"]
        product = d.get("product_string") or "(unknown)"
        path = d.get("path", b"").decode(errors="replace") if isinstance(d.get("path"), bytes) else d.get("path", "")
        print(f"  VID:PID  0x{d['vendor_id']:04X}:0x{pid:04X}")
        print(f"  Product  {product}")
        print(f"  Path     {path}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="omen-lights",
        description="Control HP Omen chassis RGB lighting on Linux.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("off", help="Turn off all chassis lights")
    sub.add_parser("scan", help="List detected HP USB HID devices")

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    {"off": cmd_off, "scan": cmd_scan}[args.command](args)


if __name__ == "__main__":
    main()
