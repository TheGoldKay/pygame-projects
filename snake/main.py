import sys 
import pygame 
import random

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
  def __init__(self, size, win, speed=1):
    self.size = size 
    self.win = win
    self.vel = speed
    self.body = []
    self.x_max = win.w // size 
    self.y_max = win.h // size 
    headx, heady = self._getXY()
    self.body.append([headx, heady])
    self.dir = random.choice(['left', 'right', 'up', 'down'])
  
  def draw(self, surf):
    for x, y in self.body:
      left, top = self._getTopLeft(x, y)
      rect = pygame.Rect(left, top, self.size, self.size)
      pygame.draw.rect(surf, 'green', rect, 10)
  
  def update(self):
    x, y = self.body[0]
    if self.dir == 'up':
      y -= self.vel 
    elif self.dir == 'down':
      y += self.vel 
    elif self.dir == 'left':
      x -= self.vel 
    elif self.dir == 'right':
      x += self.vel 
    if y < 0:
      y = self.y_max
    elif y > self.y_max:
      y = 0
    if x < 0:
      x = self.x_max
    elif x > self.x_max:
      x = 0
    self.body[0] = [x, y]
    
  def _getXY(self):
    x = random.randint(0, self.x_max)
    y = random.randint(0, self.y_max)
    return x, y 
  
  def _getTopLeft(self, x, y):
    left = x * self.size 
    top = y * self.size 
    return left, top 
  
def main():
  FPS = 5
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
        if event.key in (pygame.K_a, pygame.K_LEFT) and not snake.dir == 'right':
          snake.dir = 'left'
        elif event.key in (pygame.K_d, pygame.K_RIGHT) and not snake.dir == 'left':
          snake.dir = 'right'
        elif event.key in (pygame.K_w, pygame.K_UP) and not snake.dir == 'down':
          snake.dir = 'up'
        elif event.key in (pygame.K_s, pygame.K_DOWN) and not snake.dir == 'up':
          snake.dir = 'down'
    snake.update()
    snake.draw(screen.surf)
    pygame.display.update()
  pygame.quit()
  sys.exit()
  
if __name__ == '__main__':
  main()