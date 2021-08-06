import pygame
from utils import Color

class ChessPiece():
    STATUS_COLOR = {
        0: Color.GREEN,
        1: Color.RED,
    }

    def __init__(self, centrePoint=(0, 0)):
        self.centrePoint = centrePoint
        self.radius = 25

        self.status = 0
        self.posibleMoves = []
    
    def draw(self, win):
        color = self.STATUS_COLOR.get(self.status)
        pygame.draw.circle(win, color, self.centrePoint, self.radius)
    
    def isClicked(self, pos=None):
        if not pos: return None

        clickX, clickY = pos
        centerX, centerY = self.centrePoint

        if (clickX - centerX) ** 2 + (clickY - centerY) ** 2 < self.radius ** 2:
            print(f"I am clicked {self.centrePoint}")
            return True
        return False

    def changeStatus(self, pos):
        if not self.isClicked(pos): return False
        self.status = 0 if self.status != 0 else 1

        if self.status == 1:
            pass

        return True


