import pygame 
from random import randint, randrange

POS = set()
WIDTH, HEIGHT = 800, 600
FPS = 120

def create_window(width, height):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    return window

def randPos(width, height):
    return (randrange(width), randrange(height))

def randColor():
    return (randint(0, 255), randint(0, 255), randint(0, 255))

def paint(pxarr, x, y, color, var = 0, mouse = False):
    var = var or randint(1, 10)
    for i in range(x - var//2, x + var//2):
        for j in range(y - var//2, y + var//2):
            if not mouse:
                if (i, j) in POS:
                    return
                POS.add((i, j))
            if i < 0 or j < 0:
                continue 
            if i >= WIDTH or j >= HEIGHT:
                continue 
            pxarr[i, j] = color

def main():
    win = create_window(WIDTH, HEIGHT)
    pxarr = pygame.PixelArray(win)
    win.fill((255, 255, 255))
    pygame.display.set_caption("Pixel Manipulation")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        x, y = randPos(WIDTH, HEIGHT)
        color = randColor()
        paint(pxarr, x, y, color)
        pxarr[x, y] = (0, 0, 0) # square's center
        mouse_x, mouse_y = pygame.mouse.get_pos()
        paint(pxarr, mouse_x, mouse_y, (255, 255, 255), 25, mouse = True)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()