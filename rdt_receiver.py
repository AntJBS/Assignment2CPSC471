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
        pkt_type, seq_num, payload, is_valid = parse_packet(packet)
        # If DATA packet has expected seq, write payload and ACK it.
        if pkt_type == "DATA":
            if seq_num == expected_seq:
                f.write(payload)
                ack_pkt = make_packet("ACK", seq_num)
                sock.sendto(ack_pkt, sender_addr)

                last_good_seq = seq_num
                expected_seq = 1 - expected_seq
            else:
                # If DATA packet is duplicate, resend ACK for last_good_seq.
                ack_pkt = make_packet("ACK", seq_num)
                sock.sendto(ack_pkt, sender_addr)
        # If packet is corrupt, ignore it or resend last ACK.
        if not is_valid:
            continue
        # If FIN arrives, send FINACK and break.
        if pkt_type == "FIN":
            finack_pkt = make_packet("FINACK", seq_num)
            sock.sendto(finack_pkt, sender_addr)
            break
        # Fill in end
sock.close()
print("Receiver complete.")