import pygame as pg
from pygame.locals import *
import MainFrame.ObjectCore as MF
import mainLib

from OpenGL.GL import *
from OpenGL.GLU import *

cubeVertices = ((1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,-1,-1),(-1,-1,1),(-1,1,-1))
cubeEdges = ((0,1),(0,3),(0,4),(1,2),(1,7),(2,5),(2,3),(3,6),(4,6),(4,7),(5,6),(5,7))
cubeQuads = ((0,3,6,4),(2,5,6,3),(1,2,5,7),(1,0,4,7),(7,4,6,5),(2,3,0,1))
obj_core = ""

def init():
    global obj_core
    mw = mainLib.MapWorker()
    obj_core = MF.main(mw.GetMapData('rsr\\map\\' + "proto1" + '.json'))

def main():
    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    init()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)
    i = 0
    while True:
        #Events Ивенты
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.MOUSEMOTION:
                print(pg.mouse.get_pos())

        glRotatef(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #Main render
        obj_core.main(i)
        CamOBJ = obj_core.camera_ret()
        if not (CamOBJ is None):
            CamPos = CamOBJ.transform.position
            CamRot = CamOBJ.transform.rotation

        #solidCube()
        #wireCube()
        i += 1
        pg.display.flip()
        #pg.time.wait(10)

if __name__ == "__main__":
    main()