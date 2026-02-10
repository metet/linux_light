"""CLI entry point for omen-lights."""

import argparse
import sys

from omen_lights.device import DeviceNotFoundError, enumerate_hp_hid, find_and_open, send
from omen_lights.protocol import ALL_MODULES, build_off_packet


def cmd_off(args: argparse.Namespace) -> None:
    """Turn off all chassis lights."""
    import hid

    devices = enumerate_hp_hid()
    if not devices:
        print("No HP HID devices found.", file=sys.stderr)
        sys.exit(1)

    # Deduplicate by path
    seen_paths = set()
    unique_devices = []
    for d in devices:
        path = d["path"]
        if path not in seen_paths:
            seen_paths.add(path)
            unique_devices.append(d)

    for info in unique_devices:
        path = info["path"]
        path_str = path.decode(errors="replace") if isinstance(path, bytes) else path
        try:
            dev = hid.Device(path=path)
        except Exception as e:
            print(f"  Skipping {path_str}: {e}")
            continue
        try:
            for module_id in ALL_MODULES:
                packet = build_off_packet(module_id)
                try:
                    send(dev, packet)
                except Exception:
                    break
            else:
                print(f"  Sent off to {path_str}")
                continue
            print(f"  Skipping {path_str}: write failed")
        finally:
            dev.close()

    print("Lights turned off.")


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
