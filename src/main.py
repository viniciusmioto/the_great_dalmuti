import machines as machine
import gameplay as game
import communication as net
import interface as ui

import sys

def main():
    # Check if the correct number of arguments is provided
    if len(sys.argv) > 2:
        return

    # If an argument is provided, use it as the parameter, otherwise default to 0
    if len(sys.argv) == 2:
        ui.set_theme(sys.argv[1])
        

    machine_number = int(input("Número da Máquina:  "))
    machine_info = machine.get_machine_info(machine_number)
    players_qtd = machine.get_players_amout()
    player_deck = []
    table_hand = {}
    deck = game.get_cards()
    leaderboard = []

    # se for a primeira maquina, faz o carteado (dealer)
    if machine_info["NUMBER"] == 1:
        # faz o carteado
        player_deck = game.deal_cards(players_qtd, deck, machine_info)

        # faz a primeira jogada
        player_move = game.make_move(machine_info, player_deck)

        net.send_player_move(machine_info, player_move)
        # table_hand = game.get_move_info(machine_info["NUMBER"], player_move)


    while len(leaderboard) < players_qtd:
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

                ui.show_deck(machine_info, player_deck, "hand")

            # jogada: verifica a jogada e mostra na tela
            elif recv_message["move_info"]["info"] in ["move", "opponent_finished"]:
                opponent_info = machine.get_machine_info(recv_message["number_from"])

                if (
                    recv_message["move_info"]["info"] == "opponent_finished"
                    and opponent_info["NUMBER"] not in leaderboard
                ):
                    leaderboard.append(opponent_info["NUMBER"])

                # verifica se o jogador anterior realizou uma jogada
                if recv_message["move_info"]["player_move"]:
                    ui.show_deck(
                        opponent_info, recv_message["move_info"]["player_move"], "opponent"
                    )
                    table_hand = game.get_move_info(
                        opponent_info["NUMBER"], recv_message["move_info"]["player_move"]
                    )
                else:  # jogada vazia, passou a vez
                    print(
                        f"O jogador {opponent_info['NUMBER']} ({opponent_info['CLASS']}) passou a vez.\n"
                    )

            net.send_message(
                recv_message, machine_info["SEND_ADDRESS"], machine_info["SEND_PORT"]
            )

        # se recebeu a mensagem que enviou, então passa o token
        elif recv_message["origin"] == machine_info["ADDRESS"]:
            print("Jogada finalizada, aguardando os outros...")
            net.send_token(machine_info)

        # esta com o token e deve fazer a jogada
        else:
            player_move = game.verify_round(
                machine_info, player_deck, table_hand, leaderboard
            )

            if len(leaderboard) == players_qtd - 1 and machine_info["NUMBER"] not in leaderboard:
                player_deck = []
                leaderboard.append(machine_info["NUMBER"])

            if player_deck == []:
                net.send_player_move(machine_info, player_move, "opponent_finished")
            else:
                net.send_player_move(machine_info, player_move)

            table_hand = game.get_move_info(machine_info["NUMBER"], player_move)




    ui.clear_screen()
    # quando todos os jogadores tiverem finalizado, mostra colocação
    for i in range(len(leaderboard)):
        ui.print_success(
            f"O jogador ({leaderboard[i]}) ficou em {i+1}º lugar."
        )

if __name__ == "__main__":
    main()