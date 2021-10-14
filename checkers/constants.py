import pygame

# Ponemos que sean 800 pixeles cuadrado.
# Cada celda tendrá pues 10 píxeles
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# Colores en rgb
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
BROWN = (110,44,0)
BEIGE = (250,215,160)
GRAY = (128,128,128)

# La corona de la reina:
# He cogido una foto sugerida por el youtuber ya que como he hecho fichas negras, si cojo
# la típica corona negra, no se verá...
CROWN = pygame.transform.scale(pygame.image.load('pictures/crown.png'), (45,25))  # Esto es para que se escale.
