import pygame

from utils import Color
from chesspiece import ChessPiece

# Window's Configuration
WIN_WIDTH = WIN_HEIGHT = 800                                # height and width of window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))       # initilize win form
pygame.display.set_caption("LINE 98")                       # win caption



class BoardGame():
    def __init__(self):
        self.rows = 9
        self.cols = 8

        self.gap = 60
        self.border = 30

        self.width = self.cols * self.gap
        self.height = self.rows * self.gap

        self.grid = [[False for _ in range(self.cols + 1)] for _ in range(self.rows + 1)]  # contains info of all postions in the board
        self.activePices = []  # contains all active pieces all the board

        self.generatePosition()
        self.makeGrid()
    
    def isClicked(self, pos=None):
        '''
        Take mouse clicked positon as an argument
        Check if mouse is clicked on the board
        '''
        if not pos:
            return None
        
        clickX, clickY = pos

        if clickX < self.x - self.border or clickX > self.x + self.width + self.border:
            return False
        
        if clickY < self.y - self.border or clickY > self.y + self.height + self.border:
            return False
        
        return True

    def chessPieceCheck(self, pos=None):
        if not pos:
            return
        
        for piece in self.activePices:
            if piece.changeStatus(pos):
                return piece
        
        return None
    
    def generatePosition(self):
        '''
        Calculate the coordinate of the board
        The board should be center horizontally and occupied 75% bottom half of the window
        '''

        self.x = (WIN_WIDTH - self.width) / 2
        self.y = WIN_HEIGHT * 25 / 100

    def makeGrid(self):
        c1 = ChessPiece(self.getCoordinateFromPosition((9, 0)))
        c2 = ChessPiece(self.getCoordinateFromPosition((2, 7)))

        self.activePices.append(c1) 
        self.activePices.append(c2) 
        
        self.grid[9][0] = True
        self.grid[2][7] = True

    def drawGrid(self, win):
        '''
        Draw the chess board
        '''

        riverCoordinate = ()
        
        # Draw all the lines
        for row in range(self.rows + 1):
            pygame.draw.line(win, Color.GREY, (self.x, self.y + row * self.gap), (self.x + self.width, self.y + row * self.gap), 2)

            if row == self.rows // 2:
                riverCoordinate = (self.x + 2 , self.y + row * self.gap + 2)


            for col in range(self.cols + 1):
                pygame.draw.line(win, Color.GREY, (col * self.gap + self.x, self.y), (col * self.gap + self.x, self.height + self.y), 2)
        
        # Draw the palace
        palaceCoors = [
            ((self.x + self.gap * 3, self.y), (self.x + self.gap * 5, self.y + self.gap * 2)),
            ((self.x + self.gap * 5, self.y), (self.x + self.gap * 3, self.y + self.gap * 2)),
            ((self.x + self.gap * 3, self.y + self.gap * 7), (self.x + self.gap * 5, self.y + self.gap * 9)),
            ((self.x + self.gap * 5, self.y + self.gap * 7), (self.x + self.gap * 3, self.y + self.gap * 9)),
        ]

        for point1, point2 in palaceCoors:
            pygame.draw.line(win, Color.GREY, point1, point2, 2)
            # pygame.draw.circle(win, Color.BLUE, point1, 25)

        # Draw the river
        pygame.draw.rect(win, Color.WHITE, pygame.Rect(*riverCoordinate, self.width - 2, self.gap - 2))

        # Draw the border
        self.rectangle = pygame.draw.rect(
            win, 
            Color.BLACK, 
            (self.x - self.border, self.y - self.border, self.width + self.border * 2, self.height + self.border * 2), 
            2
        )

        for piece in self.activePices:
            piece.draw(win)

    def getCoordinateFromPosition(self, position=None):
        '''
        Get the centre coordinate of a chess piece by giving its row and cols
        '''
        if not position:
            return None
        
        row, col = position

        x = self.x + self.gap * col
        y = self.y + self.gap * row
        return (x, y)
    

def draw(board):
    WIN.fill(Color.WHITE)
    board.drawGrid(WIN)
    pygame.display.update()


def main():
    board = BoardGame()
    selectedPiece = None

    run = True
    while run:
        draw(board)
        # Loop through all events in 1 frames
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if board.isClicked(pos):
                    if not selectedPiece:
                        selectedPiece = board.chessPieceCheck(pos)
                    else:
                        selectedPiece.changeStatus(pos)



if __name__ == '__main__':
    main()