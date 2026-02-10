"""HP Omen chassis lighting HID protocol.

58-byte HID report that sets the lighting mode to OFF.
Based on the SignalRGB HP Omen plugin and OpenRGB HPOmen30LController.
"""

PACKET_SIZE = 58

# Protocol constants (bytes 1-2)
PROTO_BYTE1 = 0x3E
PROTO_BYTE2 = 0x12

# Animation modes
MODE_OFF = 0x05

# Module IDs
MODULE_ALL = 0x00


def build_off_packet(module_id: int = MODULE_ALL) -> bytes:
    """Build a 58-byte HID report that turns lights off.

    Packet layout:
      [0]  Report ID      = 0x00
      [1]  Protocol const = 0x3E
      [2]  Protocol const = 0x12
      [3]  Animation mode = 0x05 (Off)
      [48] Brightness     = 0x00
      [49] Mode selector  = 0x02
      [54] Module ID      = module_id
      [55] Power state    = 0x01
    """
    buf = bytearray(PACKET_SIZE)
    buf[0] = 0x00       # Report ID
    buf[1] = PROTO_BYTE1
    buf[2] = PROTO_BYTE2
    buf[3] = MODE_OFF
    buf[48] = 0x00      # Brightness off
    buf[49] = 0x02      # Mode selector
    buf[54] = module_id
    buf[55] = 0x01      # Power state
    return bytes(buf)
