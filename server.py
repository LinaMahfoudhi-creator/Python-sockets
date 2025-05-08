# udp_server.py
import json
import socket

from decodage import checksum_decode
from erreur import flip_random_bit_with_error
from operation import binary_operation

SERVER_IP = "127.0.0.1"  # localhost
SERVER_PORT = 5005       # port nombre arbitraire

# UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket.AF_INET: IPv4
#socket.SOCK_DGRAM: UDP

# Bind the socket to the address
server_socket.bind((SERVER_IP, SERVER_PORT))
#socket.bind: Bind the socket to an address
print(f"[+] UDP server listening on {SERVER_IP}:{SERVER_PORT}")

try:
    while True:
        # Receive data from client (max 1024 bytes)
        data, client_address = server_socket.recvfrom(1024)

        #socket.recvfrom: Receive data from the socket as a tuple (data, address)
        data = data.decode()
        message = json.loads(data)

        #simuler une erreur de transmission

        x = flip_random_bit_with_error(message[0])
        y = flip_random_bit_with_error(message[1])
        operator = message[2]

        print(f"[>] opération reçue {client_address}: [{x},{y},{operator}]")

        if checksum_decode(x)[1]=="error" or checksum_decode(y)[1]== "error":
            reply_message = checksum_decode(x)[0]+" "+operator+" "+checksum_decode(y)[0]+" = "+"error"
        else:
            reply_message = (checksum_decode(x)[0]+" "+operator+" "+checksum_decode(y)[0]+" = "
                             +binary_operation(checksum_decode(x)[0], checksum_decode(y)[0], operator))

        server_socket.sendto(reply_message.encode(), client_address)
        print(f"[<] Sent response to {client_address}")

except KeyboardInterrupt:
    print("\n[!] Server shutting down.")

finally:
    server_socket.close() # udp_client.py