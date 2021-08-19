import pygame

# Width and height of the application
WIN_WIDTH = 900
WIN_HEIGHT = 600

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


class ChessImages:
    RED_CHARIOT = pygame.image.load("./images/red-car.png")
    RED_CANNON = pygame.image.load("./images/red-cannon.png")
    RED_HORSE = pygame.image.load("./images/red-horse.png")
    RED_ELEPHANT = pygame.image.load("./images/red-elephant.png")
    RED_SOLDIER = pygame.image.load("./images/red-pawn.png")
    RED_ADVISOR = pygame.image.load("./images/red-bodyguard.png")
    RED_LORD = pygame.image.load("./images/red-king.png")

    BLUE_CHARIOT = pygame.image.load("./images/blue-car.png")
    BLUE_CANNON = pygame.image.load("./images/blue-cannon.png")
    BLUE_HORSE = pygame.image.load("./images/blue-horse.png")
    BLUE_ELEPHANT = pygame.image.load("./images/blue-elephant.png")
    BLUE_SOLDIER = pygame.image.load("./images/blue-pawn.png")
    BLUE_ADVISOR = pygame.image.load("./images/blue-bodyguard.png")
    BLUE_LORD = pygame.image.load("./images/blue-king.png")
        
        
        



