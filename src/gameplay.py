import random
import interface as ui
import communication as net
import machines as machine
from message import Message


def get_cards():
    # define as cartas do deck
    cards = [
        (13, "Jester"),
        (12, "Peasant"),
        (11, "Stonecutter"),
        (10, "Shepherdess"),
        (9, "Cook"),
        (8, "Mason"),
        (7, "Seamstress"),
        (6, "Knight"),
        (5, "Abbess"),
        (4, "Baroness"),
        (3, "Earl Marshal"),
        (2, "Archbishop"),
        (1, "The Great Dalmuti")
    ]
    deck = []
    # adiciona as cartas no deck
    for rank, name in cards:
        if rank == 13:  # existem apenas dois jesters
            deck.append((rank, name))
            deck.append((rank, name))
        else:
            for _ in range(rank):
                deck.append((rank, name))
    # embaralha o deck
    random.shuffle(deck)
    return deck


def verify_cards(selected_cards):
    # Lista menor que 2 não precisa de verificação
    if len(selected_cards) < 2:
        return True

    # Obtem o número de referência para comparação
    
    # Se o primeiro não for um Jester, ele é o número de referência
    if selected_cards[0][0] != 13:
        reference_number = selected_cards[0][0]
    # Se o primeiro for um Jester, mas a lista tem tamanho 2
    elif len(selected_cards) == 2:
        return True
    # Se o segundo não for um Jester, ele é o número de referência
    elif selected_cards[1][0] != 13:
        reference_number = selected_cards[1][0]

    # Check if all tuples in the list have the same number as the reference number
    for card in selected_cards[1:]:
        if card[0] != reference_number and card[0] != 13:
            return False

    return True


def make_move(machine_number, player_deck):
    """
    -> Realiza a jogada do jogador da vez
    :param player_deck: cartas do jogador
    :return: cartas selecionadas
    """

    selected_cards = []

    while True:
        ui.show_deck(machine_number, player_deck, "hand")

        player_move = input(
            "\nEscolha suas cartas para jogar (ou digite 'fim' para encerrar): \n"
        )

        if player_move.lower() == "fim":
            break

        # valida a jogada
        try:
            card_number = int(player_move)
            if 1 <= card_number <= 13:
                card = next(
                    (card for card in player_deck if card[0] == card_number), None
                )
                if card:
                    selected_cards.append(card)

                    if verify_cards(selected_cards):
                        player_deck.remove(card)
                    else:
                        selected_cards.remove(card)
                        ui.print_warning("Cartas não possuem o mesmo número ou não são Jesters.")
                else:
                    ui.print_warning("Carta não pertence ao seu deck.")
            else:
                ui.print_warning("Número de carta inválido.")
        except ValueError:
            ui.print_warning("Entrada inválida.")

        ui.show_deck(machine_number, selected_cards, "selection")

    ui.clear_screen()

    ui.show_deck(machine_number, selected_cards, "discard")

    ui.show_deck(machine_number, player_deck, "hand")

    return selected_cards


def deal_cards(players_qtd, deck, machine_info):
    """
    -> Distribui as cartas para todos os jogadores
    :param players_qtd: quantidade de jogadores
    :param deck: cartas
    :param machine_info: informações da máquina
    :return: cartas do dealer
    """

    card_per_player = 80 // players_qtd 

    for player in range(players_qtd - 1):
        player_info = machine.get_machine_config(
            player + 2
        )  # player + 1 para skipar o primeiro player

        opponent_deck = []
        for card in range(card_per_player):
            opponent_deck.append(deck.pop())
        opponent_deck.sort(reverse=True)

        message = Message(
            origin=machine_info["ADDRESS"],
            destiny=player_info["ADDRESS"],
            move_info={"info": "deck", "deck": opponent_deck},
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

    # pega o resto das cartas
    dealer_deck = []
    dealer_deck = sorted(deck, reverse=True)
    deck.clear()

    return dealer_deck