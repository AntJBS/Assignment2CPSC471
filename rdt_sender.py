# rdt_receiver.py
import socket
import sys
from rdt_common import BUFFER_SIZE, make_packet, parse_packet
if len(sys.argv) != 3:
    print("Usage: python rdt_receiver.py listen_port output_file")
    sys.exit(1)
listen_port = int(sys.argv[1])
output_file = sys.argv[2]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", listen_port))
expected_seq = 0
last_good_seq = 1

with open(output_file, "wb") as f:
    while True:
        packet, sender_addr = sock.recvfrom(BUFFER_SIZE)
        # Fill in start
        # Parse packet and check checksum.
        # If DATA packet has expected seq, write payload and ACK it.
        # If DATA packet is duplicate, resend ACK for last_good_seq.
        # If packet is corrupt, ignore it or resend last ACK.
        # If FIN arrives, send FINACK and break.
        # Fill in end
sock.close()
print("Receiver complete.")