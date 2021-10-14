import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE
# La razón por la cual puedo importar from checkers.constants es porque he añadido el
# archivo __init__.py en la carpeta checkers.
# Éste dice "hey, esto es un paquete de python"
from checkers.board import Board
from checkers.game import Game
from checkers.minimaxAlgorithm import *  # El asterisco es para importar toda función

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Este comando abre la ventana
pygame.display.set_caption('Checkers')  # Este es el titulillo que sale en la ventana
FPS = 60  # Esto es algo que tiene que ver con el tiempo


def getRowColFromMouse(pos):
    """
    Le pasaremos la posición de nuestro ratón (cuando hagamos click: es uno de esos 'eventos')
    y la función simplemente nos dará la posición (x,y) (siguiendo el sistema de coordenadas de
    pygame) donde hemos hecho click.

    pos es una tupla.

    La posición será convertida en el "cuadrado o casilla en la que hemos hecho click"
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col  # Como tupla


def main():
    """
    La función main será la única que ejecutaremos y desde ella se llamará a todas las funciones necesarias.

    IMPORTANTE: hay tres modalidades de ejecutar esta función.

    1. Para la cual ha sido creada: jugar contra la IA
        Para ello simplemente hay que comentar uno de los "if statements" y dejar el otro, eligiendo el
        color que se desee para la máquina (que será el que se deje sin comentar).

    2. Si queremos ver cómo la máquina juega contra sí misma.
        Entonces hay que dejar los dos "if statements" sin comentar, e ignorar la parte del "for event"
        ya que nunca entrará en ninguno de sus casos.

    3. Si quisiéramos jugar sin ninguna inteligencia artificial (por ejemplo, contra nosotros mismos,
       o dos jugadores humanos, etc.)
        Entonces comentar ambos "if statements" antes del "for event".

    Nos hubiese gustado crear un menú en el que esto se pudiese escoger. Pero era demasiado complejo
    y no teníamos suficiente tiempo para ello.
    """
    run = True
    # The clock will asure the timing for the execution.
    clock = pygame.time.Clock()  # El reloj asegurará el tiempo de ejecución
    game = Game(WIN)  # Inicializamos la clase game.
    game.turn = WHITE  # Aquí podemos decidir quien empieza. Por norma empiezan las blancas pero SE PUEDE CAMBIAR
    while run:
        clock.tick(FPS)  # Esto es un tick del reloj creo

        # |****************************************************************************************|
        # |*******************|           IA PARA LAS BLANCAS             |************************|
        # |****************************************************************************************|
        if game.turn == WHITE:
            value, newBoard = minimaxWhite(game.getBoard(), 1, WHITE, game)  # Obtenemos el mejor movimiento, con la profundidad que queramos
            if newBoard is None:  # Esto es para evitar un error. Si es None, significa que no tiene posibles movimientos
                print('White can\'t move. The winner is BLACK')  # En ese caso, ganan las negras
                break
            game.aiMove(newBoard)  # Hacemos el movimiento
        pygame.time.delay(100)  # Ponemos un poco de delay para que se pueda apreciar el movimiento
        game.update()  # Actualizamos. Esto dibujará el nuevo tablero con el movimiento hecho

        # |****************************************************************************************|
        # |*******************|           IA PARA LAS NEGRAS             |************************|
        # |****************************************************************************************|
        '''
        if game.turn == BLACK:
            value, newBoard = minimaxBlack(game.getBoard(), 3, BLACK, game)
            if newBoard is None:
                print('Black can\'t move. The winner is WHITE')
                break
            game.aiMove(newBoard)
        '''

        if game.winner() is not None:  # Miramos si hay ganador
            print('The winner is ' + str(game.winner()))  # Si lo hay, decimos quien es y cerramos el juego
            run = False

        # Un event es por ejemplo clickar, o por ejemplo cerrar la ventana o apretar intro, etc.
        for event in pygame.event.get():
            # Verifica si alguno de los siguientes eventos ha pasado
            if event.type == pygame.QUIT:  # Significa que hemos apretado el botón de cerrar la ventana
                run = False  # Salimos pues
            if event.type == pygame.MOUSEBUTTONDOWN:  # Significa que hemos apretado el botón del ratón en algún sitio dentro de la ventana
                pos = pygame.mouse.get_pos()  # Esto me dará la posición del ratón, me lo devuelve en píxeles
                row, col = getRowColFromMouse(pos)  # Me devuelve la posición (row, col) de pos
                game.select(row, col)  # Esto lo hace to do
        pygame.time.delay(100)  # Pongo el delay para que, antes de dibujar el tablero, que se aprecie el movimiento
        game.update()  # Dibujamos el tablero actualizado
    pygame.quit()  # Acaba con la ejecución de pygame


main()  # Esto es para ejecutar el main...
