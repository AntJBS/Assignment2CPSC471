# rdt_common.py
import socket
MAX_PAYLOAD = 1024
TIMEOUT = 1.0
BUFFER_SIZE = 4096
def checksum(packet_type, seq_num, payload):
    """Return a 16-bit checksum over packet fields and payload bytes."""
    # Fill in start
    header_str = f"{packet_type}|{seq_num}|{len(payload)}|"
    data = header_str.encode("utf-8") + payload

    if len(data) % 2 != 0 :
        data += b"\x00"

    s = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i+1]
        s+= word
        s = (s & 0xFFFF) + (s >> 16)
    return ~s & 0xFFFF
    # Fill in end
def make_packet(packet_type, seq_num, payload=b""):
    """Build TYPE|SEQ|LENGTH|CHECKSUM\nPAYLOAD as bytes."""
    length = len(payload)
    # Fill in start
    chk = checksum(packet_type, seq_num, length)
    header = f"{packet_type}|{seq_num}|{len(payload)}|{chk}\n"
    return header.encode("utf-8") + payload
    # Fill in end
def parse_packet(packet):
    """Return packet_type, seq_num, payload, is_valid."""
    try:
        header, payload = packet.split(b"\n", 1)
        packet_type, seq, length, sent_sum = header.decode().split("|")
        seq_num = int(seq)
        expected_length = int(length)
        sent_sum = int(sent_sum)
    except Exception:
        return None, None, b"", False
    
    # Fill in start

    # Verify length and checksum.
    chk = checksum(packet_type, seq_num, length)
    is_length_valid = (len(payload) == expected_length)
    is_chk_valid = (chk == sent_sum)
    is_valid= is_length_valid == is_chk_valid
    return packet_type, seq_num, payload, is_valid
    # Fill in end