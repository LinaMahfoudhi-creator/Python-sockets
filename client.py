# udp_client.py
import json
import socket

from codage import checksum_encode

# Define server IP and port (same as server)
SERVER_IP = "127.0.0.1"
# localhost
SERVER_PORT = 5005
# Non-privileged port nombre arbitraire

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket.AF_INET: IPv4
#socket.SOCK_DGRAM: UDP

# Set timeout in case server does not respond
client_socket.settimeout(5)

# Message to send
equation = [checksum_encode("10010011101011101"), checksum_encode("10101010101010101"),"+"]
message=json.dumps(equation)
try:
    # Send message to server
    print(f"[>] Sending to {SERVER_IP}:{SERVER_PORT}: {message}")
    client_socket.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
    #encode the string to bytes because data is in bytes not string

    # Wait for a response
    response, server_address = client_socket.recvfrom(1024)
    #socket.recvfrom: Receive data from the socket as a tuple (data, address)
    print(f"[<] Received from server: {response.decode()}")

except socket.timeout:
    print("[!] No response from server, request timed out.")

finally:
    client_socket.close()
