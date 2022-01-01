import pygame

pygame.font.init()

# Width and height of the application
WIN_WIDTH = 1200
WIN_HEIGHT = 900

# Red side, blue side indicator
RED_SIDE = RED_TURN = 1
BLUE_SIDE = BLUE_TURN = 0


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 255, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)


class Font:
    SCORE_TEXT_FONT = pygame.font.Font("./fonts/CursedTimerUlil-Aznm.ttf", 30)
    SCORE_FONT = pygame.font.Font("./fonts/CursedTimerUlil-Aznm.ttf", 30, bold=True)
    NORMAL_FONT = pygame.font.Font("./fonts/Poppins-Bold.ttf", 30)
    WRITING_FONT = pygame.font.Font("./fonts/Allison-Regular.ttf", 30)


class ChessImages:
    RED_CHARIOT = pygame.image.load("./images/pieces/red-car.png")
    RED_CANNON = pygame.image.load("./images/pieces/red-cannon.png")
    RED_HORSE = pygame.image.load("./images/pieces/red-horse.png")
    RED_ELEPHANT = pygame.image.load("./images/pieces/red-elephant.png")
    RED_SOLDIER = pygame.image.load("./images/pieces/red-pawn.png")
    RED_ADVISOR = pygame.image.load("./images/pieces/red-bodyguard.png")
    RED_LORD = pygame.image.load("./images/pieces/red-king.png")

    BLUE_CHARIOT = pygame.image.load("./images/pieces/blue-car.png")
    BLUE_CANNON = pygame.image.load("./images/pieces/blue-cannon.png")
    BLUE_HORSE = pygame.image.load("./images/pieces/blue-horse.png")
    BLUE_ELEPHANT = pygame.image.load("./images/pieces/blue-elephant.png")
    BLUE_SOLDIER = pygame.image.load("./images/pieces/blue-pawn.png")
    BLUE_ADVISOR = pygame.image.load("./images/pieces/blue-bodyguard.png")
    BLUE_LORD = pygame.image.load("./images/pieces/blue-king.png")
