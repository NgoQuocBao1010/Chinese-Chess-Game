import pygame
import numpy as np
from pprint import pprint

from .pieces import Chariot, Horse, Elephant, Soldier, Lord

from .utils import Color, RED_SIDE, BLUE_SIDE, WIN_HEIGHT, WIN_WIDTH


class BoardGame:
    def __init__(self):
        self.rows = 9
        self.cols = 8

        self.gap = 60
        self.border = 20

        self.width = self.cols * self.gap
        self.height = self.rows * self.gap

        # contains info of all postions in the board
        self.grid = [
            [None for _ in range(self.cols + 1)] for _ in range(self.rows + 1)
        ]
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
        '''
        Add new piece to the board
        Help set up the board
        '''
        chessTypes = {
            "chariot": Chariot,
            "horse": Horse,
            "elephant": Elephant,
            "soldier": Soldier,
            "lord": Lord,
        }

        centrePoint = self.getCoordinateFromPosition(position)
        newPiece = chessTypes.get(type)(centrePoint=centrePoint, position=position, side=side)
        self.activePices.append(newPiece)

        if isinstance(newPiece, Lord):
            if newPiece.side == RED_SIDE:
                self.redLord = newPiece
            else:
                self.blueLord = newPiece
        
        row, col = position
        self.grid[row][col] = newPiece
    
    def makeGrid(self):
        '''
        Set up all the pieces and their positions in the board at the beginning of the game
        '''
        side = [RED_SIDE, BLUE_SIDE]
        pieces = ["chariot", "horse", "elephant", "soldier", "lord"]
        getPos = {
            RED_SIDE: [(9, 0) , (9, 1), (9, 2), [6, 0], [9, 4]],
            BLUE_SIDE: [(0, 8) , (0, 7), (0, 6), [3, 0], [0, 4]],
        }

        for side in side:
            positions = getPos.get(side)
            for piece, pos in zip(pieces, positions):
                self.addNewPiece(piece, pos, side)

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
        The board should be center horizontally and occupied 75% bottom half of the window
        """

        self.x = (WIN_WIDTH - self.width) / 2
        self.y = WIN_HEIGHT * 5 / 100

    def getCoordinateFromPosition(self, position=None):
        """
        Get the centre coordinate of a chess piece by giving its row and column
        """
        if not position:
            return None

        row, col = position

        x = self.x + self.gap * col
        y = self.y + self.gap * row
        return (x, y)

    def getPositionFromCoordinate(self, coordinate):
        '''
        Get row and column from given game's coordinate
        '''
        x, y = coordinate
        col = round((x - self.x) / self.gap)
        row = round((y - self.y) / self.gap)

        return (row, col) 

    def getPiece(self, position):
        '''
        Get piece from given location
        '''
        row, col = position
        return self.grid[row][col]
    
    def getLord(self, side):
        '''
        Return the lord piece depends on the given side
        '''
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
        '''
        Deselect a piece
        '''
        piece = self.getPiece(piecePos)
        piece.deselect()
        self.movables = []

        return None

    def movePiece(self, piece, newPos=(0, 0)):
        """
        Moving the piece and update the board
        """

        # print(f"Moving {piece} to {newPos}")

        oldRow, oldCol = piece.position
        newRow, newCol = newPos

        self.deselectPiece(piece.position)

        if self.grid[newRow][newCol]:
            self.activePices.remove(self.grid[newRow][newCol])

        self.grid[oldRow][oldCol] = None
        self.grid[newRow][newCol] = piece

        newCentrePoint = self.getCoordinateFromPosition(newPos)
        piece.moveToNewSpot(centrePoint=newCentrePoint, position=newPos)

        # Swich turn
        self.turn = RED_SIDE if self.turn == BLUE_SIDE else BLUE_SIDE
        
     