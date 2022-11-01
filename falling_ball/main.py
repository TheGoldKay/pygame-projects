from tkinter import LEFT
from matplotlib.backend_bases import DrawEvent
from matplotlib.pyplot import barh
from matplotlib.sankey import RIGHT
import pygame as pg 
import sys

pg.init()

FPS = 60

WIN_WIDTH = 400
WIN_HEIGHT = 800
BG_COLOR = (0, 160, 80)

CIRCLE_RADIUS = 25
CIRCLE_CX = WIN_WIDTH / 2
CIRCLE_CY = (WIN_HEIGHT / 2) + (WIN_HEIGHT / 4)
CIRCLE_COLOR = (200, 200, 200)
CIRCLE_SPEED = 5

BAR_HEIGHT = 30

def makeCircle(r, cx, cy):
  circle = pg.Rect(0, 0, r * 2, r * 2)
  circle.center = cx, cy 
  return circle 

def makeBar(bars):
  rect = pg.Rect(0, WIN_HEIGHT - BAR_HEIGHT, WIN_WIDTH, BAR_HEIGHT)
  bars.append(rect)
  return bars 

def drawBars(win, bars):
  for bar in bars:
    pg.draw.rect(win, 'black', bar, 4)

def drawDisplay(win, circle, bars):
  win.fill(BG_COLOR)
  pg.draw.circle(win, 'white', circle.center, CIRCLE_RADIUS)
  drawBars(win, bars)
  pg.display.update()

def moveCircle(circle, left, right):
  if left:
    circle.x -=  CIRCLE_SPEED 
    LEFT = True 
  elif right:
    circle.x += CIRCLE_SPEED 
    RIGHT = True 
  if circle.x <= 0:
    circle.x = 0
  elif circle.x + CIRCLE_RADIUS * 2 >= WIN_WIDTH:
    circle.x = WIN_WIDTH - CIRCLE_RADIUS * 2
  return circle 
  
def main():
  clock = pg.time.Clock()
  circle = makeCircle(CIRCLE_RADIUS, CIRCLE_CX, CIRCLE_CY)
  pg.display.init()
  screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  RIGHT = False 
  LEFT = False 
  run = True 
  bars = []
  bars = makeBar(bars)
  while run:
    clock.tick(FPS)
    for event in pg.event.get():
      if event.type == pg.QUIT:
        run = False 
      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          run = False 
        elif event.key in (pg.K_a, pg.K_LEFT):
          LEFT = True  
        elif event.key in (pg.K_d, pg.K_RIGHT):
          RIGHT = True 
      elif event.type == pg.KEYUP:
        LEFT = False 
        RIGHT = False 
    circle = moveCircle(circle, LEFT, RIGHT)
    drawDisplay(screen, circle, bars)
  pg.quit()
  sys.exit()
    
  

if __name__ == '__main__':
  main()