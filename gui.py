import pygame
from pygame import SurfaceType

from button import Button
from game import *
from utils import decrease_number_of_players, increase_number_of_players, decrease, increase


class GUI:
    window = pygame.display.set_mode((950, 600))
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (45, 156, 80)
    # start screen
    Start = pygame.Rect(400, 480, 150, 70)
    Settings = pygame.Rect(100, 20, 150, 70)
    Players = pygame.Rect(300, 20, 150, 70)
    How_To_Play = pygame.Rect(500, 20, 150, 70)
    Information = pygame.Rect(700, 20, 150, 70)
    # main screen
    Name = pygame.Rect(400, 20, 150, 50)
    Roll_Dice = pygame.Rect(200, 500, 150, 50)
    Exchange = pygame.Rect(400, 500, 150, 50)
    End = pygame.Rect(600, 500, 150, 50)
    # exchanges
    exchange_buttons = []
    exchange_rectangles = [
        pygame.Rect(100, 300, 200, 70),
        pygame.Rect(100, 400, 200, 70),
        pygame.Rect(375, 300, 200, 70),
        pygame.Rect(375, 400, 200, 70),
        pygame.Rect(650, 300, 200, 70),
        pygame.Rect(650, 400, 200, 70),
    ]
    # settings window
    Number_Of_Players = pygame.Rect(50, 20, 200, 70)
    Starting_Values = pygame.Rect(50, 110, 250, 70)
    buttons = []
    Back = pygame.Rect(780, 510, 150, 70)
    # names
    name_fields = []
    field_text = ["Player 1", "Player 2", "Player 3", "Player 4"]
    active_field = None
    # end screen
    BackToMenu = pygame.Rect(300, 400, 150, 70)
    Exit = pygame.Rect(500, 400, 150, 70)

def draw_text(text: str, color: tuple, x: int, y: int) -> SurfaceType:
    font = pygame.font.SysFont(None, 32)
    text_surface = font.render(text, True, color)
    GUI.window.blit(text_surface, (x, y))
    return text_surface


def draw_image(file: str, x: int, y: int) -> None:
    image = pygame.image.load(file)
    GUI.window.blit(image, (x, y))


def draw_small_image(file: str, x: int, y: int, width: int, height: int) -> None:
    image = pygame.image.load(file)
    image = pygame.transform.scale(image, (width, height))
    GUI.window.blit(image, (x, y))


def draw_multiline_text(text: str, color: tuple, x: int, y: int, max_width: int,
                                 font = None, line_spacing = 5) -> None:
    if font is None:
        font = pygame.font.SysFont(None, 28)
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    words = text.split(' ')
    line = ""
    y_offset = 0

    for word in words:
        test_line = line + word + " "
        width, height = font.size(test_line)
        if width > max_width:
            text_surface = font.render(line, True, color)
            GUI.window.blit(text_surface, (x, y + y_offset))
            y_offset += height + line_spacing
            line = word + " "
        else:
            line = test_line

    if line:
        text_surface = font.render(line, True, color)
        GUI.window.blit(text_surface, (x, y + y_offset))

def initialize_exchange_buttons(game_state: dict) -> None:
    GUI.exchange_buttons.clear()

    for i, rectangle in enumerate(GUI.exchange_rectangles):
        GUI.exchange_buttons.append(
            Button(
                rectangle,
                lambda n=i+1: execute_exchange(game_state, n),
                ""
            )
        )

def draw_button(rectangle: pygame.rect.Rect, text: str, active: bool) -> None:
    border_color = (39, 242, 80) if active else (80,80,80)
    pygame.draw.rect(GUI.window, GUI.white, rectangle)
    pygame.draw.rect(GUI.window, border_color, rectangle, 5)
    draw_text(text, GUI.black, rectangle.x + 10, rectangle.y + 10)


def draw_exchange(exchange: int, rectangle: pygame.rect.Rect):
    amount1, what1, amount2, what2 = Game.exchanges[exchange]

    x = rectangle.x
    y = rectangle.y

    draw_text(str(amount1), GUI.black, x + 10, y + 25)
    draw_small_image(Game.files[what1], x + 30, y + 10, 50, 50)
    draw_text("=> " + str(amount2), GUI.black, x + 85, y + 25)
    draw_small_image(Game.files[what2], x + 135, y + 10, 50, 50)


# start menu
def initialize_GUI_0() -> None:
    GUI.window.fill(GUI.green)

    # top menu
    pygame.draw.rect(GUI.window, GUI.white, GUI.Settings)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Players)
    pygame.draw.rect(GUI.window, GUI.white, GUI.How_To_Play)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Information)

    draw_text("Ustawienia", GUI.black, 115, 45)
    draw_text("Gracze", GUI.black, 330, 45)
    draw_text("Jak grać", GUI.black, 530, 45)
    draw_text("Informacje", GUI.black, 720, 45)

    logo = "pictures/logo.jpg"
    draw_image(logo, 362, 187)

    pygame.draw.rect(GUI.window, GUI.white, GUI.Start)
    draw_text("Start", GUI.black, 445, 505)

    pygame.display.update()


# Ustawienia
def initialize_GUI_1() -> None:
    GUI.window.fill(GUI.green)
    GUI.buttons.clear()
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Number_Of_Players)
    draw_text("Liczba graczy: " + str(Game.number_of_players), GUI.black, 60, 45)
    GUI.buttons.append(Button(
        pygame.Rect(270, 35, 40, 40),
        lambda: decrease_number_of_players(),
        "-"
    ))
    GUI.buttons.append(Button(
        pygame.Rect(330, 35, 40, 40),
        lambda: increase_number_of_players(),
        "+"
    ))
    pygame.draw.rect(GUI.window, GUI.white, GUI.Starting_Values)
    draw_text("Wartości początkowe", GUI.black, 60, 135)
    y = 200
    for file in Game.files:
        if y <= 520:
            pygame.draw.rect(GUI.window, GUI.white, pygame.Rect(120, y, 50, 50))
            draw_small_image(Game.files[file], 50, y, 50, 50)
            draw_text(str(Game.initial_values[file]), GUI.black, 140, y+15)

            GUI.buttons.append(
                Button(
                    pygame.Rect(200, y+5, 40, 40),
                    lambda p=file: decrease(p),
                    "-"
                )
            )

            GUI.buttons.append(
                Button(
                    pygame.Rect(260, y+5, 40, 40),
                    lambda p=file: increase(p),
                    "+"
                )
            )
            y += 70
        else:
            break

    for p in GUI.buttons:
        p.draw(GUI.window, draw_text, GUI.black)

    pygame.display.update()

# Gracze
def initialize_GUI_2() -> None:
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    y = 50
    for i in range(Game.number_of_players):
        Rect = pygame.Rect(40, y, 50, 50)
        pygame.draw.rect(GUI.window, GUI.white, Rect)
        draw_text(str(i+1), GUI.black, Rect.x + 20, Rect.y + 15)
        y += 70

    if not GUI.name_fields or len(GUI.name_fields) != Game.number_of_players:
        GUI.name_fields = [pygame.Rect(100, 50 + i * 70, 200, 50) for i in range(Game.number_of_players)]
        GUI.field_text = [""] * Game.number_of_players

    for i, field in enumerate(GUI.name_fields):
        pygame.draw.rect(GUI.window, GUI.white, field)
        text_surface = draw_text(GUI.field_text[i], GUI.black, field.x + 5, field.y + 10)
        field.w = max(150, text_surface.get_width() + 10)
        if GUI.active_field == i:
            pygame.draw.rect(GUI.window, GUI.black, field, 2)
    pygame.display.update()


# Jak grać
def initialize_GUI_3() -> None:
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    text = """Jesteś hodowcą zwierząt i chcesz zostać superfarmerem. Twoje zwierzęta rozmnażają się, 
a to przynosi ci zysk. Możesz zamieniać wyhodowane zwierzęta na inne, jeśli uznasz, 
że to się opłaca. Aby zwyciężyć, musisz jako pierwszy uzyskać stado złożone co najmniej 
z konia, krowy, świni, owcy i królika. Jednak wszystkie Twoje plany mogą pozostać tylko 
w sferze marzeń, jeśli nie zachowasz należytej ostrożności! W okolicy grasują bowiem 
wilk i lis, których łatwym łupem mogą stać się Twoje zwierzęta. 
W grze może brać udział od 2 do 4 osób. Każdy gracz na początek otrzymuje jednego królika. 
Gracze rzucają kolejno, zawsze dwiema kostkami. Jeśli gracz rzuci kostkami tak, że na 
obu wypadnie takie samo zwierzę, to dostaje to zwierzę ze stada głównego. Gdy gracz ma 
już jakieś zwierzęta, to po rzucie otrzymuje ze stada tyle zwierząt wyrzuconego 
gatunku, ile ma pełnych par tego gatunku ( łącznie z wyrzuconymi na kostkach).Przed każdym rzutem kostkami gracz, 
jeśli zechce może dokonać jednej wymiany. 
Wymiany odbywają się zgodnie z przelicznikami przedstawionymi w tabeli wymian."""

    draw_multiline_text(text, GUI.black, 50, 50, 850)
    pygame.display.update()


# Informacje
def initialize_GUI_4() -> None:
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    text = """Superfarmer to gra, która powstała w Warszawie w 1943 roku. Nosiła wtedy tytuł 
„Hodowla zwierzątek". Grę wymyślił wybitny polski matematyk, profesor Uniwersytetu Warszawskiego, 
Karol Borsuk. Po zajęciu Warszawy hitlerowcy zamknęli Uniwersytet, w wyniku tego profesor stracił pracę. 
Sprzedaż gry była pomysłem profesora na ratowanie rodzinnego budżetu. Zestawy do gry wykonywane 
były metodami domowymi przez żonę profesora, panią Zofię Borsukową. 
Umieszczone w grze rysunki zwierzątek namalowała Janina Śliwicka. W krótkim czasie 
gra zyskała nadspodziewanie wielką popularność nie tylko wśród przyjaciół, lecz także 
w szerokich kręgach dalszych znajomych i nieznajomych osób. W domu państwa 
Borsuków rozdzwonił się telefon, a głos w słuchawce coraz częściej zadawał pytanie: 
Czy to hodowla zwierzątek? Po potwierdzeniu zwykle następowało zamówienie. 
Gra bawiła nie tylko dzieci, wciągała także i dorosłych pomagając im przetrwać 
ponure okupacyjne wieczory. Gry spłonęły wraz z miastem w czasie powstania warszawskiego, w sierpniu 1944r. 
Szczęśliwie jeden z egzemplarzy zachował się poza Warszawą i wiele lat po wojnie wrócił 
do rodziny Borsuków. - GRANNA, Warszawa, marzec 2013"""

    draw_multiline_text(text, GUI.black, 50, 50, 850)
    pygame.display.update()


# Main screen
def initialize_GUI_5(game_state, queue) -> None:
    name = GUI.field_text[queue[0]]
    y = 110
    GUI.window.fill(GUI.green)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Back)
    draw_text("Powrót", GUI.black, 815, 535)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Name)
    text_surface = draw_text(str(game_state['players'][queue[0]]['id'] + 1) + " " + name, GUI.black, 420, 35)
    GUI.Name.w = max(150, text_surface.get_width() + 30)
    draw_image("pictures/rabbit.jpg", 50, y)
    draw_image("pictures/sheep.jpg", 230, y)
    draw_image("pictures/pig.jpg", 410, y)
    draw_image("pictures/cow.jpg", 590, y)
    draw_image("pictures/horse.jpg", 770, y)
    draw_text(str(game_state['players'][queue[0]]["rabbit"]), GUI.black, 100, 250)
    draw_text(str(game_state['players'][queue[0]]["sheep"]), GUI.black, 270, 250)
    draw_text(str(game_state['players'][queue[0]]["pig"]), GUI.black, 460, 250)
    draw_text(str(game_state['players'][queue[0]]["cow"]), GUI.black, 640, 250)
    draw_text(str(game_state['players'][queue[0]]["horse"]), GUI.black, 820, 250)

    draw_button(
        GUI.Roll_Dice,
        "Rzuć kostką",
        not Game.roll_made
    )
    draw_button(
        GUI.Exchange,
        "Wymiany",
        not Game.exchange_made
    )
    draw_button(
        GUI.End,
        "Zakończ turę",
        Game.roll_made
    )

    if len(Game.result) > 0:
        draw_image(Game.files[Game.result[0]], 300, 300)
        draw_image(Game.files[Game.result[-1]], 500, 300)
    if Game.Exchange == 1:
        initialize_exchange_buttons(game_state)

        for i, p in enumerate(GUI.exchange_buttons):
            pygame.draw.rect(GUI.window, GUI.white, p.rectangle)
            draw_exchange(i, p.rectangle)

    if game_state["players"][queue[0]]["small_dog"] >= 1:
        draw_small_image(Game.files["small_dog"], 50, 20, 50, 50)
    if game_state["players"][queue[0]]["big_dog"] >= 1:
        draw_small_image(Game.files["big_dog"], 130, 20, 50, 50)
    pygame.display.update()

# End screen
def initialize_GUI_6() -> None:
    GUI.window.fill(GUI.green)
    draw_text("Zwycięzcą jest " + Game.Names[Game.queue[-1]], GUI.white, 350, 200)
    pygame.draw.rect(GUI.window, GUI.white, GUI.BackToMenu)
    draw_text("Menu główne", GUI.black, GUI.BackToMenu.x+5, GUI.BackToMenu.y+25)
    pygame.draw.rect(GUI.window, GUI.white, GUI.Exit)
    draw_text("Wyjdź z gry", GUI.black, GUI.Exit.x + 13, GUI.Exit.y + 25)
    pygame.display.update()

