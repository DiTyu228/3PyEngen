import RenderTest
import main
import pygame

def GetScreenZise():
    return (main.scr_h, main.scr_w)

class mouse():
    def __init__(self):
        pass

    def get_position(self):
        if len(RenderTest.mouse_pos) > 2:
            return RenderTest.mouse_pos
        else:
            return (1, 1)