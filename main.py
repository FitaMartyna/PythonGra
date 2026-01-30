# superFarmer gra - projekt
# autor: Martyna Fita
# przedmiot: Programowanie w językach funkcyjnych

import pygame

from game import GameState, Game, execute_turn, end_turn
from gui import GUI, initialize_GUI_0, initialize_GUI_1, initialize_GUI_2, initialize_GUI_3, initialize_GUI_4, \
    initialize_GUI_5, initialize_GUI_6


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Gra SuperFarmer")
    game = True
    GUI_state = 0
    game_state = None
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                if GUI_state == 0 and GUI.Start.collidepoint(position):
                    game_state = GameState(Game.number_of_players)
                    Game.queue = [i for i in range(Game.number_of_players)]
                    GUI_state = 5
                elif GUI_state == 0 and GUI.Settings.collidepoint(position):
                    GUI_state = 1
                elif GUI_state == 0 and GUI.Players.collidepoint(position):
                    GUI_state = 2
                elif GUI_state == 0 and GUI.How_To_Play.collidepoint(position):
                    GUI_state = 3
                elif GUI_state == 0 and GUI.Information.collidepoint(position):
                    GUI_state = 4
                elif GUI_state != 6 and GUI.Back.collidepoint(position):
                    GUI_state = 0
                elif GUI_state == 1:
                    for p in GUI.buttons:
                        p.handle_click(position)
                elif GUI_state == 5 and GUI.Roll_Dice.collidepoint(position) and not Game.roll_made:
                    Game.Exchange = 0
                    Game.exchange_made = True
                    game_state = execute_turn(game_state)
                    Game.roll_made = True
                elif GUI_state == 5 and GUI.Exchange.collidepoint(position) and not Game.exchange_made and Game.move_made == 0:
                    Game.Exchange = 1
                    Game.exchange_made = True
                elif GUI_state == 5 and Game.Exchange == 1:
                    for p in GUI.exchange_buttons:
                        p.handle_click(position)
                elif GUI_state == 5 and GUI.End.collidepoint(position):
                    victory = end_turn(game_state)
                    if victory:
                        GUI_state = 6
                elif GUI_state == 6 and GUI.Exit.collidepoint(position):
                    game = False
                elif GUI_state == 6 and GUI.BackToMenu.collidepoint(position):
                    GUI_state = 0

            if GUI_state == 2:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    GUI.active_field = None
                    for i, field in enumerate(GUI.name_fields):
                        if field.collidepoint(event.pos):
                            GUI.active_field = i
                            break
                elif event.type == pygame.KEYDOWN and GUI.active_field is not None:
                    if event.key == pygame.K_BACKSPACE:
                        GUI.field_text[GUI.active_field] = GUI.field_text[GUI.active_field][:-1]
                    else:
                        GUI.field_text[GUI.active_field] += event.unicode

        if GUI_state == 0:
            initialize_GUI_0()
        if GUI_state == 1:
            initialize_GUI_1()
        if GUI_state == 2:
            initialize_GUI_2()
        if GUI_state == 3:
            initialize_GUI_3()
        if GUI_state == 4:
            initialize_GUI_4()
        if GUI_state == 5:
            initialize_GUI_5(game_state, Game.queue)
        if GUI_state == 6:
            initialize_GUI_6()


if __name__ == "__main__":
    main()