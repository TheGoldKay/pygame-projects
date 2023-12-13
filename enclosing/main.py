from screeninfo import get_monitors
import ctypes
import pygame, sys, time, os, math
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT
import win32api
import win32con
import win32gui

WIN_WIDTH = 500
WIN_HEIGHT = 500
PHTHALO_GREEN = (18, 53, 36)
TRANSPARENT = (0, 0, 0) # to create the effect of transparency any color can be used except PHTHALO_GREEN (Player's screen)
PLAYER_COLOR = (255, 255, 255)
PLAYER_RADIUS = 10
STEP = 1
SPEED = 0.04 # time in seconds to wait before the window is resized
FLAGS = pygame.NOFRAME
RADIUS = WIN_WIDTH // 2
FPS = 60

def stop():
    pygame.quit()
    sys.exit()

def setWindowPos(full_sceen=True):
    monitors = get_monitors() # Get the resolution of all of the users monitors
    for monitor in monitors:
        if monitor.is_primary: # main monitor
            monitor_width = monitors[0].width 
            monitor_height = monitors[0].height 
            break
    if(full_sceen):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (0, 0)
        return monitor_width, monitor_height
    else:
        pos_x = monitor_width // 2 - WIN_WIDTH // 2
        pos_y = monitor_height // 2 - WIN_HEIGHT // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)
        return WIN_WIDTH, WIN_HEIGHT

def setWindowTransparent():
    hwnd = pygame.display.get_wm_info()["window"] # Getting information of the current active window
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                        hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # This will set the opacity and transparency color key of a layered window
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT), 255, win32con.LWA_COLORKEY)
    return hwnd # the game's window ID

def makeRect(x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    return rect
    
def main(timer=time.time(), wait=SPEED, radius=RADIUS):
    screen_width, screen_height = setWindowPos()
    window_screen = pygame.display.set_mode((screen_width, screen_height), FLAGS)
    pygame.display.set_caption("Enclosing")
    clock = pygame.time.Clock()
    hwnd = setWindowTransparent()
    rect_width = 500
    rect_height = 250
    rect = makeRect(screen_width // 2 - rect_width // 2, screen_height // 2 - rect_height // 2, rect_width, rect_height)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop()
        if time.time() - timer > wait:
            center = rect.center 
            rect.width = rect.width - 2
            rect.height = rect.height - 1
            rect.center = center
            timer = time.time()
        if (rect.width < 100):
            stop()   
        window_screen.fill(TRANSPARENT)
        pygame.draw.rect(window_screen, PHTHALO_GREEN, rect)
        rectBottom = pygame.Rect(rect.right, rect.bottom, rect.width, rect.height)
        rectTop = rect.copy()
        rectTop.bottom = rect.top 
        rectTop.right = rect.left
        pygame.draw.rect(window_screen, PHTHALO_GREEN, rectBottom)
        pygame.draw.rect(window_screen, PHTHALO_GREEN, rectTop)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()