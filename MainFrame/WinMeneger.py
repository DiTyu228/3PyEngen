import main
import pygame

def GetScreenZise():
    return (main.scr_h, main.scr_w)

class mouse():
    def __init__(self):
        pass

    def get_position(self):
        return pygame.mouse.get_pos()