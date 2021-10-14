import pygame
from .board import Board
from .piece import Piece
from .game import Game
from copy import deepcopy
from .constants import WHITE, BLACK, ROWS, COLS


def minimaxWhite(position, depth, color, game):
    """
    Función minimax de siempre, pero sin poda alfa beta.

    En este caso, es un minimax para las blancas. Es decir, las blancas serán las que maximicen
    y las negras serán las que minimicen. Después hay otra función simétrica para las negras.

    En el caso en que se hayan explorado todas las capas deseadas o que ya haya un ganador,
    devolverá directamente la función de evaluación, junto con la posición de esa evaluación (que
    en realidad es un nuevo tablero).

    En el caso en que toque maximizar, es decir, que el color sea el blanco, maximizaremos,
    como siempre se ha hecho. En caso que le toque a las negras, se minimizará.
    """
    if depth == 0 or position.winner() is not None:
        return evaluationFunctionWhite(position), position

    if color == WHITE:
        value = float('-inf')
        bestMove = None
        for move in getAllMoves(position, WHITE, game):
            evaluation = minimaxWhite(move, depth - 1, BLACK, game)[0]
            value = max(value, evaluation)
            if value == evaluation:
                bestMove = move
        return value, bestMove

    if color == BLACK:
        value = float('inf')
        bestMove = None
        for move in getAllMoves(position, BLACK, game):
            evaluation = minimaxWhite(move, depth - 1, WHITE, game)[0]
            value = min(value, evaluation)
            if value == evaluation:
                bestMove = move
        return value, bestMove


def minimaxBlack(position, depth, color, game):
    if depth == 0 or position.winner() is not None:
        return evaluationFunctionBlack(position), position

    if color == BLACK:
        value = float('-inf')
        bestMove = None
        for move in getAllMoves(position, BLACK, game):
            evaluation = minimaxBlack(move, depth - 1, WHITE, game)[0]
            value = max(value, evaluation)
            if value == evaluation:
                bestMove = move
        return value, bestMove

    if color == WHITE:
        value = float('inf')
        bestMove = None
        for move in getAllMoves(position, WHITE, game):
            evaluation = minimaxBlack(move, depth - 1, BLACK, game)[0]
            value = min(value, evaluation)
            if value == evaluation:
                bestMove = move
        return value, bestMove


def evaluationFunctionWhite(board):
    """
    Similarmente a la práctica de pacman, realizaremos una función de evaluación.

    Para que sea más legible, en cada línea le sumamos a score lo que consideremos
    que tiene que ser sumado: piezas restantes, reinas restantes, etc. otorgándole
    el peso que consideramos idóneo.

    Al final le sumamos también lo que devuelve rowsEvaluation, que más tarde se explicará
    """
    score = 0
    score += 5*(board.whitePiecesLeft - board.blackPiecesLeft)
    score += 10 * (board.whiteQueens - board.blackQueens)
    score += rowsEvaluationWhite(board)
    return score


def evaluationFunctionBlack(board):
    """
    Análoga a evaluationFunctionWhite
    """
    score = 0
    score += 5 * (board.blackPiecesLeft - board.whitePiecesLeft)
    score += 10 * (board.blackQueens - board.whiteQueens)
    score += rowsEvaluationBlack(board)
    return score

def rowsEvaluationWhite(board):
    """
    Esta función calcula una puntuación en función de en qué filas tiene un color sus piezas: cuanto
    más avanzadas tenga las piezas, más puntuación recibirá.

    Esto lo hacemos para fomentar que así muevan todas las piezas y, en cierta medida, la ia intente
    mover todas sus piezas hacia delante, y no sólo una, como pasaba a veces.

    Sin embargo, al final también restamos el número de piezas restantes, de forma que se premie
    comer piezas con más peso que lo otro
    """
    score = 0
    rowIndex = -1  # La primera fila tendrá índice 0, así no sumarán nada las piezas que no se muevan de la primera fila
    for row in board.board:
        rowIndex += 1  # Empezamos sumando uno para que la primera tenga índice 0 y la última 7
        for piece in row:
            if piece is not 0 and piece.color is WHITE:  # Siempre y cuando se trate de una pieza del color que evaluamos...
                if not piece.queen:  # ... y no sea una reina ...
                    score += rowIndex  # ... le sumamos el índice de la fila: cuanto más avance, más alto es este valor
                if piece.queen:  # Si es una reina, como puede moverse libremente, potenciaremos que vaya hacia detrás...
                   score += 0.5*(ROWS - rowIndex)  # ... ya que las reinas se forman en el lado opuesto del tablero.
    score -= board.blackPiecesLeft  # Finalmente le restamos el total de piezas rivales, para potenciar que se las coma si puede
    return score


def rowsEvaluationBlack(board):
    """
    Simétrica a su homónima White. Aquí tenemos que pensar en la simetría de las filas. Para ser coherente
    le he asignado el mismo índice a cada fila, pero esta vez empezamos desde abajo de todo, es decir, desde
    la fila 7.
    """
    score = 0
    rowIndex = ROWS
    for row in board.board:
        rowIndex -= 1
        for piece in row:
            if piece is not 0 and piece.color is BLACK:
                if not piece.queen:
                    score += rowIndex
                else:
                   score += 0.5*(ROWS - rowIndex)
    score -= board.whitePiecesLeft
    return score


def getAllMoves(board, color, game):
    """
    Devolverá todos los posibles movimientos de TODAS las piezas de un color dado.

    Los movimientos son, en realidad, nuevos tableros en los que las piezas han sido colocadas según el
    movimiento.

    Así pues, se creará una lista que acumulará todos los posibles tableros futuros, dados los movimientos
    legales de cada pieza
    """
    moves = []
    for piece in board.getAllPieces(color):
        validMoves = board.getLegalMoves(piece)  # Diccionario
        # (row, col): [piezas saltadas]
        # Si nos movemos a (row, col), saltamos las piezas guardadas en [piezas saltadas]
        for move, skip in validMoves.items():  # Iteramos sobre las claves y sus listas asociadas...
            # ... esto es: las posibles posiciones a la que la pieza puede moverse y aquellas piezas que son comidas
            tempBoard = deepcopy(board)  # Hacemos deepcopy para no tocar el tablero original: creamos un tablero temporal
            tempPiece = tempBoard.getPiece(piece.row, piece.col)  # Creamos una pieza temporal para realizar el movimiento
            newBoard = simulateMove(tempPiece, move, tempBoard, game, skip)  # Simulamos el movimiento que genera un nuevo tablero
            moves.append(newBoard)  # Devolvemos este nuevo tablero
    return moves


def simulateMove(piece, move, board, game, skip):
    """
    Esta función simulará un movimiento, es decir, realizará un movimiento pero sobre un tablero "temporal".

    Coge la pieza, el movimiento a realizar y un tablero temporal. Entonces hace el movimiento, es decir,
    genera un nuevo tablero con el movimiento realizado que es lo que devuelve.
    """
    board.move(piece, move[0], move[1])
    if skip:  # Hay que mirar si hay alguna pieza para eliminar
        board.remove(skip)  # Si la hay, la eliminamos
    return board
