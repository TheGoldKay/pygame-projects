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
    pygame.display.update()

def main():
  FPS = 60
  clock = pygame.time.Clock()
  screen = Screen(800, 800, 'grey')
  flag = True  
  while flag:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        flag = False   
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          flag = False 
    screen.display()
  pygame.quit()
  sys.exit()
  
if __name__ == '__main__':
  main()