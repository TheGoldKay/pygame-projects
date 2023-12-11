from screeninfo import get_monitors
import ctypes
import pygame, sys, time, os, math
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT

WIN_WIDTH = 500
WIN_HEIGHT = 500
FLAGS = pygame.RESIZABLE

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
    print ("top (%d), left (%d), bottom (%d), right (%d)" % (rect.top, rect.left, rect.bottom, rect.right))

    # bottom, top, left, right:  644 98 124 644

def main(screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT, flags=FLAGS, timer=time.time(), wait=0.005):
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
            new_width, new_height = math.floor(screen_width * 0.9999999), math.floor(screen_height * 0.9999999)
            new_pos_x = (pos_x + screen_width // 2) - new_width // 2
            new_pos_y = (pos_y + screen_height // 2) - new_height // 2
            changeWinSize(new_pos_x, new_pos_y, new_width, new_height, hwnd['window'])
            screen_width, screen_height = new_width, new_height
            pos_x = new_pos_x
            pos_y = new_pos_y
            timer = time.time()
            protoType()
        if done:
            pygame.quit()
            sys.exit()
        screen.fill((18, 53, 36))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()