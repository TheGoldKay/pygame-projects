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
    self.x_max = win.w // size 
    self.y_max = win.h // size 
    self.dir = 'left'
    self._makeBody()
    self.last = self.body[-1]
  
  def _makeBody(self, length=4):
    self.body = []
    headx, heady = self._getXY()
    self.body.append([headx, heady])
    for i in range(1, length):
      self.body.append([headx + i, heady])
     
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
    self.body.insert(0, [x, y])
    self.last = self.body[-1]
    del self.body[-1]
  
  def _getHeadRect(self):
    left, top = self.body[0]
    return pygame.Rect(left, top, self.size, self.size)
    
  def gotFood(self, food):
    #head = self._getHeadRect()
    #if head.colliderect(foodRect):
    x, y = self.body[0]
    if food.x == x and food.y == y:
      self.body.append(self.last)
      return True 
    return False          
    
  def _getXY(self):
    x = random.randint(0, self.x_max)
    y = random.randint(0, self.y_max)
    return [x, y] 
  
  def _getTopLeft(self, x, y):
    left = x * self.size 
    top = y * self.size 
    return left, top 

class Food:
  def __init__(self, size, xmax, ymax):
    self.s = size 
    self.xmax = xmax 
    self.ymax = ymax 
    self.newPos()
  
  def newPos(self):
    self.x = random.randint(0, self.xmax)
    self.y = random.randint(0, self.ymax)
  
  def getRect(self):
    return pygame.Rect(self.s * self.x, self.s * self.y, self.s, self.s)
  
  def draw(self, surf):
    rect = self.getRect()
    pygame.draw.rect(surf, 'white', rect)
    

def main():
  FPS = 5
  clock = pygame.time.Clock()
  screen = Screen(800, 800, 'grey')
  snake = Snake(40, screen)
  food = Food(snake.size, snake.x_max, snake.y_max)
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
    if snake.gotFood(food):
      food.newPos()
    food.draw(screen.surf)
    snake.draw(screen.surf)
    pygame.display.update()
  pygame.quit()
  sys.exit()
  
if __name__ == '__main__':
  main()