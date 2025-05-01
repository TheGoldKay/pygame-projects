# Example file showing a basic pygame "game loop"
import pygame

WIN_W, WIN_H = 100, 100

def make_window(mouse_x, mouse_y):
    return pygame.Window(title="Clicked!", position=(mouse_x + WIN_W // 2, mouse_y + WIN_H // 2), size=(WIN_W, WIN_H))

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Window Testing")
    clock = pygame.time.Clock()
    running = True
    windows = []
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    window = make_window(*pygame.mouse.get_pos())
                    window.always_on_top = True  # Set the window to always be on top
                    window.opacity = 0.5
                    windows.append(window)
            # Add this event check for window closing
            if event.type == pygame.WINDOWCLOSE:
                print("Window close event detected")
                for window in windows[:]:  # Create a copy of the list to safely modify it
                    print(event.window, window.id)
                    if event.window.id == window.id:
                        print("Window closed")
                        windows.remove(window)
                        window.destroy()
                        break

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE
        pygame.draw.circle(screen, "white", pygame.mouse.get_pos(), 10)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
    
if __name__ == "__main__":
    main()