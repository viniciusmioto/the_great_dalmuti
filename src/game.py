from machines import get_machine_config
import communication as net

machine_number = int(input("Machine Number: "))
machine_info = get_machine_config(machine_number)
received = False
if(machine_number == 1):
    while(1):
        # Marcador de inicio / origem / jogada / confirmação de recebimento / marcador de fim
        message = input("Message: ")
        net.send_message(message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"])
        net.receive_message(machine_info["RECV_PORT"])
else:
    while(1):
        net.receive_message(machine_info["RECV_PORT"])
        # Marcador de inicio / origem / jogada / confirmação de recebimento / marcador de fim
        message = input("Message: ")
        net.send_message(message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"])
        
