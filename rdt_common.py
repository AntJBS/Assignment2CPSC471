# rdt_common.py
import socket
MAX_PAYLOAD = 1024
TIMEOUT = 1.0
BUFFER_SIZE = 4096

# TEST TOGGLES
import random
# Normal Run
# TEST_MODE = False
# LOSE_RATE = .2
# CORRUPT_RATE = .2

# Loss Case
# TEST_MODE = True
# LOSE_RATE = 0.3
# CORRUPT_RATE = 0.0   

# Corruption Case
TEST_MODE = True
LOSE_RATE = 0.0
CORRUPT_RATE = 0.3

# Large File Case
# TEST_MODE = False

def send_packet_simulated(sock, packet, addr):
    if not TEST_MODE:
        sock.sendto(packet, addr)
        return
    rand = random.random()

    if rand < LOSE_RATE:
        print("[Simulation] This packet is corrupted!")
        return
    elif rand < (LOSE_RATE + CORRUPT_RATE):
        print("[Simulation] This packet is corrputed!")
        corrupted_pkt = bytearray(packet)
        if len(corrupted_pkt) > 0:
            corrupted_pkt[-1] ^= 0xFF
        sock.sendto(bytes(corrupted_pkt), addr)
    else:
        sock.sendto(packet, addr)


def checksum(packet_type, seq_num, payload):
    """Return a 16-bit checksum over packet fields and payload bytes."""
    # Fill in start
    header_str = f"{packet_type}|{seq_num}|{len(payload)}|"
    if isinstance(payload, str):
        payload = payload.encode("utf-8")

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
    chk = checksum(packet_type, seq_num, payload)
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
    chk = checksum(packet_type, seq_num, payload)
    is_length_valid = (len(payload) == expected_length)
    is_chk_valid = (chk == sent_sum)
    is_valid= is_length_valid == is_chk_valid
    return packet_type, seq_num, payload, is_valid
    # Fill in end