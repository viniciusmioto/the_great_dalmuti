import network as net

def main():
    machine_configs = net.read_machine_configurations('config.txt')
    machine1_ip, machine1_port = machine_configs['Machine 1']
    machine2_ip, machine2_port = machine_configs['Machine 2']
    message = "Hello, receiver!"
    net.send_message(machine1_ip, machine1_port, machine2_ip, machine2_port, message)
    response = net.receive_message(machine2_ip, machine2_port)
    print("Received:", response)


if __name__ == '__main__':
    main()
