import socket
import ast

def send_message(message, address, port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the message
        str_message = str(message)
        sock.sendto(str_message.encode(), (address, port))
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
        # Receive messages continuously
        while True:
            data, addr = sock.recvfrom(2048)  # Adjust buffer size as needed
            res = ast.literal_eval(data.decode())
            return res
            break
    
    except socket.error as e:
        print("Error while receiving message:", e)
    finally:
        # Close the socket
        sock.close()
