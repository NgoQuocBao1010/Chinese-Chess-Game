import pygame
import numpy as np
from pprint import pprint

from .pieces import Chariot, Horse, Elephant, Lord

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

        if self.grid[newRow][newCol]:
            self.activePices.remove(self.grid[newRow, newCol])

        self.grid[oldRow][oldCol] = None
        self.grid[newRow][newCol] = piece

        newCentrePoint = self.getCoordinateFromPosition(newPos)
        piece.moveToNewSpot(centrePoint=newCentrePoint, position=newPos)

        # Swich turn
        self.turn = RED_SIDE if self.turn == BLUE_SIDE else BLUE_SIDE
        
    def checkForChessMate(self):
        '''
        Checking the board after every moves
        '''
        totalMoves = 0
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
                    print(piece)
                    checkMateMoves.setdefault(piece, moves)
        
        # If there is a check then solve it
        if len(checkMateMoves) > 0:
            lordPiece.mated = True

            for piece, posMoves in checkMateMoves.items():
                totalMoves += self.solveCheck(piece, posMoves, lordPiece, enemyMoves)
        

        else:  # else check the other side moves
            for piece in self.activePices:
                if not piece.isEnemy(lordPiece):
                    if piece == lordPiece:
                        totalMoves += len(piece.checkPossibleMove(self.grid, avoidMoves=enemyMoves))
                    else:
                        totalMoves += len(piece.checkPossibleMove(self.grid))
        
        return totalMoves

    def solveCheck(self, piece, posMoves, lordPiece, enemyMoves):
        '''
        Find possible move if the lord is checked

        Parameters:
        piece: the piece that currently checking
        posMoves: all the moves the the cheking piece could go
        lordPiece: the checked piece
        '''
        totalMoves = 0
        lordPos = tuple(lordPiece.position)
        piecePos = tuple(piece.position)

        ourPieces = [piece for piece in self.activePices if not piece.isEnemy(lordPiece)]

        solveMoves = [piecePos, ]  # Capture the checking piece
        avoidMoves = [*enemyMoves]  # Moves lord need to avoid
        blockingMoves = []  # Moves that can block the attack

        # Block the checking piece
        if isinstance(piece, Chariot):
            print("Charior is checking")
            # Check if the chariot in the same row as the lord
            if piecePos[0] == lordPos[0]:
                if piecePos[1] < lordPos[1]:
                    blockingMoves = [ pos for pos in posMoves if pos[0] == lordPos[0] and pos != lordPos and piecePos[1] < pos[1] < lordPos[1] ]
                else:
                    blockingMoves = [ pos for pos in posMoves if pos[0] == lordPos[0] and pos != lordPos and lordPos[1] < pos[1] < piecePos[1] ]

                # Check if the lord can capture that chariot, if not, move away from the row
                if (lordPos[0], lordPos[1] + 1) != piecePos:
                    avoidMoves.append((lordPos[0], lordPos[1] + 1))
                if (lordPos[0], lordPos[1] - 1) != piecePos:
                    avoidMoves.append((lordPos[0], lordPos[1] - 1))

            # Did the same for column
            elif piecePos[1] == lordPos[1]:
                if piecePos[0] < lordPos[0]:
                    blockingMoves = [ pos for pos in posMoves if pos[1] == lordPos[1] and pos != lordPos and piecePos[0] < pos[0] < lordPos[0] ]
                else:
                    blockingMoves = [ pos for pos in posMoves if pos[1] == lordPos[1] and pos != lordPos and lordPos[0] < pos[0] < piecePos[0] ]

                if (lordPos[0] + 1, lordPos[1]) != piecePos:
                    avoidMoves.append((lordPos[0] + 1, lordPos[1]))
                if (lordPos[0] - 1, lordPos[1]) != piecePos:
                    avoidMoves.append((lordPos[0] - 1, lordPos[1]))
            
        elif isinstance(piece, Horse):
            print("Horse is checking")
            # Checking for which directions that the horse is attacking from
            if piecePos[0] - 2 == lordPos[0]:  # attack from below
                blockingMoves.append((piecePos[0] - 1, piecePos[1]))
            elif piecePos[0] + 2 == lordPos[0]:  # attack from above
                blockingMoves.append((piecePos[0] + 1, piecePos[1]))
            elif piecePos[1] - 2 == lordPos[1]:  # attack from the right
                blockingMoves.append((piecePos[0], piecePos[1] - 1))
            elif piecePos[1] + 2 == lordPos[1]:  # attack from the left
                blockingMoves.append((piecePos[0], piecePos[1] + 1))
        
        solveMoves += blockingMoves

        for piece in ourPieces:
            if piece == lordPiece:
                totalMoves += len(piece.checkPossibleMove(self.grid, avoidMoves=avoidMoves))
            else:
                totalMoves += len(piece.checkPossibleMove(self.grid, forceMoves=solveMoves))
                
        return totalMoves
    
    def test(self):
        for piece in self.activePices:
            piece.checkPossibleMove(self.grid)
        