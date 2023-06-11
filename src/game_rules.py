import random

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
