import pygame as pg 
import sys

pg.init()

WIN_WIDTH = 400
WIN_HEIGHT = 800
BG_COLOR = (0, 160, 80)

CIRCLE_RADIOUS = 25
CIRCLE_CX = WIN_WIDTH / 2
CIRCLE_CY = (WIN_HEIGHT / 2) + (WIN_HEIGHT / 4)
CIRCLE_COLOR = (100, 10, 10)

def makeCircle(r, cx, cy):
  circle = pg.Rect(cx - r, cy - r, r * 2, r * 2)
  return circle 



def main():
  circle = makeCircle(CIRCLE_RADIOUS, CIRCLE_CX, CIRCLE_CY)
  pg.display.init()
  screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  while True:
    screen.fill(BG_COLOR)
    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        sys.exit()
      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          pg.quit()
          sys.exit()
    pg.display.flip()
    
  

if __name__ == '__main__':
  main()