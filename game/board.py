import pygame
import os
import numpy as np

from .pieces import Chariot, Cannon, Horse, Elephant, Soldier, Advisor, Lord
from .utils import Color, RED_SIDE, BLUE_SIDE, WIN_HEIGHT, WIN_WIDTH


class BoardGame:
    def __init__(self):
        self.rows = 9
        self.cols = 8

        self.gap = WIN_WIDTH // 15
        self.border = 20

        self.width = self.cols * self.gap
        self.height = self.rows * self.gap

        # contains info of all postions in the board
        self.grid = [[None for _ in range(self.cols + 1)] for _ in range(self.rows + 1)]
        # contains all active pieces all the board
        self.activePices = []
        # contains all movable positions
        self.movables = []
        # info of which side's turn
        self.turn = RED_SIDE
        # Varible contain to LORD pieces of either side
        self.blueLord = None
        self.redLord = None

        self.calculatePostion()
        self.makeGrid()

    def addNewPiece(self, type, position, side):
        """
        Add new piece to the board
        Help set up the board
        """
        chessTypes = {
            "chariot": Chariot,
            "cannon": Cannon,
            "horse": Horse,
            "elephant": Elephant,
            "soldier": Soldier,
            "advisor": Advisor,
            "lord": Lord,
        }

        centrePoint = self.getCoordinateFromPosition(position)
        newPiece = chessTypes.get(type)(
            centrePoint=centrePoint, position=position, side=side
        )
        self.activePices.append(newPiece)

        if isinstance(newPiece, Lord):
            if newPiece.side == RED_SIDE:
                self.redLord = newPiece
            else:
                self.blueLord = newPiece

        row, col = position
        self.grid[row][col] = newPiece

    def readPreset(self):
        directory = os.path.dirname(__file__)
        presetPath = os.path.join(directory, "presets/standard.cfg")
        seperator = " ******** "

        with open(presetPath, "r") as f:
            lines = f.readlines()

        result = []
        for line in lines:
            line = line[:-1]

            piece, row, col, side = line.split(seperator)

            row, col = int(row), int(col)
            position = (row, col)

            side = RED_SIDE if side == "red" else BLUE_SIDE

            result.append((piece, position, side))

        return result

    def makeGrid(self):
        """
        Set up all the pieces and their positions in the board at the beginning of the game
        """
        pieces = self.readPreset()

        for piece, position, side in pieces:
            self.addNewPiece(piece, position, side)

        # Check all possible move for all the pieces after initialize the board
        for piece in self.activePices:
            piece.checkPossibleMove(self.grid)

    def drawGrid(self, win):
        """
        Draw the chess board
        """

        riverCoordinate = ()

        # Draw all the lines
        for row in range(self.rows + 1):
            pygame.draw.line(
                win,
                Color.GREY,
                (self.x, self.y + row * self.gap),
                (self.x + self.width, self.y + row * self.gap),
                2,
            )

            if row == self.rows // 2:
                riverCoordinate = (self.x + 2, self.y + row * self.gap + 2)

            for col in range(self.cols + 1):
                pygame.draw.line(
                    win,
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
            pygame.draw.line(win, Color.GREY, point1, point2, 2)

        # Draw the river
        pygame.draw.rect(
            win,
            Color.BLACK,
            pygame.Rect(*riverCoordinate, self.width - 2, self.gap - 2),
        )

        # Draw the border
        self.rectangle = pygame.draw.rect(
            win,
            Color.WHITE,
            (
                self.x - self.border,
                self.y - self.border,
                self.width + self.border * 2,
                self.height + self.border * 2,
            ),
            2,
        )

        for piece in self.activePices:
            piece.draw(win)

        for position in self.movables:
            coor = self.getCoordinateFromPosition(position)
            pygame.draw.circle(win, Color.GREEN, coor, 7)

    def calculatePostion(self):
        """
        Calculate the coordinate of the board
        The board position will be center verically and occupied left side of the screen
        """

        self.x = 50
        self.y = (WIN_HEIGHT - self.height) / 2

    def getCoordinateFromPosition(self, position=None):
        """
        Get the centre coordinate of a chess piece by giving its row and column,
        Which means the corner of a square from the board
        """
        if not position:
            return None

        row, col = position

        x = self.x + self.gap * col
        y = self.y + self.gap * row
        return (x, y)

    def getPositionFromCoordinate(self, coordinate):
        """
        Get row and column from given game's coordinate
        """
        x, y = coordinate
        col = round((x - self.x) / self.gap)
        row = round((y - self.y) / self.gap)

        return (row, col)

    def getPiece(self, position):
        """
        Get piece from given location
        """
        row, col = position
        return self.grid[row][col]

    def getLord(self, side):
        """
        Return the lord piece depends on the given side
        """
        return self.redLord if side == RED_SIDE else self.blueLord

    def isClicked(self, clickedPos=None):
        """
        Take mouse clicked positon as an argument
        Check if mouse is clicked on the board
        """
        if not clickedPos:
            return False

        clickX, clickY = clickedPos

        if clickX < self.x - self.border or clickX > self.x + self.width + self.border:
            return False

        if clickY < self.y - self.border or clickY > self.y + self.height + self.border:
            return False

        return True

    def deselectPiece(self, piecePos):
        """
        Deselect a piece
        """
        piece = self.getPiece(piecePos)
        piece.deselect()
        self.movables = []

        return None

    def movePiece(self, oldPos, newPos=(0, 0)):
        """
        Moving the piece and update the board
        """

        lordPiece = self.getLord(side=self.turn)
        lordPiece.mated = False

        oldRow, oldCol = oldPos
        newRow, newCol = newPos

        self.deselectPiece(oldPos)

        # Capture a piece if there is one in a new pos
        if self.grid[newRow][newCol]:
            self.activePices.remove(self.grid[newRow][newCol])

        # Swap piece's position to new position
        movingPiece = self.grid[oldRow][oldCol]
        self.grid[oldRow][oldCol] = None
        self.grid[newRow][newCol] = movingPiece

        newCentrePoint = self.getCoordinateFromPosition(newPos)
        movingPiece.moveToNewSpot(centrePoint=newCentrePoint, position=newPos)

        # Swich turn
        self.turn = RED_SIDE if self.turn == BLUE_SIDE else BLUE_SIDE

    def lordTolord(self):
        """
        Check if 2 lords are directly look at each other, which is an invalid move
        """
        row1, col1 = self.redLord.getPosition()
        row2, col2 = self.blueLord.getPosition()

        if col1 == col2:
            up = max(row1, row2)
            down = min(row1, row2)

            column = np.array(self.grid)[:, col1]

            for index in range(down + 1, up):
                if column[index] is not None:
                    return False

            return True
        else:
            return False
