# rdt_sender.py
import socket
import sys
from rdt_common import BUFFER_SIZE, MAX_PAYLOAD, TIMEOUT, make_packet, parse_packet
if len(sys.argv) != 4:
    print("Usage: python rdt_sender.py receiver_host receiver_port input_file")
    sys.exit(1)
receiver_host = sys.argv[1]
receiver_port = int(sys.argv[2])
input_file = sys.argv[3]
receiver_addr = (receiver_host, receiver_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)
seq = 0
with open(input_file, "rb") as f:
    while True:
        data = f.read(MAX_PAYLOAD)
        if not data:
            break
        acked = False
        while not acked:
            # Fill in start
            # Send DATA packet for current seq.
            # Wait for ACK.
            # If ACK is valid and matches seq, set acked = True.
            # If timeout occurs, retransmit this same packet.
            # Fill in end
        seq = 1 - seq
# Fill in start
# Send FIN until a valid FINACK is received.
# Fill in end

sock.close()
print("Transfer complete.")