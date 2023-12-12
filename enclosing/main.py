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
STEP = 1
SPEED = 0.04 # time in seconds to wait before the window is resized
FLAGS = pygame.NOFRAME
RADIUS = WIN_WIDTH // 2

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
def stop():
    pygame.quit()
    sys.exit()

def getWindowRect():
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

def setWindowTransparent():
    pygame.init() 
    TRANSPARENT = (255,0,128)
    window_screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), FLAGS)
    # size of the pygame window will be of width 700 and height 450
    hwnd = pygame.display.get_wm_info()["window"]
    # Getting information of the current active window
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                        hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT), 0, win32con.LWA_COLORKEY)
    # This will set the opacity and transparency color key of a layered window
    font = pygame.font.SysFont("Times New Roman", 54)
    while True: 
        # Accessing the event if any occurred
        for event in pygame.event.get(): 
            # Checking if quit button is pressed or not
            if event.type == pygame.QUIT: 
                # If quit then store true
                done = 1			
            # Checking if the escape button is pressed or not
            if event.type == pygame.KEYDOWN: 
                # If the escape button is pressed then store true in the variable
                if event.key == pygame.K_ESCAPE: 
                    stop()
        # Transparent background
        window_screen.fill(TRANSPARENT) 
        # Calling the show_text function
        window_screen.blit(font.render("Press Esc: ", 0, (255, 0, 0)), (0, 0))
        window_screen.blit(font.render("For closing window", 0, (255, 0, 0)), (0, 50))
        # Checking for the update in the display
        pygame.display.update()




def main(screen_width=WIN_WIDTH, screen_height=WIN_HEIGHT, flags=FLAGS, timer=time.time(), wait=SPEED, radius=RADIUS):
    monitors = get_monitors() # Get the resolution of all of the users monitors
    for monitor in monitors:
        if monitor.is_primary: # main monitor
            monitor_width = monitors[0].width 
            monitor_height = monitors[0].height 

    pos_x = monitor_width // 2 - screen_width // 2
    pos_y = monitor_height // 2 - screen_height // 2
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x, pos_y)

    pygame.init()
    
    window_screen = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.display.set_caption("Enclosing")
    clock = pygame.time.Clock()
    
    hwnd = pygame.display.get_wm_info()["window"] # Getting information of the current active window
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                        hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # This will set the opacity and transparency color key of a layered window
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 0, 128), 0, win32con.LWA_COLORKEY)
    

    limit = 50 # the smallest the window's height and wight are allowed to get
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop()
        if time.time() - timer > wait:
            #new_width, new_height = math.floor(screen_width * STEP), math.floor(screen_height * STEP)
            new_width, new_height = screen_width - STEP, screen_height - STEP
            new_pos_x = (pos_x + screen_width // 2) - new_width // 2
            new_pos_y = (pos_y + screen_height // 2) - new_height // 2
            changeWinSize(new_pos_x, new_pos_y, new_width, new_height, hwnd)
            screen_width, screen_height = new_width, new_height
            pos_x = new_pos_x
            pos_y = new_pos_y
            radius -= STEP
            timer = time.time()
            if (screen_width < limit or screen_height < limit):
                stop()   
        window_screen.fill((255,0,128))
        pygame.draw.circle(window_screen, PHTHALO_GREEN, window_screen.get_rect().center, radius)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()