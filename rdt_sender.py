# rdt_sender.py
# MORE TEST STUFF
import socket
import sys
from rdt_common import BUFFER_SIZE, MAX_PAYLOAD, TIMEOUT, make_packet, parse_packet, send_packet_simulated

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
            # Send DATA packet for current seq.
            pkt = make_packet("DATA", seq, data)
            send_packet_simulated(sock, pkt, receiver_addr)
            # Wait for ACK.
            try:
                resp, _ = sock.recvfrom(BUFFER_SIZE)
                p_type, p_seq, _, is_valid = parse_packet(resp)

                # If ACK is valid and matches seq, set acked = True.
                if is_valid and p_type == "ACK" and p_seq == seq:
                    acked = True
            except (socket.timeout, ConnectionResetError):
                # If timeout occurs, retransmit this same packet.
                pass
        seq = 1 - seq
# Send FIN until a valid FINACK is received.
fin_acked = False
while not fin_acked:
    fin_pkt = make_packet("FIN", seq)
    send_packet_simulated(sock, fin_pkt, receiver_addr)

    try: 
        resp, _ = sock.recvfrom(BUFFER_SIZE)
        p_type, p_seq, _, is_valid = parse_packet(resp)
        if is_valid and p_type == "FINACK" and p_seq == seq:
            fin_acked = True
    except (socket.timeout, ConnectionResetError):
        pass

sock.close()
print("Transfer complete.")
