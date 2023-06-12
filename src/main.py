import machines as machine
import gameplay as game
import communication as net
import interface as ui
from message import Message


machine_number = int(input("Número da Máquina: \n"))
machine_info = machine.get_machine_config(machine_number)
players_qtd = machine.get_players_amout()
player_deck = []
deck = game.get_cards()

# se for a primeira maquina, faz o carteado (dealer)
if machine_number == 1:
    # faz o carteado
    player_deck = game.deal_cards(players_qtd, deck, machine_info)

    print(f"O Deck do jogador {machine_number} é\n")
    for c in player_deck:
        ui.print_deck(c)

    # faz a primeira jogada
    player_move = game.make_move(player_deck)

    net.send_player_move(machine_info, machine_number, player_move)


while True:
    recv_message = net.receive_message(machine_info["RECV_PORT"])
    recv_message["receive_confirm"] = 1

    # se a mensagem nao for da propria maquina ou for diferente do bastao, passa pra frente
    if (
        recv_message["origin"] != machine_info["ADDRESS"]
        and recv_message["move_info"] != "bastao"
    ):
        # carteado: verifica se o destino está correto e se contem o deck
        if (
            recv_message["destiny"] == machine_info["ADDRESS"]
            and recv_message["move_info"]["info"] == "deck"
        ):
            # recebe o deck e mostra na tela
            player_deck = recv_message["move_info"]["deck"]

            print(f"O Deck do jogador {machine_number} é\n")
            for c in player_deck:
                ui.print_deck(c)

        # jogada: verifica a jogada e mostra na tela
        elif recv_message["move_info"]["info"] == "move":
            print(f'\nO jogador {recv_message["move_info"]["machine_number"]} jogou\n')

            for c in recv_message["move_info"]["player_move"]:
                ui.print_move(c)

        net.send_message(
            recv_message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
        )

    # se recebeu a mensagem que enviou, então passa o bastao
    elif recv_message["origin"] == machine_info["ADDRESS"]:
        print(f"O jogador {machine_number} finalizou a jogada...\n")

        net.send_token(machine_info)

    # esta com o bastao e deve fazer a jogada
    else:
        player_move = game.make_move(player_deck)

        net.send_player_move(machine_info, machine_number, player_move)
