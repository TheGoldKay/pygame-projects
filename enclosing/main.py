import pygame, sys, time

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600
FLAGS = pygame.RESIZABLE

def main(screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT, flags=FLAGS, timer=time.time(), wait=3):
    screen = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.display.set_caption("Enclosing")
    done = False
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        #if time.time() - timer > wait:
        #    pygame.quit()
        #    main(screen_width - 1, screen_height - 1)
        if done:
            pygame.quit()
            sys.exit()
        screen.fill((18, 53, 36))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()