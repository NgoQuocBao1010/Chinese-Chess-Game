import pygame

from utils import Color, Configuration
from chessBoard import BoardGame

# Window's Configuration
WIN_WIDTH = Configuration.WIN_WIDTH  # height and width of window
WIN_HEIGHT = Configuration.WIN_HEIGHT

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))  # initilize win form
pygame.display.set_caption("LINE 98")  # win caption
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

RED_TURN = Configuration.RED_SIDE
GREEN_TURN = Configuration.BLUE_SIDE



def draw(board, turn):
    '''
    Drawing the game to window
    '''
    WIN.fill(Color.BLACK)
    board.drawGrid()
    textsurface = myfont.render(f'This is {turn} turn', False, Color.TURQUOISE)
    WIN.blit(textsurface,(0,0))
    pygame.display.update()


def main():
    '''
    Main function
    '''
    board = BoardGame(WIN)
    selectedPiece = None

    turn = "Red"

    run = True
    while run:
        draw(board, turn)
        # Loop through all events in 1 frames
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                boardPos = board.isClicked(pos)
                if boardPos:
                    if not selectedPiece:  # if there is no piece that already selected
                        selectedPiece = board.chessPieceCheck(pos)

                        if selectedPiece:  # if there is a clicked piece
                            movables = selectedPiece.checkPossibleMove(board.grid)
                            board.movables = movables
                    else:  # if there is a selected piece
                        # if selected piece is clicked again, unselect it
                        if selectedPiece.isClicked(pos):
                            selectedPiece.changeStatus(selected=False)
                            selectedPiece = None
                            board.movables = []
                        # if another position is clicked
                        else:
                            # if piece can move to that position
                            if boardPos in board.movables:
                                board.movePiece(selectedPiece, boardPos)
                                selectedPiece.changeStatus(selected=False)
                                selectedPiece = None
                                board.movables = []
                                turn = board.switchTurn()
                            else:
                                print(f"Cant move there {boardPos}")


if __name__ == "__main__":
    main()
