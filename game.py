import random


class Game:
    exchanges = [[6, "rabbit", 1, "sheep"], [2, "sheep", 1, "pig"], [3, "pig", 1, "cow"], [2, "cow", 1, "horse"],
               [1, "sheep", 1, "small_dog"], [1, "cow", 1, "big_dog"]]
    files = {
        "rabbit": "pictures/rabbit.jpg",
        "sheep": "pictures/sheep.jpg",
        "pig": "pictures/pig.jpg",
        "cow": "pictures/cow.jpg",
        "horse": "pictures/horse.jpg",
        "fox": "pictures/fox.png",
        "wolf": "pictures/wolf.png",
        "small_dog": "pictures/small_dog.png",
        "big_dog": "pictures/big_dog.png"
    }
    limits = {
        "rabbit": 60,
        "sheep": 24,
        "pig": 20,
        "cow": 12,
        "horse": 6,
        "small_dog": 1,
        "big_dog": 2
    }
    farm_animals = ["rabbit", "sheep", "pig", "cow", "horse"]
    initial_values = {
        "rabbit": 1,
        "sheep": 0,
        "pig": 0,
        "cow": 0,
        "horse": 0
    }
    number_of_players = 2
    queue = []
    choice = 1
    victory = 0
    result = ()
    move_made = 0
    Names = ["Player 1", "Player 2", "Player 3", "Player 4"]
    roll_made = False
    exchange_made = False
    Exchange = 0

def create_player(id: int) -> dict:
    return {
    "id": id,
    "rabbit": Game.initial_values["rabbit"],
    "sheep": Game.initial_values["sheep"],
    "pig": Game.initial_values["pig"],
    "cow": Game.initial_values["cow"],
    "horse": Game.initial_values["horse"],
    "small_dog": 0,
    "big_dog": 0
    }

def roll_dice(dice1: list, dice2: list) -> tuple:
    return random.choice(dice1), random.choice(dice2)


def apply_limits(player: dict) -> None:
    for animal, limit in Game.limits.items():
        if player[animal] > limit:
            player[animal] = limit


def player_roll(id: int, game_state: dict) -> dict:
    blue = ["rabbit"] * 6 + ["sheep"] * 3 + ["pig"] + ["cow", "wolf"]
    orange = ["rabbit"] * 6 + ["sheep"] * 2 + ["pig"] * 2 + ["horse", "fox"]

    result = roll_dice(orange, blue)
    Game.result = result
    player = game_state["players"][id]

    player = {
        animal:
            player[animal]
            + ((player[animal] + result.count(animal)) // 2)
            if animal in Game.farm_animals and result.count(animal) > 0
            else player[animal]
        for animal in player
    }

    if "fox" in result:
        if player["small_dog"] >= 1:
            player["small_dog"] = 0
        else:
            player["rabbit"] = 1

    if "wolf" in result:
        if player["big_dog"] >= 1:
            player["big_dog"] = 0
        else:
            player["sheep"] = 0
            player["pig"] = 0
            player["cow"] = 0

    apply_limits(player)

    new_game_state = game_state.copy()
    new_game_state["players"][id] = player

    return new_game_state


def create_players(number_of_players: int) -> list:
    players = [create_player(i) for i in range(number_of_players)]
    return players


def GameState(number_of_players: int) -> dict:
    game_state = {
        "players": create_players(number_of_players),
    }
    return game_state


def execute_turn(game_state: dict) -> dict:
    player_id = Game.queue[0]
    new_state = player_roll(player_id, game_state)
    Game.move_made = 1
    return new_state

def exchange(game_state: dict, choice: int) -> dict:
    player_id = Game.queue[0]
    new_game_state = game_state.copy()

    if new_game_state["players"][player_id][Game.exchanges[choice-1][1]] >= Game.exchanges[choice-1][0]:
        new_game_state["players"][player_id][Game.exchanges[choice-1][3]] += Game.exchanges[choice-1][2]
        new_game_state["players"][player_id][Game.exchanges[choice-1][1]] -= Game.exchanges[choice-1][0]
    apply_limits(new_game_state["players"][player_id])
    return new_game_state


def execute_exchange(game_state: dict, nr: int) -> None:
    new_state = exchange(game_state, nr)
    game_state.update(new_state)
    Game.Exchange = 0
    Game.exchange_made = True

def end_turn(game_state: dict) -> bool:
    Game.result = ()
    Game.Exchange = 0
    queue = Game.queue
    victory = check_victory(game_state['players'][queue[0]])
    new_queue = queue[1:] + [queue[0]]
    Game.queue = new_queue
    Game.move_made = 0
    Game.roll_made = False
    Game.exchange_made = False
    return victory


def check_victory(player) -> bool:
    return all(player[animal] >= 1 for animal in Game.farm_animals)
