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

        self.enemyPieces = []
        self.calculateNextMoves()
    
    def updateGame(self):
        self.board.drawGrid(self.win)
    
    def switchTurn(self):
        '''
        Switching side
        '''
        self.turn = RED_TURN if self.turn == BLUE_TURN else BLUE_TURN
        self.enemyPieces = [ piece for piece in self.board.activePices if piece.side != self.turn ]
    
    def checkForMove(self, clickedPos):
        clickX, clickY = clickedPos
        
        # Check if any position in the board is clicked
        if self.board.isClicked(clickedPos):
            postion = self.board.getPositionFromCoordinate(clickedPos)
            piece = self.board.getPiece(postion)
            # self.calculateNextMoves()
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
                    self.checkForMated()

        else:  # If other the board is not clicked, diselect any selected piece
            if self.selectedPiece is not None:
                self.board.deselectPiece(self.selectedPiece.getPosition())
                self.selectedPiece = None

    def move(self, postion):
        if postion in self.board.movables:
            self.board.movePiece(self.selectedPiece, postion)
            self.selectedPiece = None
            self.checkForMated()
            self.switchTurn()
            self.calculateNextMoves()
        else: 
            print(f"Cant move there {postion}")
    
    def checkForMated(self):
        lordPiece = self.board.getLord(self.turn)
        enemyMoves = []
        for p in self.enemyPieces:
            enemyMoves += p.checkPossibleMove(self.board.grid)

        lordPiece.mated = True if tuple(lordPiece.position) in enemyMoves else False
        
    
    def calculateNextMoves(self):
        '''
        Calcalate the next moves for every piece
        '''
        piecesInTurn = [ piece for piece in self.board.activePices if piece.side == self.turn ]  # get all pieces that in the turn to move
        
        allMoves = {}

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
                    if p.getSide() != self.turn:
                        enemyMoves += p.checkPossibleMove(tempBoard.grid)
                
                if tuple(lordPiece.position) in enemyMoves:
                    continue
                
                validMoves.append(move)
            
            allMoves.setdefault(piece, validMoves)
            piece.possibleMoves = validMoves
