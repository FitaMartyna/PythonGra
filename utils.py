from game import Game


def decrease(file: str) -> None:
    if Game.initial_values[file] > 0:
        Game.initial_values[file] -= 1


def increase(file: str) -> None:
    if Game.initial_values[file] < 15:
        Game.initial_values[file] += 1


def decrease_number_of_players() -> None:
    if Game.number_of_players > 2:
        Game.number_of_players -= 1


def increase_number_of_players() -> None:
    if Game.number_of_players < 4:
        Game.number_of_players += 1

