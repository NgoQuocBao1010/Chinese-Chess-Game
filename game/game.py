import pygame
from copy import deepcopy
from pprint import pprint

from .utils import RED_TURN, BLUE_TURN
from .board import BoardGame
from .pieces import Chariot, Horse, Elephant, Lord


class Game:
    def __init__(self, win):
        self.win = win
        self.board = BoardGame()
        self.turn = RED_TURN
        self.selectedPiece = None
        self.nextMoves = []
    
    def updateGame(self):
        self.board.drawGrid(self.win)
    
    def switchTurn(self):
        '''
        Switching side
        '''
        self.turn = RED_TURN if self.turn == BLUE_TURN else BLUE_TURN
    
    def checkForMove(self, clickedPos):
        clickX, clickY = clickedPos
        
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
                    self.move(postion)

        else:  # If other the board is not clicked, diselect any selected piece
            if self.selectedPiece is not None:
                self.board.deselectPiece(self.selectedPiece.getPosition())
                self.selectedPiece = None
    

    def move(self, postion):
        if postion in self.board.movables:
            self.board.movePiece(self.selectedPiece, postion)
            self.board.deselectPiece(self.selectedPiece.getPosition())
            self.selectedPiece = None
            self.board.test()
            self.switchTurn()
            print(self.calculateNextMoves())
        else: 
            print(f"Cant move there {postion}")
    
    def calculateNextMoves(self):
        '''
        Calcalate the next moves for every piece
        '''
        piecesInTurn = [ piece for piece in self.board.activePices if piece.side == self.turn ]  # get all pieces that in the turn to move
        
        allMoves = {}

        for piece in piecesInTurn:
            moves = piece.checkPossibleMove(self.board.grid)
            allMoves.setdefault(piece, moves)
        
        tempBoard = deepcopy(self.board)

        pprint(tempBoard)
        return
