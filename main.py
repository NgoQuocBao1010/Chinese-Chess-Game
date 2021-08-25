import pygame

# from utils import Color, Configuration
# from chessBoard import BoardGame

from game.utils import Color, RED_TURN, BLUE_TURN, WIN_HEIGHT, WIN_WIDTH
from game.board import BoardGame
from game.controlPanel import ControlPanel
from game.game import Game

# Window's Configuration
WIN_WIDTH = WIN_WIDTH  # height and width of window
WIN_HEIGHT = WIN_HEIGHT

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)  # initilize win form
pygame.display.set_caption("LINE 98")  # win caption
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)


def draw(game, controlPanel):
    '''
    Drawing the game to window
    '''
    WIN.fill(Color.BLACK)
    game.updateGame()


    # textsurface = myfont.render(f'{turn} has {movesLeft}', False, Color.RED)
    # WIN.blit(textsurface,(0,40))

    # textsurface = myfont.render(f'This is {turn} turn', False, Color.TURQUOISE)
    # WIN.blit(textsurface,(0,0))
    controlPanel.draw(WIN)
    pygame.display.update()


def main():
    '''
    Main function
    '''

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
