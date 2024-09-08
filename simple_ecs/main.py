import pygame
import esper
from pygame_emojis import load_emoji
import math

FPS = 60
RESOLUTION = 720, 480

EMOJI_SIZE = (10, 10)
SQUARES = {
    'red': '🟥',
    'green': '🟩',
    'yellow': '🟨',
    'blue': '🟦',
    'brown': '🟫',
    'purple': '🟪',
    'white': '⬜',
    'black': '⬛',
}

PLAYER_VEL = 3
SCALE = 200 

##################################
#  Define some Components:
##################################
class Velocity:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Renderable:
    def __init__(self, image, posx, posy, depth=0):
        self.image = image
        self.depth = depth
        self.x = posx
        self.y = posy
        self.w = image.get_width()
        self.h = image.get_height()


################################
#  Define some Processors:
################################
class MovementProcessor:
    def __init__(self, minx, maxx, miny, maxy):
        super().__init__()
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.scale = SCALE

    def process(self, dt):
        # This will iterate over every Entity that has BOTH of these components:
        for ent, (vel, rend) in esper.get_components(Velocity, Renderable):
            # Update the Renderable Component's position by it's Velocity:
            norm_x, norm_y = self.normalize(vel.x, vel.y)
            rend.x += norm_x * self.scale * dt
            rend.y += norm_y * self.scale * dt
            print(norm_x * self.scale * dt, norm_y * self.scale * dt)
            # An example of keeping the sprite inside screen boundaries. Basically,
            # adjust the position back inside screen boundaries if it tries to go outside:
            rend.x = max(self.minx, rend.x)
            rend.y = max(self.miny, rend.y)
            rend.x = min(self.maxx - rend.w, rend.x)
            rend.y = min(self.maxy - rend.h, rend.y)

    def normalize(self, x, y):
        d = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        return (x / d, y / d) if d else (0, 0)

class RenderProcessor:
    def __init__(self, window, clear_color=(0, 0, 0)):
        super().__init__()
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        render = []
        for ent, rend in esper.get_component(Renderable):
            render.append(rend)
        render.sort(key=lambda r: r.depth)
        for rend in render:
            self.window.blit(rend.image, (rend.x, rend.y))
        # Flip the framebuffers
        pygame.display.flip()


################################
#  The main core of the program:
################################
def run():
    # Initialize Pygame stuff
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Esper Pygame example")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # Initialize Esper world, and create a "player" Entity with a few Components.
    player = esper.create_entity()
    esper.add_component(player, Velocity(x=0, y=0))
    esper.add_component(player, Renderable(image=load_emoji(SQUARES['white'], EMOJI_SIZE), posx=100, posy=100, depth=1))
    # Another motionless Entity
    enemy = esper.create_entity()
    esper.add_component(enemy, Renderable(image=load_emoji(SQUARES['black'], EMOJI_SIZE), posx=400, posy=250, depth=0))

    # Create some Processor instances, and asign them to be processed.
    render_processor = RenderProcessor(window=window)
    movement_processor = MovementProcessor(minx=0, maxx=RESOLUTION[0], miny=0, maxy=RESOLUTION[1])

    running = True
    while running:  
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Here is a way to directly access a specific Entity's
                    # Velocity Component's attribute (y) without making a
                    # temporary variable.
                    esper.component_for_entity(player, Velocity).x = -PLAYER_VEL
                elif event.key == pygame.K_RIGHT:
                    # For clarity, here is an alternate way in which a
                    # temporary variable is created and modified. The previous
                    # way above is recommended instead.
                    player_velocity_component = esper.component_for_entity(player, Velocity)
                    player_velocity_component.x = PLAYER_VEL
                elif event.key == pygame.K_UP:
                    esper.component_for_entity(player, Velocity).y = -PLAYER_VEL
                elif event.key == pygame.K_DOWN:
                    esper.component_for_entity(player, Velocity).y = PLAYER_VEL
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    esper.component_for_entity(player, Velocity).x = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    esper.component_for_entity(player, Velocity).y = 0

        # A single call to e.process() will update all Processors:
        render_processor.process()
        movement_processor.process(dt)


if __name__ == "__main__":
    run()
    pygame.quit()
