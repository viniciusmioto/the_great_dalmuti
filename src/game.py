import machines as config
from game_rules import get_cards
import communication as net

machine_number = int(input("Machine Number: "))
machine_info = config.get_machine_config(machine_number)
players_qt = config.get_players_amout()
player_deck = []
deck = get_cards()
card_per_player = 80//players_qt
if(machine_number == 1):
    # faz o carteado
    for player in range(players_qt-1):
        player_info = config.get_machine_config(player+2) # player + 1 para skipar o primeiro player
        player_deck = []
        for card in range(card_per_player):
            player_deck.append(deck.pop())
        print(f'enviou as cartas para o jogador {player+2}')
        message = {"init_marker": "01110", "origin": machine_info["ADDRESS"], "destiny": player_info["ADDRESS"], "move_info": {"info": "deck", "deck": player_deck}, "receive_confirm": 0, "end_marker": "10001"}
        net.send_message(message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]) # manda a carta para o jogador da vez
        recv_message = net.receive_message(machine_info["RECV_PORT"])
        if(recv_message["origin"] == machine_info["ADDRESS"]): # espera chegar em todo mundo antes de enviar a proxima mensagem
            continue
    # faz a primeira jogada
    jogada = input("Jogada: ")
    move = {"info": "move", "machine_number": machine_number, "move": jogada}
    message = {"init_marker": "01110", "origin": machine_info["ADDRESS"], "destiny": machine_info["SEND_ADDRESS"], "move_info": move, "receive_confirm": 0, "end_marker": "10001"} # Marcador de inicio / origem / jogada / confirmação de recebimento / marcador de fim / destino
    net.send_message(message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]) # faz a primeira jogada
    
while(1):
    recv_message = net.receive_message(machine_info["RECV_PORT"])
    recv_message["receive_confirm"] = 1

    if(recv_message["origin"] != machine_info["ADDRESS"] and recv_message["move_info"] != "bastao"): #se a mensagem nao for da propria maquina ou for diferente do bastao, passa pra frente
        if(recv_message["destiny"] == machine_info["ADDRESS"] and recv_message["move_info"]["info"] == "deck"):
            player_deck = recv_message["move_info"]["deck"]
            print(f'O Deck do jogador {machine_number} é {player_deck}')
        elif (recv_message["move_info"]["info"] == "move"):
            print(f'O jogador {recv_message["move_info"]["machine_number"]} jogou a carta {recv_message["move_info"]["move"]}\n')
        net.send_message(recv_message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"])
    
    elif(recv_message["origin"] == machine_info["ADDRESS"]): #se recebeu a mensagem que enviou, então passa o bastao
        print(f'O jogador {machine_number} finalizou a jogada...\n')
        message = {"init_marker": "01110", "origin": machine_info["ADDRESS"], "move_info": "bastao", "receive_confirm": 1, "end_marker": "10001"}
        net.send_message(message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]) # passou o bastao

    else: # esta com o bastao e deve fazer a jogada
        jogada = input("Jogada: ")
        move = {"info": "move", "machine_number": machine_number, "move": jogada}
        message = {"init_marker": "01110", "origin": machine_info["ADDRESS"], "destiny": machine_info["SEND_ADDRESS"], "move_info": move, "receive_confirm": 0, "end_marker": "10001"}
        net.send_message(message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"])
        
