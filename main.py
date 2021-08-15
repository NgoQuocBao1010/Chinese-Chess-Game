import pygame

from utils import Color
from chesspiece import ChessPiece, Rook

# Window's Configuration
WIN_WIDTH = WIN_HEIGHT = 600  # height and width of window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))  # initilize win form
pygame.display.set_caption("LINE 98")  # win caption


class BoardGame:
    def __init__(self, win):
        self.win = win
        self.rows = 9
        self.cols = 8

        self.gap = 40
        self.border = 15

        self.width = self.cols * self.gap
        self.height = self.rows * self.gap

        # contains info of all postions in the board
        self.grid = [
            [False for _ in range(self.cols + 1)] for _ in range(self.rows + 1)
        ]
        # contains all active pieces all the board
        self.activePices = []
        # contains all movable positions
        self.movables = []

        self.generatePosition()
        self.makeGrid()

    def makeGrid(self):
        rook = Rook(centrePoint=self.getCoordinateFromPosition((9, 0)), position=(9, 0))
        c2 = Rook(centrePoint=self.getCoordinateFromPosition((2, 7)), position=(2, 7))

        self.activePices.append(rook)
        self.activePices.append(c2)

        self.grid[9][0] = True
        self.grid[2][7] = True

    def drawGrid(self):
        """
        Draw the chess board
        """

        riverCoordinate = ()

        # Draw all the lines
        for row in range(self.rows + 1):
            pygame.draw.line(
                self.win,
                Color.GREY,
                (self.x, self.y + row * self.gap),
                (self.x + self.width, self.y + row * self.gap),
                2,
            )

            if row == self.rows // 2:
                riverCoordinate = (self.x + 2, self.y + row * self.gap + 2)

            for col in range(self.cols + 1):
                pygame.draw.line(
                    self.win,
                    Color.GREY,
                    (col * self.gap + self.x, self.y),
                    (col * self.gap + self.x, self.height + self.y),
                    2,
                )

        # Draw the palace
        palaceCoors = [
            (
                (self.x + self.gap * 3, self.y),
                (self.x + self.gap * 5, self.y + self.gap * 2),
            ),
            (
                (self.x + self.gap * 5, self.y),
                (self.x + self.gap * 3, self.y + self.gap * 2),
            ),
            (
                (self.x + self.gap * 3, self.y + self.gap * 7),
                (self.x + self.gap * 5, self.y + self.gap * 9),
            ),
            (
                (self.x + self.gap * 5, self.y + self.gap * 7),
                (self.x + self.gap * 3, self.y + self.gap * 9),
            ),
        ]
        for point1, point2 in palaceCoors:
            pygame.draw.line(self.win, Color.GREY, point1, point2, 2)
            # pygame.draw.circle(win, Color.BLUE, point1, 25)

        # Draw the river
        pygame.draw.rect(
            self.win,
            Color.WHITE,
            pygame.Rect(*riverCoordinate, self.width - 2, self.gap - 2),
        )

        # Draw the border
        self.rectangle = pygame.draw.rect(
            self.win,
            Color.BLACK,
            (
                self.x - self.border,
                self.y - self.border,
                self.width + self.border * 2,
                self.height + self.border * 2,
            ),
            2,
        )

        for piece in self.activePices:
            piece.draw(self.win)

        for position in self.movables:
            coor = self.getCoordinateFromPosition(position)
            pygame.draw.circle(self.win, Color.BLACK, coor, 5)

    def generatePosition(self):
        """
        Calculate the coordinate of the board
        The board should be center horizontally and occupied 75% bottom half of the window
        """

        self.x = (WIN_WIDTH - self.width) / 2
        self.y = WIN_HEIGHT * 25 / 100

    def getCoordinateFromPosition(self, position=None):
        """
        Get the centre coordinate of a chess piece by giving its row and cols
        """
        if not position:
            return None

        row, col = position

        x = self.x + self.gap * col
        y = self.y + self.gap * row
        return (x, y)

    def isClicked(self, pos=None):
        """
        Take mouse clicked positon as an argument
        Check if mouse is clicked on the board
        """
        if not pos:
            return None

        clickX, clickY = pos

        if clickX < self.x - self.border or clickX > self.x + self.width + self.border:
            return None

        if clickY < self.y - self.border or clickY > self.y + self.height + self.border:
            return None

        col = round((clickX - self.x) / self.gap)
        row = round((clickY - self.y) / self.gap)

        return (row, col)

    def chessPieceCheck(self, pos=None):
        if not pos:
            return None

        for piece in self.activePices:
            if piece.isClicked(pos):
                piece.changeStatus(selected=True)
                return piece

        return None

    def movePiece(self, piece, newPos=(0, 0)):
        """
        Moving the piece and update the board
        """
        oldRow, oldCol = piece.position
        newRow, newCol = newPos

        self.grid[oldRow][oldCol] = False
        self.grid[newRow][newCol] = True

        newCentrePoint = self.getCoordinateFromPosition(newPos)
        piece.moveToNewSpot(centrePoint=newCentrePoint, position=newPos)

        print(f"Moving {piece} to {newRow}, {newCol}")


def draw(board):
    WIN.fill(Color.WHITE)
    board.drawGrid()
    pygame.display.update()


def main():
    board = BoardGame(WIN)
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
                            else:
                                print(f"Cant move there {boardPos}")


if __name__ == "__main__":
    main()
