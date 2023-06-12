font_colour = {
    "black": "\033[1;30m",
    "purple": "\033[1;31m",
    "green": "\033[1;32m",
    "yellow": "\033[1;33m",
    "blue": "\033[1;34m",
    "red": "\033[1;35m",
    "cyan": "\033[1;36m",
    "grey": "\033[1;37m",
    "bold": "\033[;1m",
    "clear": "\033[m",
}


def font(c):
    return font_colour[c]


def print_warning(msg):
    print(f'{font("yellow")}WARNING: {msg}{font("clear")}')


def print_error(msg):
    print(f'{font("red")}ERROR: {msg}{font("clear")}')


def print_success(msg):
    print(f'{font("green")}SUCCESS: {msg}{font("clear")}')


def print_info(msg):
    print(f'{font("cyan")}INFO: {msg}{font("clear")}')


def print_deck(deck):
    """
    -> This function print the deck
    :param deck: list of cards
    :return: print the deck
    """
    print(f'{font("purple")}{deck}{font("clear")}')


def print_move(deck):
    """
    -> This function print the deck
    :param deck: list of cards
    :return: print the deck
    """
    print(f'{font("cyan")}{deck}{font("clear")}')