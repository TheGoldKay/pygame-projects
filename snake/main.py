import sys 
import pygame 
from random import randint 

pygame.init()

class Screen:
  def __init__(self, width, height, background_color):
    self.w = width
    self.h = height
    self.bg_color = background_color
    pygame.display.init()
    self.surf = pygame.display.set_mode((width, height))
  
  def display(self):
    self.surf.fill(self.bg_color)

class Snake:
  def __init__(self, size, win):
    self.size = size 
    self.win = win
    self.body = []
    self.x_max = win.w // size 
    self.y_max = win.h // size 
    headx, heady = self._getXY()
    self.body.append([headx, heady])
  
  def draw(self, surf):
    for x, y in self.body:
      left, top = self._getTopLeft(x, y)
      rect = pygame.Rect(left, top, self.size, self.size)
      pygame.draw.rect(surf, 'green', rect, 10)
  
  def _getXY(self):
    x = randint(0, self.x_max)
    y = randint(0, self.y_max)
    return x, y 
  
  def _getTopLeft(self, x, y):
    left = x * self.size 
    top = y * self.size 
    return left, top 
  
def main():
  FPS = 60
  clock = pygame.time.Clock()
  screen = Screen(800, 800, 'grey')
  snake = Snake(40, screen)
  flag = True  
  while flag:
    clock.tick(FPS)
    screen.display()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        flag = False   
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          flag = False 
    snake.draw(screen.surf)
    pygame.display.update()
  pygame.quit()
  sys.exit()
  
if __name__ == '__main__':
  main()