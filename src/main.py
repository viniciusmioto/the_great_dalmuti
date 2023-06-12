import machines as config
import gameplay as game
import communication as net
import interface as ui
from message import Message


machine_number = int(input("Número da Máquina: \n"))
machine_info = config.get_machine_config(machine_number)
players_qtd = config.get_players_amout()
player_deck = []
deck = game.get_cards()
card_per_player = 80 // players_qtd  # sempre vai ser 80 cartas pq ta na regra

if machine_number == 1:
    # faz o carteado
    for player in range(players_qtd - 1):
        player_info = config.get_machine_config(
            player + 2
        )  # player + 1 para skipar o primeiro player

        player_deck = []
        for card in range(card_per_player):
            player_deck.append(deck.pop())
        player_deck.sort(reverse=True)

        message = Message(
            origin=machine_info["ADDRESS"],
            destiny=player_info["ADDRESS"],
            move_info={"info": "deck", "deck": player_deck},
        )

        net.send_message(
            message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
        )  # manda a carta para o jogador da vez

        print(f"Deu as cartas para o jogador {player+2}\n")

        recv_message = net.receive_message(machine_info["RECV_PORT"])
        if (
            recv_message["origin"] == machine_info["ADDRESS"]
        ):  # espera chegar em todo mundo antes de enviar a proxima mensagem
            continue

    player_deck = []

    # pega o resto das cartas
    for card in range(len(deck)):
        player_deck.append(deck.pop())
    player_deck.sort(reverse=True)

    print(f"O Deck do jogador {machine_number} é\n")
    for c in player_deck:
        ui.print_deck(c)

    # faz a primeira jogada
    player_move = game.make_move(player_deck)

    move = {"info": "move", "machine_number": machine_number, "move": player_move}

    message = Message(
        origin=machine_info["ADDRESS"], destiny=machine_info["ADDRESS"], move_info=move
    )

    net.send_message(
        message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
    )  # faz a primeira jogada

while 1:
    recv_message = net.receive_message(machine_info["RECV_PORT"])
    recv_message["receive_confirm"] = 1

    if (
        recv_message["origin"] != machine_info["ADDRESS"]
        and recv_message["move_info"] != "bastao"
    ):  # se a mensagem nao for da propria maquina ou for diferente do bastao, passa pra frente
        if (
            recv_message["destiny"] == machine_info["ADDRESS"]
            and recv_message["move_info"]["info"] == "deck"
        ):
            player_deck = recv_message["move_info"]["deck"]

            print(f"O Deck do jogador {machine_number} é\n")
            for c in player_deck:
                ui.print_deck(c)

        elif recv_message["move_info"]["info"] == "move":
            # verificar a jogada e atualizar
            print(f'\nO jogador {recv_message["move_info"]["machine_number"]} jogou\n')

            for c in recv_message["move_info"]["move"]:
                ui.print_deck(c)

        net.send_message(
            recv_message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
        )

    elif (
        recv_message["origin"] == machine_info["ADDRESS"]
    ):  # se recebeu a mensagem que enviou, então passa o bastao
        print(f"O jogador {machine_number} finalizou a jogada...\n")

        message = Message(origin=machine_info["ADDRESS"], move_info="bastao", receive_confirm=1)

        net.send_message(
            message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
        )  # passou o bastao

    else:  # esta com o bastao e deve fazer a jogada
        player_move = game.make_move(player_deck)

        move = {"info": "move", "machine_number": machine_number, "move": player_move}

        message = Message(origin=machine_info["ADDRESS"], move_info=move)

        net.send_message(
            message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
        )
