import pygame
from .constants import BROWN, BEIGE, ROWS, SQUARE_SIZE, COLS, WHITE, BLACK
from .piece import Piece


class Board:
    def __init__(self):  # El __init__ entiendo yo que es para que se pueda utilizar en todas partes como "variables globales"
        self.board = []
        self.selected_piece = None
        self.blackPiecesLeft = self.whitePiecesLeft = 12
        self.blackQueens = self.whiteQueens = 0
        self.createBoard()

    def drawSquares(self, win):
        """
        Siguiendo los métodos que nos proporciona pygame, vamos a dibujar el tablero.

        Primero pintaré toda la ventana de color marrón y luego le haré los cuadraditos
        """
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):  # Sólo los pares o impares dependiendo del número de fila en el que estemos
                # Pygame empieza a contar desde arriba a la izquierda (0,0)
                pygame.draw.rect(win, BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        """
        Para mover una pieza lo que haremos será borrarla de su posición actual y dibujarla en la nueva posición.

        piece será la pieza que queremos mover. Está situada en (piece.row, piece.col) y queremos moverla
        a la nueva posición (row, col)
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)  # Esto borra la pieza antigua

        # Miramos si hemos llegado a una posición en la que se convierta en reina;
        if row == ROWS - 1 or row == 0:  # Si ha llegado al final...
            piece.becomeQueen()  # ...hacer reina
            if piece.color == WHITE:
                self.whiteQueens += 1
            else:
                self.blackQueens += 1
        # Ojo porque al principio ya tenemos las piezas en row 0 o 7, entonces no serán ya reinas?? No, porque tienen
        # que MOVERSE A ESA POSICIÓN, y no pueden porque no pueden volver hacia atrás. Sólo las reinas, entonces si éstas
        # volviesen serían "dobles reinas" pero eso no tiene sentido... asíq ue se quedan siendo reinas.

    def getPiece(self, row, col):
        """
        Le pasamos una fila y una columna y me devolverá la pieza situada en esa posición
        Si no hay pieza pues devuelve un 0
        """
        return self.board[row][col]

    def getAllPieces(self,color):
        """
        Esto devolverá una lista con todas las piezas del color deseado
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def createBoard(self):
        """
        Función de creación del tablero.

        El tablero es una lista de listas. Cada lista es una fila:
        [[0, pieza, 0, pieza, ...]
         [pieza, 0, pieza, 0,...
         ...
         [pieza, 0, pieza, 0...]]

        En esta función crearemos el tablero inicial, con las piezas en su posición inicial.
        Para ello implementaremos una función aritmética que utilizará % para poner las
        piezas en la posición que les corresponda.

        Donde no haya pieza pondremos un 0
        """
        for row in range(ROWS):
            self.board.append([])  # Queremos una lista para cada fila
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:  # 0, 1 y 2 son las primeras 3 filas
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)  # No hay pieza
                else:
                    self.board[row].append(0)  # No hay pieza

    def draw(self, win):
        """
        Una vez dibujados los cuadraditos del tablero, dibujamos las piezas.
        """
        self.drawSquares(win)  # primero dibujamos el tablero
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]  # Obtenemos la pieza que hay en cada casilla
                if piece != 0:  # Si hay pieza, la dibujamos. Sino, no dibujamos nada
                    piece.drawPiece(win)

    def remove(self, pieces):
        """
        Esto será para quitar todas las piezas listadas en piece
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0  # ponemos un 0 para indicar que no hay pieza
            if piece != 0:  # Si realmente había pieza que quitar, tendremos que restar uno al color correspondiente
                if piece.color == BLACK:
                    self.blackPiecesLeft -= 1
                else:
                    self.whitePiecesLeft -= 1

    def noPossibleMovesForWhite(self):
        """
        Función que devuelve un True si no hay más movimientos posibles para realizar, para el color white.
        En este caso, white perdería
        """
        listOfAllMoves = []
        whitePieces = self.getAllPieces(WHITE)
        for piece in whitePieces:
            for move in self.getLegalMoves(piece):
                listOfAllMoves.append(move)
        if not listOfAllMoves:
            return True
        return False

    def noPossibleMovesForBlack(self):
        """
        Análogo al anterior método
        """
        listOfAllMoves = []
        blackPieces = self.getAllPieces(BLACK)
        for piece in blackPieces:
            for move in self.getLegalMoves(piece):
                listOfAllMoves.append(move)
        if not listOfAllMoves:
            return True
        return False

    def winner(self):
        """
        Devuelve quién ha ganado en función de quién se ha quedado sin piezas
        """
        if self.blackPiecesLeft <= 0:
            return WHITE
        if self.whitePiecesLeft <= 0:
            return BLACK


    def getLegalMoves(self, piece):
        """
        Diccionario moves = {} con claves (x,y) que son las posiciones a las cuales
        queremos saltar. Hace referencia a una lista [piezas saltaddas] que contendrá
        las piezas que son comidas.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # Tenemos que mirar en qué dirección se mueve la pieza
        if piece.color == BLACK or piece.queen:
            # Si somos BLACK, vamos hacia arriba, así que tendremos que mirar hacia arriba si hay algo válido
            # Por tanto empezamos en la fila más baja, y miramos hacia arriba hasta row-3 (sólo queremos mirar
            # 2 líneas por arriba) o -1 (el máximo).
            moves.update(self._diagonalLeft(row-1, max(row-3,-1), -1, piece.color, left))
            moves.update(self._diagonalRight(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.queen:
            moves.update(self._diagonalLeft(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._diagonalRight(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves

    def _diagonalLeft(self, start, stop, step, color, left, skipped=[]):
        """
        If current == 0 significa que hay un hueco
        Sino, si es igual al color de nuestra pieza: no podemos movernos ahí
        Si es del equipo contrario: igual podemos movernos por encima, asumiendo que al otro hay vacío
        Miramos si se puede saltar por encima
            Si la siguiente pieza es vacío: perfecto pues podemos movernos

        Para start, stop y step:
        1.  Si left < 0 significa que hemos alcanzado el borde y ya no podemos movernos en esa dirección, así que salimos
        current es coger la pieza que hay en la casilla que queremos movernos.
        2.  Si current == 0 significa que no hay pieza ahí:
            2.1. Si skipped significa que hemos saltado alguna pieza, pero en un inicio siempre será que no
                 Si not last significa que si no hemos alcanzado la última
            2.2. Elif skipped: es que hemos saltado una pieza
                2.2.1.  Puede que saltemos dos piezas o más, que se van sumando en el diccionario
                        con la key (rg, left) que es el movimiento en cuestión
            2.3. Else:
                2.3.1.  ponemos los movimientos
            2.4. Si last: esto significa que last no está vacío --> vamos a ver si se puede saltar
                2.4.1.  Recalculamos la posición a la que vamos a intentar saltar y entonces volvemos a
                        ejecutar esta misma función:
                2.4.2.  Actualizamos de forma recursiva el movimiento, pero ahora el inicio es rg + step
                        porque ya hemos hecho un step. Lo demás se lo pasamos igual pero skipped = last
        3.  Si no: significa que hay una pieza (que puede ser nuestra o del otro color)
        4.  Si es de nuestro color
            4.1. No podemos movernos ahí: break
            4.2. Si es del color del contrincante:
                4.2.1.  last = [current] --> Potencialmente podríamos movernos por encima
                        suponiendo que en la siguiente casilla haya un hueco. Entonces last
                        se actualiza como una lista que contiene current (que es la pieza
                        que pretendemos saltar).

                        Entonces se volvería arriba del bucle y ahora moves[(rg, left)] = last
                        nos añade esto como un posible movimiento (recordamos que moves es un
                        diccionario de piezas con key = su posición). Vamos a 2.4.
        """
        moves = {}
        last = []
        for rg in range(start, stop, step):  # Row I'm starting at, stopping at and stepping by
            if left < 0:  # Alcanzado el borde
                break
            current = self.board[rg][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(rg,left)] = last + skipped
                else:
                    moves[(rg, left)] = last
                if last:
                    if step == -1:
                        row = max(rg - 3, 0)  # Como máximo intentamos movernos 2 casillas: si en la primera no se puede, la segunda alomejor sí
                    else:
                        row = min(rg + 3, ROWS)  # Como máximo intentamos movernos 2 casillas: si en la primera no se puede, la segunda alomejor sí
                    moves.update(self._diagonalLeft(rg+step, row, step, color, left-1, skipped = last))
                    moves.update(self._diagonalRight(rg + step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves

    def _diagonalRight(self, start, stop, step, color, right, skipped=[]):
        """
        análoga a la anterior
        """
        moves = {}
        last = []
        for rg in range(start, stop, step):  # Row I'm starting at, stopping at and stepping by
            if right >= COLS:  # Alcanzado el borde
                break
            current = self.board[rg][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(rg,right)] = last + skipped
                else:
                    moves[(rg, right)] = last
                if last:
                    if step == -1:
                        row = max(rg - 3, 0)  # Como máximo intentamos movernos 2 casillas: si en la primera no se puede, la segunda alomejor sí
                    else:
                        row = min(rg + 3, ROWS)  # Como máximo intentamos movernos 2 casillas: si en la primera no se puede, la segunda alomejor sí
                    moves.update(self._diagonalLeft(rg+step, row, step, color, right-1, skipped = last))
                    moves.update(self._diagonalRight(rg + step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves
