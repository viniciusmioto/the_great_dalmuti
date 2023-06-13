import machines as machine
import gameplay as game
import communication as net
import interface as ui


machine_number = int(input("Número da Máquina:  "))
machine_info = machine.get_machine_config(machine_number)
players_qtd = machine.get_players_amout()
player_deck = []
table_hand = {}
deck = game.get_cards()

# se for a primeira maquina, faz o carteado (dealer)
if machine_info["number"] == 1:
    print(machine_info)
    # faz o carteado
    player_deck = game.deal_cards(players_qtd, deck, machine_info)

    # faz a primeira jogada
    player_move = game.make_move(machine_info["number"], player_deck)

    net.send_player_move(machine_info, machine_info["number"], player_move)


while True:
    recv_message = net.receive_message(machine_info["RECV_PORT"])
    recv_message["receive_confirm"] = 1

    # se a mensagem nao for da propria maquina ou for diferente do token, passa pra frente
    if (
        recv_message["origin"] != machine_info["ADDRESS"]
        and recv_message["move_info"] != "token"
    ):
        # carteado: verifica se o destino está correto e se contem o deck
        if (
            recv_message["destiny"] == machine_info["ADDRESS"]
            and recv_message["move_info"]["info"] == "deck"
        ):
            # recebe o deck e mostra na tela
            player_deck = recv_message["move_info"]["deck"]

            ui.show_deck(machine_info["number"], player_deck, "hand")

        # jogada: verifica a jogada e mostra na tela
        elif recv_message["move_info"]["info"] == "move":
            ui.show_deck(recv_message["move_info"]["machine_number"], recv_message["move_info"]["player_move"], "opponent")

            if recv_message["move_info"]["player_move"]:
                table_hand = game.get_move_info(recv_message["move_info"]["player_move"])

        net.send_message(
            recv_message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
        )

    # se recebeu a mensagem que enviou, então passa o token
    elif recv_message["origin"] == machine_info["ADDRESS"]:
        print(f"O jogador {machine_info['number']} ({machine_info['CLASS']}) finalizou a jogada...\n")

        net.send_token(machine_info)

    # esta com o token e deve fazer a jogada
    else:
        player_move = game.make_move(machine_info["number"], player_deck, table_hand)

        net.send_player_move(machine_info, machine_info["number"], player_move)
