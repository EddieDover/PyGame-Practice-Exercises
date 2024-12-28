import pygame as pg
import os
import ctypes
from sys import exit



def find_ratio(x):
    """
    Finds ratio of 5120x2880 to the active resolution. Used in scaling backgrounds, sprites, and fonts. 
    """
    ratio = x/5120
    return ratio

def scale_bg(name, screen):
    img = pg.image.load(f'img/bg_{name}.png').convert_alpha() # Loads img
    x, y = screen.get_size() # Retrieves screen size
    img = pg.transform.scale(img, (x, y)) # Resizes img to screen size
    return img

def scale_spr(name, screen, pos):
    img = pg.image.load(f'img/spr_{name}.png') # Loads img
    x, y = screen.get_size() # Retrieves screen size
    w, h = img.get_size() # Retrieves img dimensions
    ratio = find_ratio(x)
    # Uses ratio to resize img appropriately for current resolution
    img = pg.transform.scale(img, (w*ratio, h*ratio))
    surf, pos = img, (pos[0]*ratio, pos[1]*ratio)
    return surf, pos

def scale_txt(surf, screen, pos):
    x, y = screen.get_size()
    w, h = surf.get_size()
    ratio = find_ratio(x)
    surf = pg.transform.scale(surf, (w*ratio, h*ratio))
    pos = (pos[0]*ratio, pos[1]*ratio)
    return surf, pos

def get_res(settings):
    res = settings.get("Resolution")
    res = list(map(int, res.split('x'))) # turns string into a list of ints
    return res

def set_res(settings):
    res = settings.get('Resolution')
    res = list(map(int, res.split('x'))) # turns string into a list of ints
    fullscreen = settings.get('Fullscreen')
    print(f'fullscreen = {fullscreen}')
    if fullscreen == "0":
        screen = pg.display.set_mode(res)
    else: 
        screen = pg.display.set_mode(res, pg.FULLSCREEN)
    return screen

def start_menu(screen, settings):

    X, Y = 5120, 2880 # The constant size of the 'canvas', which the image files are already
                      # sized appropriately for before any scaling is done. Use this like a coordinate
                      # system since it's constant, then run it thorugh display functions for final
                      # placement accounting for resolution. 
    x, y = get_res(settings) # The resolution selected in settings. 
    w, h = screen.get_size() # The actual resolution, which will differ from that in settings if fullscreen is enabled.

    clock = pg.time.Clock()

    font = pg.font.SysFont('Comic Sans', 100)
    header = font.render("Stef's test game", True, 'Black')

    bg_start = scale_bg('start', screen)
    ground_surf, ground_pos = scale_spr('ground', screen, (0, Y-320))
    protag_surf, protag_pos = scale_spr('protag', screen, (X*.1, Y-860))
    txt_surf, txt_pos = scale_txt(header, screen, (X*.5-(header.get_size()[0]*.5), Y*.02))

    protag_x = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        protag_x += w*.01
        if protag_x > w:
            protag_x = -w*.4
        screen.blit(bg_start, (0,0))
        screen.blit(ground_surf, ground_pos)
        screen.blit(protag_surf, (protag_pos[0]+protag_x, protag_pos[1]))
        screen.blit(txt_surf, txt_pos)
        pg.display.update()
        clock.tick(60)

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1' # centers window when not in fullscreen
    pg.init()
    pg.font.init()
    ctypes.windll.user32.SetProcessDPIAware() # keeps Windows GUI scale settings from messing with resolution
    pg.display.set_caption("Stef's Practice Game")

    # Opens settings.csv and creates dictionary for settings
    settings = {}
    with open('settings.csv') as file:
        for line in file:
            key, value = line.split(': ')
            settings[key] = value

    screen = set_res(settings)
    
    start_menu(screen, settings)

if __name__ == '__main__':
    main()