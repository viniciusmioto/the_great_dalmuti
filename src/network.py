import socket


def get_next_machine(config_file, current_machine):
    machines = {}

    with open(config_file, "r") as file:
        lines = file.readlines()
        num_machines = int(lines[0].split()[1])

        for i in range(1, len(lines)):
            line = lines[i].strip()

            if line.startswith("MACHINE"):
                machine_number = int(line.split()[1])
                machine_info = {"number": machine_number}
            elif line.startswith(("ADDRESS", "SEND_ADDRESS", "SEND_PORT", "RECV_PORT")):
                key, value = line.split()
                machine_info[key.split("_")[0].lower()] = value

                if line.startswith("RECV_PORT"):
                    machines[machine_number] = machine_info

    if current_machine in machines:
        current_machine_info = machines[current_machine]
        next_machine_number = (current_machine % num_machines) + 1
        next_machine_info = machines[next_machine_number]

        next_machine_info["number"] = next_machine_number
        return next_machine_info

    return None


def get_current_machine(config_file, current_machine):
    machines = {}

    with open(config_file, "r") as file:
        lines = file.readlines()
        num_machines = int(lines[0].split()[1])

        for i in range(1, len(lines)):
            line = lines[i].strip()

            if line.startswith("MACHINE"):
                machine_number = int(line.split()[1])
                machine_info = {"number": machine_number}
            elif line.startswith(("ADDRESS", "SEND_ADDRESS", "SEND_PORT", "RECV_PORT")):
                key, value = line.split()
                machine_info[key.split("_")[0].lower()] = value

                if line.startswith("RECV_PORT"):
                    machines[machine_number] = machine_info

    if current_machine in machines:
        return machines[current_machine]

    return None




def receive_message(receiver_ip, receiver_port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the receiver's IP and port
    sock.bind((receiver_ip, receiver_port))

    # Receive the message
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    # Close the socket
    sock.close()

    return message


def send_message(sender_ip, sender_port, receiver_ip, receiver_port, message):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the sender's IP and port
    sock.bind((sender_ip, sender_port))

    # Send the message to the receiver
    sock.sendto(message.encode(), (receiver_ip, receiver_port))

    # Close the socket
    sock.close()
