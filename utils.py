import pygame


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
    RED_HORSE = pygame.image.load("./images/red-horse.png")
    RED_ELEPHANT = pygame.image.load("./images/red-elephant.png")
