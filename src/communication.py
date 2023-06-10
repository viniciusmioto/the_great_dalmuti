import socket

def send_message(message, address, port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the message
        sock.sendto(message.encode(), (address, port))
        print("Message sent successfully!")
    except socket.error as e:
        print("Error while sending message:", e)
    finally:
        # Close the socket
        sock.close()

def receive_message(port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Bind the socket to the specified port
        sock.bind(('', port))
        print("Listening for incoming messages...")

        # Receive messages continuously
        while True:
            data, addr = sock.recvfrom(1024)  # Adjust buffer size as needed
            message = data.decode()
            print(f"Received message from {addr}: {message}")
            break
    
    except socket.error as e:
        print("Error while receiving message:", e)
    finally:
        # Close the socket
        sock.close()
