import pygame
import numpy as np
from pprint import pprint

from utils import Configuration, Color
from chesspiece import Chariot, Horse, Elephant, Lord

RED_SIDE = Configuration.RED_SIDE
BLUE_SIDE = Configuration.BLUE_SIDE

class BoardGame:
    def __init__(self, win):
        self.win = win
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
        self.grid = np.array(self.grid)
        # contains all active pieces all the board
        self.activePices = []
        # contains all movable positions
        self.movables = []
        # info of which side's turn
        self.turn = RED_SIDE
        # Varible contain to LORD pieces of either side
        self.blueLord = None
        self.redLord = None

        self.generatePosition()
        self.makeGrid()


    def addNewPiece(self, type, position, side):
        chessTypes = {
            "chariot": Chariot,
            "horse": Horse,
            "elephant": Elephant,
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
        self.grid[row, col] = newPiece
    
    def makeGrid(self):
        '''
        Set up the board at the beginning of the game
        '''
        side = [RED_SIDE, BLUE_SIDE]
        pieces = ["chariot", "horse", "elephant", "lord"]
        getPos = {
            RED_SIDE: [(9, 0) , (9, 1), (9, 2), [9, 4]],
            BLUE_SIDE: [(0, 8) , (0, 7), (0, 6), [0, 4]],
        }

        for side in side:
            positions = getPos.get(side)
            for piece, pos in zip(pieces, positions):
                self.addNewPiece(piece, pos, side)

        # Check all possible move for all the pieces after initialize the board
        for piece in self.activePices:
            piece.checkPossibleMove(self.grid)

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
            Color.BLACK,
            pygame.Rect(*riverCoordinate, self.width - 2, self.gap - 2),
        )

        # Draw the border
        self.rectangle = pygame.draw.rect(
            self.win,
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
            piece.draw(self.win)

        for position in self.movables:
            coor = self.getCoordinateFromPosition(position)
            pygame.draw.circle(self.win, Color.GREEN, coor, 7)

    def generatePosition(self):
        """
        Calculate the coordinate of the board
        The board should be center horizontally and occupied 75% bottom half of the window
        """

        self.x = (Configuration.WIN_WIDTH - self.width) / 2
        self.y = Configuration.WIN_HEIGHT * 5 / 100

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

        pieces = [piece for piece in self.activePices if piece.side == self.turn]
        for piece in pieces:
            if piece.isClicked(pos):
                piece.changeStatus(selected=True)
                return piece

        return None

    def movePiece(self, piece, newPos=(0, 0)):
        """
        Moving the piece and update the board
        """

        # print(f"Moving {piece} to {newPos}")

        oldRow, oldCol = piece.position
        newRow, newCol = newPos

        if self.grid[newRow, newCol]:
            self.activePices.remove(self.grid[newRow, newCol])

        self.grid[oldRow, oldCol] = None
        self.grid[newRow, newCol] = piece

        newCentrePoint = self.getCoordinateFromPosition(newPos)
        piece.moveToNewSpot(centrePoint=newCentrePoint, position=newPos)

        print("Moving done")

        # Swich turn
        self.turn = RED_SIDE if self.turn == BLUE_SIDE else BLUE_SIDE
        
    def checkForChessMate(self):
        self.redLord.mated = False
        self.blueLord.mated = False

        enemyMoves = []
        checkMateMoves = {}
        lordPiece = self.redLord if self.turn == RED_SIDE else self.blueLord

        for piece in self.activePices:
            if not piece.isEnemy(lordPiece):
                continue
            else:
                # Check move from enemy to see if the king is checked
                moves = piece.checkPossibleMove(self.grid)
                enemyMoves += moves
                if tuple(lordPiece.position) in moves:
                    checkMateMoves.setdefault(piece, moves)
        
        # If there is a check then solve it
        if len(checkMateMoves) > 0:
            lordPiece.mated = True

            for piece, posMoves in checkMateMoves.items():
                self.solveCheck(piece, posMoves, lordPiece, enemyMoves)
        else:  # else check the other side moves
            print("Checking from this side")
            for piece in self.activePices:
                if not piece.isEnemy(lordPiece):
                    if piece == lordPiece:
                        piece.checkPossibleMove(self.grid, avoidMoves=enemyMoves)
                    else:
                        piece.checkPossibleMove(self.grid)
        
        return

    def solveCheck(self, piece, posMoves, lordPiece, enemyMoves):
        '''
        Find possible move if the lord is checked
        Parameters:
        piece: the piece that currently checking
        posMoves: all the moves the the cheking piece could go
        lordPiece: the checked piece
        '''
        lordPos = tuple(lordPiece.position)
        piecePos = tuple(piece.position)

        ourPieces = [piece for piece in self.activePices if not piece.isEnemy(lordPiece)]

        solveMoves = [piecePos, ]  # Capture the checking piece
        avoidMoves = [*enemyMoves]  # The lord to run

        # Block the checking piece
        if isinstance(piece, Chariot):
            if piecePos[0] == lordPos[0]:
                if piecePos[1] < lordPos[1]:
                    blockingMoves = [ pos for pos in posMoves if pos[0] == lordPos[0] and pos != lordPos and piecePos[1] < pos[1] < lordPos[1] ]
                else:
                    blockingMoves = [ pos for pos in posMoves if pos[0] == lordPos[0] and pos != lordPos and lordPos[1] < pos[1] < piecePos[1] ]

                avoidMoves.append((lordPos[0], lordPos[1] + 1))
                avoidMoves.append((lordPos[0], lordPos[1] - 1))

            elif piecePos[1] == lordPos[1]:
                if piecePos[0] < lordPos[0]:
                    blockingMoves = [ pos for pos in posMoves if pos[1] == lordPos[1] and pos != lordPos and piecePos[0] < pos[0] < lordPos[0] ]
                else:
                    blockingMoves = [ pos for pos in posMoves if pos[1] == lordPos[1] and pos != lordPos and lordPos[0] < pos[0] < piecePos[0] ]
                avoidMoves.append((lordPos[0] + 1, lordPos[1]))
                avoidMoves.append((lordPos[0] - 1, lordPos[1]))
            
            solveMoves += blockingMoves

        for piece in ourPieces:
            if piece == lordPiece:
                piece.checkPossibleMove(self.grid, avoidMoves=avoidMoves)
            else:
                piece.checkPossibleMove(self.grid, forceMoves=solveMoves)
        



        

