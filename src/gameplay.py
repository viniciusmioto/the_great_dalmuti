import random
import interface as ui

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


def make_move(player_deck):
    selected_cards = []
    while True:
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
                    player_deck.remove(card)
                else:
                    ui.print_warning("Carta não pertence ao seu deck.")
            else:
                ui.print_warning("Número de carta inválido.")
        except ValueError:
            ui.print_warning("Entrada inválida.")

    print("Cartas Restantes: \n")
    for c in player_deck:
        ui.print_deck(c)

    return selected_cards