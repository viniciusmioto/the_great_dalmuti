import socket


def read_machine_configurations(file_path):
    machine_configs = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):
            machine_name = lines[i].strip()
            machine_ip = lines[i + 1].split(': ')[1].strip()
            machine_port = int(lines[i + 2].split(': ')[1].strip())
            machine_configs[machine_name] = (machine_ip, machine_port)
    return machine_configs


def send_message(sender_ip, sender_port, receiver_ip, receiver_port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender_address = (sender_ip, sender_port)
    receiver_address = (receiver_ip, receiver_port)
    sock.bind(sender_address)
    sock.sendto(message.encode(), receiver_address)
    sock.close()


def receive_message(receiver_ip, receiver_port, buffer_size=1024):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_address = (receiver_ip, receiver_port)
    sock.bind(receiver_address)
    data, address = sock.recvfrom(buffer_size)
    sock.close()
    return data.decode()


def main():
    machine_configs = read_machine_configurations('config.txt')
    machine1_ip, machine1_port = machine_configs['Machine 1']
    machine2_ip, machine2_port = machine_configs['Machine 2']
    message = "Hello, receiver!"
    send_message(machine1_ip, machine1_port, machine2_ip, machine2_port, message)
    response = receive_message(machine2_ip, machine2_port)
    print("Received:", response)


if __name__ == '__main__':
    main()
