import socket
import json

HOST = "localhost"  # The server's hostname or IP address
PORT = 5000  # The server's port number

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
server.bind((HOST, PORT))  # Bind the socket to the host and port

while True:
    # Receive data from the client
    data, addr = server.recvfrom(1024)
    print(f"Received data from {addr}")

    # Decode the JSON data
    data = json.loads(data.decode("utf-8"))

    # Process the data
    if data["type"] == "message":
        message = data["message"]
        print(f"Client says: {message}")

        # Send a response to the client
        response = {"message": f"Server received: {message}"}
        response_data = json.dumps(response).encode("utf-8")
        server.sendto(response_data, addr)
