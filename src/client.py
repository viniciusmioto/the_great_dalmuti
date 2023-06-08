import socket

sender_ip = '10.254.223.29'
sender_port = 5501

receiver_ip = '10.254.223.30'
receiver_port = 5501

message = 'Hello, Machine 2!'

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the sender's IP and port
sock.bind((sender_ip, sender_port))

# Send the message to the receiver
sock.sendto(message.encode(), (receiver_ip, receiver_port))

# Close the socket
sock.close()
