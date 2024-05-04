import socket
import json

HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The server's port number

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket

# Send a message to the server
message = {"type": "message", "message": "Hello from the client!"}
message_data = json.dumps(message).encode("utf-8")
client.sendto(message_data, (HOST, PORT))

# Receive a response from the server
data, addr = client.recvfrom(1024)
print(f"Received data from {addr}")

# Decode the JSON data
data = json.loads(data.decode("utf-8"))
print(f"Server says: {data['message']}")