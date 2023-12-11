from screeninfo import get_monitors
import ctypes
import pygame, sys, time, os, math
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

WIN_WIDTH = 500
WIN_HEIGHT = 500
FLAGS = pygame.NOFRAME

def changeWinSize(x, y, new_width, new_height, hwnd):
    # Use ctypes to change the window size
    ctypes.windll.user32.SetWindowPos(
        hwnd,
        ctypes.c_int(0),  # HWND_TOP,
        x,
        y,
        new_width,
        new_height,
        0  # Flags
    )

def protoType():
    # get our window ID:
    hwnd = pygame.display.get_wm_info()["window"]

    # Jump through all the ctypes hoops:
    prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
    paramflags = (1, "hwnd"), (2, "lprect")

    GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)

    # finally get our data!
    rect = GetWindowRect(hwnd)
    #print ("top (%d), left (%d), bottom (%d), right (%d)" % (rect.top, rect.left, rect.bottom, rect.right))

    # bottom, top, left, right:  644 98 124 644

def protoType2():
    import ctypes
    import pygame

    # Load the necessary Windows DLLs
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    # Define the window center and radius
    center_x = 400
    center_y = 300
    radius = 200

    # Calculate points on the circumference
    points = []
    for angle in range(0, 360):
        x = int(center_x + radius * math.cos(math.radians(angle)))
        y = int(center_y + radius * math.sin(math.radians(angle)))
        points.append((x, y))


    # Convert points to Windows POINT structure
    points_array = (ctypes.wintypes.POINT * len(points))(*points)

    # Create a region object
    region_handle = gdi32.CreatePolygonRgn(points_array, len(points), 0)
    
    # Initialize Pygame and create the screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
    pygame.display.set_caption("Custom Window Shape")

    # Define the window handle
    window_handle = pygame.display.get_wm_info()['window']

    # Set window region using the HRGN handle
    user32.SetWindowRgn(window_handle, region_handle, True)

    # Set window transparency and frameless style
    screen.set_alpha(None)
    #window = pygame.display.get_wm_info()
    #window.set_frame(False)
    #window.update()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with any desired color
        screen.fill((255, 255, 255))

        # Update the display
        pygame.display.flip()

    # Clean up
    gdi32.DeleteObject(region_handle)
    pygame.quit()


def main(screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT, flags=FLAGS, timer=time.time(), wait=0.00000005):
    monitors = get_monitors() # Get the resolution of all of the users monitors
    for monitor in monitors:
        if monitor.is_primary: # main monitor
            monitor_width = monitors[0].width 
            monitor_height = monitors[0].height 

    pos_x = monitor_width // 2 - screen_width // 2
    pos_y = monitor_height // 2 - screen_height // 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)

    pygame.init()
    
    screen = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.display.set_caption("Enclosing")
    done = False
    clock = pygame.time.Clock()
    
    hwnd = pygame.display.get_wm_info()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
        if time.time() - timer > wait:
            new_width, new_height = math.floor(screen_width * 0.99999999999999), math.floor(screen_height * 0.99999999999999)
            new_pos_x = (pos_x + screen_width // 2) - new_width // 2
            new_pos_y = (pos_y + screen_height // 2) - new_height // 2
            changeWinSize(new_pos_x, new_pos_y, new_width, new_height, hwnd['window'])
            screen_width, screen_height = new_width, new_height
            pos_x = new_pos_x
            pos_y = new_pos_y
            timer = time.time()
        if done:
            pygame.quit()
            sys.exit()
        screen.fill((18, 53, 36))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    protoType2()