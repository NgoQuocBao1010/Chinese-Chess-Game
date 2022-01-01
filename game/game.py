import pygame
from copy import deepcopy
from pprint import pprint

from .utils import RED_TURN, BLUE_TURN
from .board import BoardGame
from .pieces import Chariot, Horse, Elephant, Lord, Soldier


class Game:
    def __init__(self, win):
        self.win = win
        self._init()

    def updateGame(self):
        self.board.drawGrid(self.win)

    def _init(self):
        """
        Initilize new board
        """
        self.board = BoardGame()
        self.tempBoard = self.board
        self.gameover = False
        self.turn = RED_TURN
        self.selectedPiece = None
        self.enemyPieces = []

    @property
    def isOver(self):
        return self.gameover

    def resetGame(self):
        """
        Reset the game
        """
        self._init()

    def undo(self):
        """
        Undo a move
        """

        if not self.isOver:
            self.board = self.tempBoard
            self.turn = self.board.turn

    def switchTurn(self):
        """
        Switching side
        """
        self.turn = RED_TURN if self.turn == BLUE_TURN else BLUE_TURN
        self.enemyPieces = [
            piece for piece in self.board.activePices if piece.side != self.turn
        ]

    def checkForMove(self, clickedPos):
        """
        Check for click event to move pieces around in the game
        """
        # Check if any position in the board is clicked
        if self.board.isClicked(clickedPos):
            postion = self.board.getPositionFromCoordinate(clickedPos)
            piece = self.board.getPiece(postion)

            if not self.selectedPiece:
                if piece is not None and piece.side == self.board.turn:
                    self.selectedPiece = piece
                    self.selectedPiece.makeSelected()
                    self.board.movables = self.selectedPiece.possibleMoves

            else:
                if piece == self.selectedPiece:
                    self.board.deselectPiece(postion)
                    self.selectedPiece = None
                # if another position is clicked
                else:
                    # if piece can move to that position
                    moved = self.move(postion)

                    if not moved:
                        self.board.deselectPiece(self.selectedPiece.getPosition())
                        self.selectedPiece = None
                        self.checkForMove(clickedPos)

        else:  # If other the board is not clicked, diselect any selected piece
            if self.selectedPiece is not None:
                self.board.deselectPiece(self.selectedPiece.getPosition())
                self.selectedPiece = None

    def move(self, postion):
        """
        Moving the piece
        """
        if postion in self.board.movables:
            self.tempBoard = deepcopy(self.board)
            self.board.movePiece(self.selectedPiece, postion)
            self.selectedPiece = None
            self.switchTurn()
            self.checkForMated()

            if self.calculateNextMoves() == 0:
                self.gameover = True

            return True
        else:
            print(f"Cant move there {postion}")
            return False

    def checkForMated(self):
        """
        Check if the lord is under attack
        """
        lordPiece = self.board.getLord(self.turn)
        enemyMoves = []
        for p in self.enemyPieces:
            enemyMoves += p.checkPossibleMove(self.board.grid)

        lordPiece.mated = True if tuple(lordPiece.position) in enemyMoves else False

    def calculateNextMoves(self):
        """
        Calcalate the next moves for every piece
        """
        piecesInTurn = [
            piece for piece in self.board.activePices if piece.side == self.turn
        ]  # get all pieces that in the turn to move

        nextMoves = 0

        totalPiecesCheck = 0

        for piece in piecesInTurn:
            moves = piece.checkPossibleMove(self.board.grid)
            validMoves = []

            for move in moves:
                tempBoard = deepcopy(self.board)
                tempPiece = tempBoard.getPiece(piece.getPosition())

                tempBoard.movePiece(tempPiece, move)
                lordPiece = tempBoard.getLord(self.turn)

                enemyMoves = []
                for p in tempBoard.activePices:
                    if p.getSide() != self.turn and p.attackingPiece:
                        enemyMoves += p.checkPossibleMove(tempBoard.grid)
                        totalPiecesCheck += 1

                if tuple(lordPiece.position) in enemyMoves or tempBoard.lordTolord():
                    continue

                validMoves.append(move)

            nextMoves += len(validMoves)
            piece.possibleMoves = validMoves

        return nextMoves
