import pygame

from .utils import ChessImages, Color, Font, RED_SIDE, BLUE_SIDE, WIN_HEIGHT, WIN_WIDTH


class ControlPanel:
    MARGIN_RIGHT = 50

    def __init__(self, game):
        self.width = 250
        self.height = 600

        self.x = WIN_WIDTH - self.width - self.MARGIN_RIGHT
        self.y = 50

        self.game = game

        self.buttons = []

        self.makeIndicators()
        self.makeButton(self.x, self.y + 200, "Undo")
        self.makeButton(self.x + self.width - 100, self.y + 200, "Reset")
        self.makeButton(self.x, self.y + 300, "New Room")
        self.makeButton(self.x + self.width - 100, self.y + 300, "Join Room")

    def makeIndicators(self):
        """
        Make indicators to guide players on whose turn to play
        """
        self.blueLord = pygame.transform.scale(ChessImages.BLUE_LORD, (70, 70))
        self.redLord = pygame.transform.scale(ChessImages.RED_LORD, (70, 70))

        self.indicatorRadius = 35
        self.indicators = [
            (self.blueLord, (self.x + 35, self.y + 35)),
            (self.redLord, (self.x + self.width - 35, self.y + 35)),
        ]

    def makeButton(self, x, y, text):
        """
        Make sure every button is the same size
        W = 100
        H = 30
        """
        width = 100
        height = 30
        coordinate = (x, y)

        self.buttons.append((coordinate, width, height, text))

    def runCommand(self, buttonText):
        # if buttonText == "Undo":
        #     self.game.undo()

        # elif buttonText == "Reset":
        #     self.game.resetGame()

        FUNCTIONS = {"Undo": self.game.undo, "Reset": self.game.resetGame}

        FUNCTIONS[buttonText]()

    def checkForClick(self, clickPos):
        """
        Run command if any button is clicked
        """
        clickX, clickY = clickPos

        for coordinate, width, height, text in self.buttons:
            btnX, btnY = coordinate

            if clickX < btnX or clickX > btnX + width:
                continue

            if clickY < btnY or clickY > btnY + height:
                continue

            self.runCommand(text)

    def draw(self, win):
        """
        Draw the control panel
        """
        for indicator, centrePoint in self.indicators:
            pygame.draw.circle(win, Color.WHITE, centrePoint, self.indicatorRadius)
            win.blit(
                indicator,
                (
                    centrePoint[0] - self.indicatorRadius,
                    centrePoint[1] - self.indicatorRadius,
                ),
            )

        for coordinate, width, height, text in self.buttons:
            text = Font.WRITING_FONT.render(text, True, Color.BLACK)
            textWidth, textHeight = text.get_size()
            pygame.draw.rect(
                win,
                Color.WHITE,
                pygame.Rect(*coordinate, width, height),
            )
            textX = coordinate[0] + (width - textWidth) // 2
            textY = coordinate[1] + (height - textHeight) // 2

            win.blit(text, (textX, textY))

        if self.game.isOver:
            winnerTeam = "Blue" if self.game.turn == RED_SIDE else "Red"
            text = Font.NORMAL_FONT.render(f"{winnerTeam} won", True, Color.GREEN)
            textWidth, textHeight = text.get_size()

            textX = self.x + (self.width - textWidth) // 2
            textY = 150

            win.blit(text, (textX, textY))
