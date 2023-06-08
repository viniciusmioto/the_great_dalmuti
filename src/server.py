import socket

receiver_ip = '10.254.223.30'
receiver_port = 5501

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the receiver's IP and port
sock.bind((receiver_ip, receiver_port))

# Receive the message
data, addr = sock.recvfrom(1024)
message = data.decode()

print('Received message:', message)

# Close the socket
sock.close()
