from .constants import WHITE, BLACK, SQUARE_SIZE, BROWN, GRAY, CROWN
import pygame


class Piece:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False  # Utilizaré este booleano para determinar si una pieza es reina o no

        # Pensando en el sistema de coordenadas de pygame: si estamos arriba de to do a la derecha estamos en el (0,0)
        # Entonces si nos movemos de arriba a abajo, nos movemos en dirección positiva, en cambio de abajo a arriba es negativo

        if self.color == BLACK:
            self.direction = -1
        else:
            self.direction = 1

        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def calculatePosition(self):
        """
        Justo en el medio del cuadrado está la posición (x,y) de la pieza: el centro del círculo
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def becomeQueen(self):
        """
        Simplemente poner en True el atributo queen, si es reina
        """
        self.queen = True

    def drawPiece(self, win):
        """
        Lo que voy a hacer es dibujar las piezas de la siguiente manera:
            Definiré un radio que será en función del SQUARE_SIZE para que quepa dentro de cada cuadradito
            Usaré pygame.draw.circle(dónde, color, coordenadas (x,y), radio (en px))
            Dibujaré primero un círculo de 2px más de radio, de color negro y encima pondré el de color blanco
            De esta manera quedará como si fuese un contorno
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GRAY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        pygame.draw.circle(win, GRAY, (self.x, self.y), radius - 8)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius - 10)
        if self.queen:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))  # pygame method

    def move(self, row, col):
        """
        Mover piezas
        """
        self.row = row
        self.col = col
        self.calculatePosition()  # Tenemos que recalcular

    def __repr__(self):  # Representación interna de este objeto. Esto no lo acabo de entender
        return str(self.color)
