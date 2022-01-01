import pygame

from game.utils import Color, WIN_HEIGHT, WIN_WIDTH
from game.controlPanel import ControlPanel
from game.game import Game


# Increase sharpness
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Window's Configuration
WIN_WIDTH = WIN_WIDTH  # height and width of window
WIN_HEIGHT = WIN_HEIGHT

WIN = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE
)  # initilize win form
pygame.display.set_caption("Chinese Chess Game")  # win caption
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 15)


def draw(game, controlPanel):
    """
    Drawing the game to window
    """
    WIN.fill(Color.BLACK)
    game.updateGame()

    controlPanel.draw(WIN)
    pygame.display.update()


def main():
    """
    Main function
    """

    game = Game(WIN)
    controlPanel = ControlPanel(game)

    run = True
    while run:
        draw(game, controlPanel)
        # Loop through all events in 1 frames
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if not game.isOver:
                    game.checkForMove(pos)
                else:
                    print("Game is over")

                controlPanel.checkForClick(pos)


if __name__ == "__main__":
    main()
