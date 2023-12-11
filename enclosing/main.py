import pygame

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Enclosing")

def main():
    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((18, 53, 36))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()