# udp_server.py
import json
import socket

from decodage import checksum_decode

# Define server IP address and port
SERVER_IP = "127.0.0.1"  # localhost
SERVER_PORT = 5005       # Non-privileged port nombre arbitraire

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket.AF_INET: IPv4
#socket.SOCK_DGRAM: UDP

# Bind the socket to the address
server_socket.bind((SERVER_IP, SERVER_PORT))
#socket.bind: Bind the socket to an address
print(f"[+] UDP server listening on {SERVER_IP}:{SERVER_PORT}")
#socket.listen: Listen for incoming connections

try:
    while True:
        # Receive data from client (max 1024 bytes)
        data, client_address = server_socket.recvfrom(1024)
        #socket.recvfrom: Receive data from the socket as a tuple (data, address)

        print(f"[>] Received from {client_address}: {data.decode()}")
        #socket.decode: Decode the bytes to string because data is in bytes not string

        # Decode the JSON message
        message = json.loads(data.decode())
        x=checksum_decode(message[0])
        y=checksum_decode(message[1])
        operator=message[2]
        print(f"[>] Decoded message: {x}, {y}, {operator}")
        reply_message = "Message received loud and clear!"
        server_socket.sendto(reply_message.encode(), client_address)
        print(f"[<] Sent response to {client_address}")

except KeyboardInterrupt:
    print("\n[!] Server shutting down.")

finally:
    server_socket.close()
