import random

cards = {
    13: "Jester 🃏",
    12: "Peasant 🌾",
    11: "Stonecutter 🪨",
    10: "Shepherdess 🐑",
    9: "Cook 🍴",
    8: "Mason 🛠️",
    7: "Seamstress 🧵",
    6: "Knight 🗡️",
    5: "Abbess 📿",
    4: "Baroness 🪙",
    3: "Earl Marshal 🛡️",
    2: "Archbishop ⛪",
    1: "The Great Dalmuti 👑",
}

deck = []
for rank in cards:
    if rank == 13:  # existem apenas dois jesters
        deck.extend([13, 13])
    else:
        deck.extend([rank] * rank)

# mostra a quantidade de cada carta
for card in cards:
    print(f"{cards[card]}: {deck.count(card)}")

# embaralha o deck
random.shuffle(deck)

my_deck = deck[:10]

# mostra o deck (rank, description)
for card in my_deck:
    print(f"[({card}) {cards[card]}]")