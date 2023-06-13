import random
import interface as ui
import communication as net
import machines as machine
from communication import Message

cards = [
    (13, "Jester 🃏"),
    (12, "Peasant 🌾"),
    (11, "Stonecutter 🪨"),
    (10, "Shepherdess 🐑"),
    (9, "Cook 🍴"),
    (8, "Mason 🛠️"),
    (7, "Seamstress 🧵"),
    (6, "Knight 🗡️"),
    (5, "Abbess 📿"),
    (4, "Baroness 🪙"),
    (3, "Earl Marshal 🛡️"),
    (2, "Archbishop ⛪"),
    (1, "The Great Dalmuti 👑"),
]


def get_cards():
    # define as cartas do deck
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
    """
    -> Verifica as cartas adicionadas a seleção para descarte
    Leva em consideração apenas a seleção, não a mesa
    :param selected_cards: cartas selecionadas
    :return: True se a seleção for válida, False se não for
    """

    # lista menor que 2 não precisa de verificação
    if len(selected_cards) < 2:
        return True

    # Obtem o número de referência para comparação

    # se o primeiro não for um Jester, ele é o número de referência
    if selected_cards[0][0] != 13:
        reference_number = selected_cards[0][0]
    # se o primeiro for um Jester, mas a lista tem tamanho 2
    elif len(selected_cards) == 2:
        return True
    # se o segundo não for um Jester, ele é o número de referência
    elif selected_cards[1][0] != 13:
        reference_number = selected_cards[1][0]

    # verifica se o número de referência é igual ao número das outras cartas
    for card in selected_cards[1:]:
        if card[0] != reference_number and card[0] != 13:
            return False

    return True


def verify_move(player_move, table_hand):
    """
    -> Verifica a jogada em relação a mesa
    :param selected_cards: cartas selecionadas
    :return: True se a jogada for válida, False se não for
    """

    if player_move["amount"] != table_hand["amount"] and table_hand["amount"] != 0:
        return False

    if player_move["rank"] >= table_hand["rank"]:
        return False

    return True


def undo_move(player_deck, selected_cards):
    """
    -> Desfaz a jogada do jogador
    :param player_deck: cartas do jogador
    :param selected_cards: cartas selecionadas
    :return: cartas do jogador e da mesa
    """

    for card in selected_cards:
        player_deck.append(card)
    player_deck.sort(reverse=True)

    selected_cards.clear()


def make_move(machine_number, player_deck, table_hand=None):
    """
    -> Realiza a jogada do jogador da vez
    :param player_deck: cartas do jogador
    :return: cartas selecionadas
    """

    selected_cards = []

    while True:
        ui.show_deck(machine_number, player_deck, "hand")

        player_move = input(
            "Escolha a carta ('0' - conclui seleção; 'p' - passa a vez):  "
        )

        if player_move.lower() == "0":
            if table_hand:
                if verify_move(get_move_info(selected_cards), table_hand):
                    break
                else:
                    undo_move(player_deck, selected_cards)
            else:
                break
        elif player_move.lower() == "p":
            undo_move(player_deck, selected_cards)
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
                        ui.print_warning(
                            "Cartas não possuem o mesmo número ou não são Jesters."
                        )
                else:
                    ui.print_warning("Carta não pertence ao seu deck.")
            else:
                ui.print_warning("Número de carta inválido.")
        except ValueError:
            ui.print_warning("Entrada inválida. Tente novamente.")

        ui.show_deck(machine_number, selected_cards, "selection")

    ui.clear_screen()

    if len(selected_cards) == 0:
        print(f"Jogador {machine_number} passou a vez.\n")
    else:
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
        player_info = machine.get_machine_info(
            player + 2
        )  # player + 1 para skipar o primeiro player

        opponent_deck = []
        for card in range(card_per_player):
            opponent_deck.append(deck.pop())
        opponent_deck.sort(reverse=True)

        message = Message(
            origin=machine_info["ADDRESS"],
            destiny=player_info["ADDRESS"],
            number_from=machine_info["number"],
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


def get_move_info(deck):
    # obtém o tamanho do descarte
    deck_size = len(deck)

    if deck_size == 0:
        return {"amount": 0, "rank": 0}

    # descobre o rank do oponente
    # descartou apenas uma carta ou não é um Jester
    if deck_size == 1 or deck[0][0] != 13:
        reference_number = deck[0][0]
    # Se o primeiro for um Jester, mas a lista tem tamanho 2
    elif deck_size == 2 or deck[1][0] != 13:
        reference_number = deck[1][0]

    return {"amount": deck_size, "rank": reference_number}
