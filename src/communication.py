import socket
import ast

class Message:
    def __init__(self, origin, number_from, destiny=None, move_info=None, receive_confirm=0):
        self.init_marker = "01110"
        self.origin = origin
        self.number_from = number_from
        self.destiny = destiny
        self.move_info = move_info
        self.receive_confirm = receive_confirm
        self.end_marker = "10001"

    def __str__(self):
        return str(self.__dict__)


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
        sock.bind(("", port))
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


def send_token(machine_info):
    message = Message(
        origin=machine_info["ADDRESS"],
        number_from=machine_info['NUMBER'],
        move_info="token",
        receive_confirm=1,
    )

    send_message(
        message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
    )  # passou o token


def send_player_move(machine_info, player_move, move_info="move"):
    move = {
        "info": move_info,
        "player_move": player_move,
    }

    message = Message(
        origin=machine_info["ADDRESS"],
        number_from=machine_info['NUMBER'],
        move_info=move,
    )

    send_message(message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"])
