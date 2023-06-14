import os
import gameplay as game


def set_theme(theme):
    if theme == 1:
        global font_colour

        font_colour = {
            "black": "\033[1;30m",
            "purple": "\033[1;31m",
            "purple_b": "\033[7;31m",
            "green": "\033[1;32m",
            "yellow": "\033[1;33m",
            "blue": "\033[1;34m",
            "red": "\033[1;35m",
            "cyan": "\033[1;36m",
            "grey": "\033[1;37m",
            "bold": "\033[;1m",
            "clear": "\033[m",
        }
    else:
        font_colour = {
            "black": "\033[1;30m",
            "purple": "\033[1;35m",
            "purple_b": "\033[7;35m",
            "green": "\033[1;32m",
            "yellow": "\033[1;33m",
            "blue": "\033[1;34m",
            "red": "\033[1;31m",
            "cyan": "\033[1;36m",
            "grey": "\033[1;37m",
            "bold": "\033[;1m",
            "clear": "\033[m",
        }


def font(c):
    return font_colour[c]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_warning(msg):
    print(f'{font("yellow")}WARNING: {msg}{font("clear")}')


def print_error(msg):
    print(f'{font("red")}ERROR: {msg}{font("clear")}')


def print_success(msg):
    print(f'{font("green")}{msg}{font("clear")}')


def print_info(msg):
    print(f'{font("cyan")}INFO: {msg}{font("clear")}')


def print_table(msg):
    print(f'{font("purple_b")} MESA|| {msg} {font("clear")}')


def print_deck(deck, font_color, new_line=True):
    """
    -> This function print the deck
    :param deck: list of cards
    :return: print the deck
    """

    if new_line:
        print(f'{font(font_color)}{deck}{font("clear")}')
    else:
        print(f'{font(font_color)}{deck}{font("clear")}', end=" ")


def show_deck(machine_info, player_deck, deck_type):
    if deck_type == "hand":
        color = "purple"
        print(f"Seu deck ({machine_info['NUMBER']}| {machine_info['CLASS']}):")
    elif deck_type == "opponent":
        print(f"O jogador {machine_info['NUMBER']}| {machine_info['CLASS']} descartou:")
        color = "cyan"
    elif deck_type == "selection":
        print(f"Cartas selecionadas:")
        color = "green"
    else:
        print(f"Você descartou:")
        color = "green"

    previous_number = None
    for card in player_deck:
        if card != previous_number:
            print()
        print_deck(f"[{card}|{game.cards[card]}]", color, new_line=False)
        previous_number = card

    print("\n")
