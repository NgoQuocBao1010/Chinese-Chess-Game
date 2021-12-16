import pygame
import numpy as np

from .utils import Color, ChessImages, RED_SIDE, BLUE_SIDE


class ChessPiece:
    NOT_SELECTED = 0
    SELECTED = 1

    NAME = "A chess piece"

    def __init__(self, centrePoint=(0, 0), position=(0, 0), side=RED_SIDE):
        self.position = position
        self.centrePoint = centrePoint
        self.radius = 20

        self.attackingPiece = False
        self.side = side
        self.status = self.NOT_SELECTED
        self.possibleMoves = []
        self.image = None

    def _getImage(self):
        """
        Get image of piece depends on its side and type
        """
        if isinstance(self, Horse):
            return (
                ChessImages.RED_HORSE
                if self.getSide() == RED_SIDE
                else ChessImages.BLUE_HORSE
            )

        if isinstance(self, Soldier):
            return (
                ChessImages.RED_SOLDIER
                if self.getSide() == RED_SIDE
                else ChessImages.BLUE_SOLDIER
            )

        if isinstance(self, Elephant):
            return (
                ChessImages.RED_ELEPHANT
                if self.getSide() == RED_SIDE
                else ChessImages.BLUE_ELEPHANT
            )

        if isinstance(self, Chariot):
            return (
                ChessImages.RED_CHARIOT
                if self.getSide() == RED_SIDE
                else ChessImages.BLUE_CHARIOT
            )

        if isinstance(self, Cannon):
            return (
                ChessImages.RED_CANNON
                if self.getSide() == RED_SIDE
                else ChessImages.BLUE_CANNON
            )

        if isinstance(self, Advisor):
            return (
                ChessImages.RED_ADVISOR
                if self.getSide() == RED_SIDE
                else ChessImages.BLUE_ADVISOR
            )

        if isinstance(self, Lord):
            return (
                ChessImages.RED_LORD
                if self.getSide() == RED_SIDE
                else ChessImages.BLUE_LORD
            )

    def draw(self, win):
        """
        Draw the piece
        """
        pygame.draw.circle(win, Color.WHITE, self.centrePoint, self.radius)
        x, y = self.centrePoint
        if self.status == self.SELECTED:
            pygame.draw.rect(
                win,
                Color.GREEN,
                pygame.Rect(
                    x - self.radius - 1,
                    y - self.radius - 1,
                    self.radius * 2 + 2,
                    self.radius * 2 + 2,
                ),
                2,
            )

        image = self._getImage()
        win.blit(image, (x - self.radius, y - self.radius))

    def isClicked(self, pos=None):
        """
        Check if the piece is clicked
        """
        if not pos:
            return None

        clickX, clickY = pos
        centerX, centerY = self.centrePoint

        if (clickX - centerX) ** 2 + (clickY - centerY) ** 2 < self.radius ** 2:
            return True
        return False

    def getPosition(self):
        return self.position

    def makeSelected(self):
        """
        Make the piece seleceted
        """
        self.status = self.SELECTED

    def deselect(self):
        """
        Deleselect the piece
        """
        self.status = self.NOT_SELECTED

    def checkPossibleMove(self, boardGrid):
        """
        Checking all possible moves of the piece
        """
        print("This is not a real chesspiece")

    def checkForAttackAbility(self):
        """
        Depends on the piece's position, determine whether they are a threat to the other lord or not
        """
        return None

    def moveToNewSpot(self, centrePoint=None, position=None):
        """
        Change the piece attribute according to the new spot
        """
        if not centrePoint:
            return

        self.centrePoint = centrePoint
        self.position = position

        self.checkForAttackAbility()

    def getSide(self):
        return self.side

    def isEnemy(self, other):
        return True if other.getSide() != self.getSide() else False

    def __str__(self):
        return f"A {self.NAME} at {self.position}"

    def __repr__(self):
        return f"Object {self.NAME}-{self.side}"

    def __eq__(self, other):
        if not isinstance(other, ChessPiece):
            return False
        return self.centrePoint == other.centrePoint

    def __hash__(self):
        return hash(self.centrePoint)


class Chariot(ChessPiece):
    """
    Chariot chess piece
    """

    NAME = "Chariot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attackingPiece = True

    def checkPossibleMove(self, boardGrid, update=True):
        boardGrid = np.array(boardGrid)
        movables = []

        rowPos, colPos = self.position

        column = boardGrid[:, colPos]  # get the whole colummn
        # Move up
        for r in range(
            rowPos - 1, -1, -1
        ):  # get all the row above current row, except current row
            if not column[r]:
                movables.append((r, colPos))
            else:
                otherPiece = column[r]
                if self.isEnemy(otherPiece):
                    movables.append((r, colPos))
                break

        # Move down
        for r in range(rowPos + 1, 10):
            if not column[r]:
                movables.append((r, colPos))
            else:
                otherPiece = column[r]
                if self.isEnemy(otherPiece):
                    movables.append((r, colPos))
                break

        row = boardGrid[rowPos]  # get the whole row
        # Move left
        for c in range(colPos - 1, -1, -1):
            if not row[c]:
                movables.append((rowPos, c))
            else:
                otherPiece = row[c]
                if self.isEnemy(otherPiece):
                    movables.append((rowPos, c))
                break

        # Move right
        for c in range(colPos + 1, 9):
            if not row[c]:
                movables.append((rowPos, c))
            else:
                otherPiece = row[c]
                if self.isEnemy(otherPiece):
                    movables.append((rowPos, c))
                break

        if update:
            self.possibleMoves = movables

        return movables


class Cannon(ChessPiece):
    """
    Cannon chess piece
    """

    NAME = "Cannon"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attackingPiece = True

    def checkPossibleMove(self, boardGrid, update=True):
        boardGrid = np.array(boardGrid)
        movables = []

        rowPos, colPos = self.position

        column = boardGrid[:, colPos]  # get the whole colummn
        skip = False
        # Move up
        for r in range(
            rowPos - 1, -1, -1
        ):  # get all the row above current row, except current row
            if not skip:
                if column[r] is None:
                    movables.append((r, colPos))
                else:
                    skip = True
            else:
                otherPiece = column[r]
                if otherPiece is not None:
                    if self.isEnemy(otherPiece):
                        movables.append((r, colPos))
                    break

        # Move down
        skip = False
        for r in range(rowPos + 1, 10):
            if not skip:
                if column[r] is None:
                    movables.append((r, colPos))
                else:
                    skip = True
            else:
                otherPiece = column[r]
                if otherPiece is not None:
                    if self.isEnemy(otherPiece):
                        movables.append((r, colPos))
                    break

        row = boardGrid[rowPos]  # get the whole row
        # Move left
        skip = False
        for c in range(colPos - 1, -1, -1):
            if not skip:
                if row[c] is None:
                    movables.append((rowPos, c))
                else:
                    skip = True
            else:
                otherPiece = row[c]
                if otherPiece is not None:
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos, c))
                    break

        # Move right
        skip = False
        for c in range(colPos + 1, 9):
            if not skip:
                if row[c] is None:
                    movables.append((rowPos, c))
                else:
                    skip = True
            else:
                otherPiece = row[c]
                if otherPiece is not None:
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos, c))
                    break

        if update:
            self.possibleMoves = movables

        return movables


class Horse(ChessPiece):
    """
    Horse Chess Piece
    """

    NAME = "Horse"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def checkPossibleMove(self, boardGrid, update=True):
        boardGrid = np.array(boardGrid)
        movables = []

        rowPos, colPos = self.position

        # All possibles move of a Knight
        moveX = []
        moveY = []

        # Move up
        stepX = [-2, -2]
        stepY = [-1, 1]
        if 0 <= rowPos - 1 and not boardGrid[rowPos - 1, colPos]:
            moveX += stepX
            moveY += stepY

        # Move down
        stepX = [2, 2]
        stepY = [-1, 1]
        if rowPos + 1 <= 9 and not boardGrid[rowPos + 1, colPos]:
            moveX += stepX
            moveY += stepY

        # Move left
        stepX = [1, -1]
        stepY = [-2, -2]
        if 0 <= colPos - 1 and not boardGrid[rowPos, colPos - 1]:
            moveX += stepX
            moveY += stepY

        # Move right
        stepX = [1, -1]
        stepY = [2, 2]
        if colPos + 1 <= 8 and not boardGrid[rowPos, colPos + 1]:
            moveX += stepX
            moveY += stepY

        for mX, mY in zip(moveX, moveY):
            newRow = rowPos + mX
            newCol = colPos + mY

            # Check if the move is valid
            if 0 <= newRow <= 9 and 0 <= newCol <= 8:
                if not boardGrid[newRow, newCol]:
                    movables.append((newRow, newCol))
                else:
                    otherPiece = boardGrid[newRow, newCol]
                    if self.isEnemy(otherPiece):
                        movables.append((newRow, newCol))

        if update:
            self.possibleMoves = movables

        return movables

    def checkForAttackAbility(self):
        if self.side == BLUE_SIDE and self.position[0] > 4:
            self.attackingPiece = True

        if self.side == RED_SIDE and self.position[0] < 5:
            self.attackingPiece = True


class Elephant(ChessPiece):
    """
    Horse Chess Piece
    """

    NAME = "Elephant"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moveLimit = (0, 4) if 0 <= self.position[0] <= 4 else (5, 9)

    def checkPossibleMove(self, boardGrid, update=True):
        boardGrid = np.array(boardGrid)
        movables = []

        rowPos, colPos = self.position

        upLimit, downLimt = self.moveLimit

        # Move up left
        if (
            rowPos - 1 >= upLimit
            and colPos - 1 >= 0
            and not boardGrid[rowPos - 1, colPos - 1]
        ):
            if rowPos - 2 >= upLimit and colPos - 2 >= 0:
                if not boardGrid[rowPos - 2, colPos - 2]:
                    movables.append((rowPos - 2, colPos - 2))
                else:
                    otherPiece = boardGrid[rowPos - 2, colPos - 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos - 2, colPos - 2))

        # Move up right
        if (
            rowPos - 1 >= upLimit
            and colPos + 1 <= 8
            and not boardGrid[rowPos - 1, colPos + 1]
        ):
            if rowPos - 2 >= upLimit and colPos + 2 <= 8:
                if not boardGrid[rowPos - 2, colPos + 2]:
                    movables.append((rowPos - 2, colPos + 2))
                else:
                    otherPiece = boardGrid[rowPos - 2, colPos + 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos - 2, colPos + 2))

        # Move down left
        if (
            rowPos + 1 <= downLimt
            and colPos - 1 >= 0
            and not boardGrid[rowPos + 1, colPos - 1]
        ):
            if rowPos + 2 >= upLimit and colPos - 2 >= 0:
                if not boardGrid[rowPos + 2, colPos - 2]:
                    movables.append((rowPos + 2, colPos - 2))
                else:
                    otherPiece = boardGrid[rowPos + 2, colPos - 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos + 2, colPos - 2))

        # Move down right
        if (
            rowPos + 1 <= downLimt
            and colPos + 1 <= 8
            and not boardGrid[rowPos + 1, colPos + 1]
        ):
            if rowPos + 2 >= upLimit and colPos + 2 <= 8:
                if not boardGrid[rowPos + 2, colPos + 2]:
                    movables.append((rowPos + 2, colPos + 2))
                else:
                    otherPiece = boardGrid[rowPos + 2, colPos + 2]
                    if self.isEnemy(otherPiece):
                        movables.append((rowPos + 2, colPos + 2))

        if update:
            self.possibleMoves = movables

        return movables


class Soldier(ChessPiece):
    NAME = "Soldier"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.goSideWay = False
        self.riverLine = 4 if self.position[0] < 4 else 5
        self.direction = 1 if self.position[0] < 4 else -1

    def checkPossibleMove(self, boardGrid, update=True):
        boardGrid = np.array(boardGrid)
        movables = []

        rowPos, colPos = self.position

        if self.direction == 1 and rowPos > self.riverLine:
            self.goSideWay = True

            if rowPos > self.riverLine + 1:
                self.attackingPiece = True

        if self.direction == -1 and rowPos < self.riverLine:
            self.goSideWay = True

            if rowPos < self.riverLine - 1:
                self.attackingPiece = True

        # Move up
        newRow = rowPos + self.direction
        if 0 <= newRow <= 9:
            if boardGrid[newRow, colPos] is None or self.isEnemy(
                boardGrid[newRow, colPos]
            ):
                movables.append((newRow, colPos))

        if self.goSideWay:
            directionsX = [1, -1]
            for direction in directionsX:
                newCol = colPos + direction
                if 0 <= newCol <= 8:
                    if boardGrid[rowPos, newCol] is None or self.isEnemy(
                        boardGrid[rowPos, newCol]
                    ):
                        movables.append((rowPos, newCol))

        if update:
            self.possibleMoves = movables

        return movables


class Lord(ChessPiece):
    NAME = "Lord"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moveLimit = (0, 2) if 0 <= self.position[0] <= 2 else (7, 9)
        self.mated = False

        # Animation when lord is under attack
        self.grow = True
        self.thickness = 4
        self.skip = True

    def draw(self, win):
        super().draw(win)
        if self.mated:
            if self.grow:
                self.thickness += 1
            else:
                self.thickness -= 1

            if self.thickness == 6:
                self.grow = False
            if self.thickness <= 4:
                self.grow = True

            pygame.draw.circle(
                win,
                Color.RED,
                self.centrePoint,
                self.radius + self.thickness,
                self.thickness,
            )

    def checkPossibleMove(self, boardGrid, update=True):
        boardGrid = np.array(boardGrid)
        movables = []

        rowPos, colPos = self.position

        upLimit, downLimt = self.moveLimit
        leftLimit, rightLimit = (3, 5)

        movesX = [0, 0, 1, -1]
        movesY = [-1, 1, 0, 0]

        for mX, mY in zip(movesX, movesY):
            newRow = rowPos + mX
            newCol = colPos + mY

            # Check if the move is valid
            if upLimit <= newRow <= downLimt and leftLimit <= newCol <= rightLimit:
                if not boardGrid[newRow, newCol]:
                    movables.append((newRow, newCol))
                else:
                    otherPiece = boardGrid[newRow, newCol]
                    if self.isEnemy(otherPiece):
                        movables.append((newRow, newCol))

        if update:
            self.possibleMoves = movables

        return movables


class Advisor(ChessPiece):
    NAME = "Advisor"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moveLimit = (0, 2) if 0 <= self.position[0] <= 2 else (7, 9)

    def checkPossibleMove(self, boardGrid, update=True):
        boardGrid = np.array(boardGrid)
        movables = []

        rowPos, colPos = self.position

        upLimit, downLimt = self.moveLimit
        leftLimit, rightLimit = (3, 5)

        movesX = [1, 1, -1, -1]
        movesY = [-1, 1, 1, -1]

        for mX, mY in zip(movesX, movesY):
            newRow = rowPos + mX
            newCol = colPos + mY

            # Check if the move is valid
            if upLimit <= newRow <= downLimt and leftLimit <= newCol <= rightLimit:
                if not boardGrid[newRow, newCol]:
                    movables.append((newRow, newCol))
                else:
                    otherPiece = boardGrid[newRow, newCol]
                    if self.isEnemy(otherPiece):
                        movables.append((newRow, newCol))

        if update:
            self.possibleMoves = movables

        return movables
