import socket

listen_host = "127.0.0.1"
listen_port = 12345

# Create a listening socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((listen_host, listen_port))
server_socket.listen(1)

print(f"Listening on {listen_host}:{listen_port}...")

conn, addr = server_socket.accept()
print("Connection received!")

data = conn.recv(4096)
print("Received message:")
print(data.decode())

conn.close()
server_socket.close()
