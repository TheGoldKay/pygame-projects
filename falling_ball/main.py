import pygame as pg 
import sys
from random import randint

pg.init()

FPS = 60

WIN_WIDTH = 400
WIN_HEIGHT = 800
BG_COLOR = (0, 160, 80)

CIRCLE_RADIUS = 20
CIRCLE_CX = WIN_WIDTH / 2
CIRCLE_CY = (WIN_HEIGHT / 2) + (WIN_HEIGHT / 4)
CIRCLE_COLOR = (200, 200, 200)
CIRCLE_SPEED = 5
FALL = False 
OFF = 5

BAR_HEIGHT = 30
BAR_SPEED = 2

OFF = 20
HOLE_WIDTH = 60 + OFF * 2

BAR_ON = None 

def makeCircle(r, cx, cy):
  circle = pg.Rect(0, 0, r * 2, r * 2)
  circle.center = cx, cy 
  return circle 

def makeHole(bar):
  left = randint(0, WIN_WIDTH - HOLE_WIDTH)
  hole = pg.Rect(left, bar.y, HOLE_WIDTH, BAR_HEIGHT)
  return hole 

def makeBars():
  bars = []
  for y in range(BAR_HEIGHT, WIN_HEIGHT - BAR_HEIGHT, BAR_HEIGHT * 4):
    rect = pg.Rect(0, y, WIN_WIDTH, BAR_HEIGHT)
    hole = makeHole(rect)
    bars.append([rect, hole])
  bars[-1][0].y -= 20
  return bars 

def drawBars(win, bars):
  for pair in bars:
    pg.draw.rect(win, (180, 180, 180), pair[0])
    pg.draw.rect(win, BG_COLOR, pair[1])

def drawDisplay(win, circle, bars):
  win.fill(BG_COLOR)
  drawBars(win, bars)
  pg.draw.circle(win, 'green', circle.center, CIRCLE_RADIUS)
  pg.display.update()

def moveCircle(circle, left, right, bars):
  global FALL
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
  
  
  for pair in bars:
    bar, hole = pair 
    #left_rect = pg.Rect(hole.left, hole.top, OFF, BAR_HEIGHT)
    #right_rect = pg.Rect(hole.right - OFF, hole.top, OFF, BAR_HEIGHT)
    rect = pg.Rect(hole.left - OFF, hole.top - OFF, HOLE_WIDTH + OFF * 2, BAR_HEIGHT)
    if circle.colliderect(rect):
      FALL = True 
    #else:
    if circle.colliderect(bar):
          #if (circle.colliderect(hole) or circle.colliderect(left_rect) or circle.colliderect(right_rect)):
          #if not (bar.top < circle.bottom < bar.bottom or bar.right < circle.bottom < bar.bottom):
          circle.y = bar.y - CIRCLE_RADIUS * 2
          FALL = False 
  
  if FALL:
    circle.y += CIRCLE_SPEED
    
  if circle.y <= 0:
    circle.y = WIN_HEIGHT 
  elif circle.y + CIRCLE_RADIUS * 2 >= WIN_HEIGHT:
    circle.y = WIN_HEIGHT - CIRCLE_RADIUS * 2
  return circle 

def moveBars(bars):
  for i, pair in enumerate(bars):
    bar, hole = pair 
    bar.y -= BAR_SPEED
    if bar.y < 0: 
      bar.y = WIN_HEIGHT
    hole.y = bar.y 
    bars[i] = [bar, hole]
  return bars 
  
def main():
  clock = pg.time.Clock()
  circle = makeCircle(CIRCLE_RADIUS, CIRCLE_CX, CIRCLE_CY)
  pg.display.init()
  screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  pg.display.set_caption("Falling Ball")
  RIGHT = False 
  LEFT = False 
  #FALL = False 
  BAR_ON = None
  run = True 
  bars = makeBars()
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
    #circle = moveCircle(circle, LEFT, RIGHT, bars)
    #global FALL
    if LEFT:
      circle.x -=  CIRCLE_SPEED 
      LEFT = True 
    elif RIGHT:
      circle.x += CIRCLE_SPEED 
      RIGHT = True 
    if circle.x <= 0:
      circle.x = 0
    elif circle.x + CIRCLE_RADIUS * 2 >= WIN_WIDTH:
      circle.x = WIN_WIDTH - CIRCLE_RADIUS * 2
  
    for j, pair in enumerate(bars):
      bar, hole = pair 
      #left_rect = pg.Rect(hole.left, hole.top, OFF, BAR_HEIGHT)
      #right_rect = pg.Rect(hole.right - OFF, hole.top, OFF, BAR_HEIGHT)
      rect = pg.Rect(hole.left - OFF, hole.top - OFF, HOLE_WIDTH + OFF * 2, BAR_HEIGHT)
      if circle.colliderect(rect) and BAR_ON:
        #FALL = True 
        if BAR_ON+1 == len(bars):
          i = 0 
        else:
          i = BAR_ON 
        while not bars[i-1][0].colliderect(circle):
          circle.y += CIRCLE_SPEED
          bars = moveBars(bars)
          drawDisplay(screen, circle, bars)
          clock.tick(FPS)
        BAR_ON = i
          
      #else:
      if circle.colliderect(bar):
            #if (circle.colliderect(hole) or circle.colliderect(left_rect) or circle.colliderect(right_rect)):
            #if not (bar.top < circle.bottom < bar.bottom or bar.right < circle.bottom < bar.bottom):
            circle.y = bar.y - CIRCLE_RADIUS * 2
            #FALL = False 
            BAR_ON = j
            
      #if FALL:
      #  circle.y += CIRCLE_SPEED
        
      if circle.y <= 0:
        circle.y = WIN_HEIGHT 
      elif circle.y + CIRCLE_RADIUS * 2 >= WIN_HEIGHT:
        circle.y = WIN_HEIGHT - CIRCLE_RADIUS * 2
            
    bars = moveBars(bars)
    drawDisplay(screen, circle, bars)
  pg.quit()
  sys.exit()
    
  

if __name__ == '__main__':
  main()