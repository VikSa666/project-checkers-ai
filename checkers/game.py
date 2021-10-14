import pygame
from .constants import BLACK, WHITE, ROWS, COLS, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.board = Board()

    def _init(self):
        self.selected = None  # Pieza seleccionada
        self.board = Board()  # Usaremos aquí el board, y en el main sólo llamaremos al game
        self.turn = WHITE
        self.legalMoves = {}  # Diccionario de los movimientos legales

    def update(self):
        """
        Función update, que dibujará el tablero. Entonces se supone que cada vez que la llamemos
        será porque hemos cambiado el tablero y queremos dibujar el nuevo.

        También dibujará los movimientos legales, para que se vean las bolitas azules.
        """
        self.board.draw(self.win)
        self.drawLegalMoves(self.legalMoves)
        pygame.display.update()

    def reset(self):
        """
        El método reset es para resetear el juego.

        Así que definimos el método privado _init para inicializr el juego, pero no queremos que
        se inicialize cada vez que queremos resetear.
        """
        self._init()

    def select(self, row, col):
        """
        Si selected es True significa que tenemos ya algo seleccionado (es
        decir, una ficha)

        Entonces seleccionamos la casilla a la que queremos ir y la función
        ya se encarga de mover la ficha ahí (lo intenta). Si no tiene sentido
        devolverá un False o algo así, y entonces reseleccionamos.

        Si el resultado del movimiento no es bueno, entonces volvemos a poner
        como si no hubiese nada seleccionado y llamamos de nuevo a la función
        select para seleccionar de cero.

        Es decir: si hemos seleccionado una ficha y luego una casilla para mover
        la ficha a la que en realidad no puede moverse, entonces la función ._move
        tendrá que devolver un False, y así pues se reestablecerán los parámetros:
        se deseleccionará la ficha y se volverá a llamar a la misma función.

        Si no hay ficha seleccionada, significa que lo que toca es seleccionar ficha.
        Entonces si lo que se seleccione no es una pieza del color que toca
        la función devolverá un False y en este caso se tendrá que volver
        a seleccionar.
        """
        if self.selected:  # If we already selected something...
            result = self._move(row, col)  # ...it is because we want to move to there
            if not result:
                self.selected = None
                self.select(row, col)
        # Si no hay ninguna pieza seleccionada, pues la vamos a selecionar
        piece = self.board.getPiece(row, col)
        if piece != 0 and piece.color == self.turn:  # Esto significa que si seleccionamos una casilla en la que no hay pieza no entrará
            self.selected = piece
            self.legalMoves = self.board.getLegalMoves(piece)
            return True
        return False

    def winner(self):
        return self.board.winner()

    def _move(self, row, col):  # La barra baja es para indicar que es una función privada
        """
        No vamos a hacer nada maás
        que mover si seleccionamos una casilla, después de haber seleccionado una ficha

        Si selected es true, significa que hemos seleccionado algo (una ficha por ejemplo)
        Si piece == 0 significa que la segunda selección es una casilla en la que
        no hay piezas. Y si (row, col) están dentro de los movimientos permitidos:


        """
        piece = self.board.getPiece(row, col)
        if self.selected and piece == 0 and (row, col) in self.legalMoves:
            self.board.move(self.selected, row, col)
            skipped = self.legalMoves[(row, col)]
            if skipped:  # Tenemos que borrar la pieza que hayamos saltado y restarle uno al número de piezas
                self.board.remove(skipped)
            self.changeTurn()
        else:
            return False

        return True

    def changeTurn(self):
        if self.turn == BLACK:
            self.legalMoves = []
            self.turn = WHITE
        else:
            self.legalMoves = []
            self.turn = BLACK

    def drawLegalMoves(self, moves):
        """
        Intentaré que cuando se seleccione una pieza, aparezca un circulito
        azul en aquellos lugares en los que se pueda mover la pieza
        """
        for move in moves:  # Loop sobre las claves del diccionario
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    # A partir de aquí son métodos para implementar la ia
    def aiMove(self, board):
        self.board = board  # Actualizar el tablero
        self.changeTurn()  # Cambiar turnos

    def getBoard(self):
        return self.board


