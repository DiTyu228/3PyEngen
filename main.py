import Consoll
import m_math
import random
import time

import pygame
import pygame.freetype
import keyboard
import numpy as np
import math
import os
import sys

import mainLib
import MainFrame.ObjectCore as og
from MainFrame import GPURenderHelper as GPUhelp
from Consoll.pygame_console import Console
import m_math as ma

from OpenGL.GL.SUN import vertex
from OpenGL.GL.feedback import Vertex
from OpenGL.arrays import vbo
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileShader, compileProgram

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np

import multiprocessing
import threading
import importlib.util

resurs = "rsr\\"
textur = "material\\"
dir = os.getcwd()
obj_on_scene = []
main = mainLib.main
shad = mainLib.shader_worker()
eng_ver = "0.1.2 2d render in progress"
models = dir + "\\" + resurs + "\\" + "models\\"
scr_w = 800
scr_h = 600
mX = 0
mY = 0
_obj_core = 0


def terminal_processing(queue):
    mw = mainLib.MapWorker()
    while True:
        try:
            command = 'exit'
            if command.lower().startswith("map"):
                com = command.lower().split(" ")
                data = mw.GetMapData('rsr\\map\\' + str(com[1]) + '.json')
                queue.put(data)
            elif command.lower().startswith("exit"):
                exit(0)
            elif command.lower().startswith("ver"):
                print("engen version ")
                print(eng_ver)

        except EOFError:
            print("terminal error")
            break


def MapSelect(path):
    global _obj_core
    _obj_core = og.main(mw.GetMapData(path))


if __name__ == '__main__':
    # нициализация
    i = 0
    GPUrd = GPUhelp.main()
    sys.path.append('\\')



    # Создаем очередь для передачи команд между процессами
    command_queue = multiprocessing.Queue()

    # Создаем процесс для выполнения обработки команд в терминале
    terminal_processor = multiprocessing.Process(target=terminal_processing, args=(command_queue,))

    # Запускаем процесс обработки команд в терминале
    terminal_processor.start()

    conrine = True  # рендер на CPU если true если false рендер на GPU
    scripts_path = 'rsr\\scripts'
    script_files = os.listdir(scripts_path)

    # Предположим, что у вас есть класс с именем таким же, как имя скрипта
    class_name = script_files[0].split('.')[0]

    # Импортируем модуль
    vrct = ma.vectors()
    # obj_core = object_core.MyGLObject()
    textures = main.loadpak(0)
    name = textur.replace(";" and "all" or "png" or "jpg", "")
    texway = dir + "\\" + resurs + textur + name + "\\"
    mapway = dir + "\\" + resurs + "map\\"
    tmode = ""
    noclip = False
    dppress = False
    if "png" in textures:
        tmode = "png"
    if "jpg" in textures:
        tmode = "png"
    sphere = gluNewQuadric()
    paused = False
    run = True
    last_cam_pos = m_math.Vector3(0, 0, 0)
    CamPos = m_math.Vector3(0, 0, 0)

    ambient = ""

    lightpos = 0, 1, 0,
    greencolor = (0.2, 0.8, 0.0, 0.8)
    cxrot = 0
    cyrot = 0
    czrot = 0
    cx = 0
    cy = 0
    cz = 0
    wx = 0
    wy = 0
    wz = 0
    speed = 0.1
    up_down_angle = 0.0
    vertex = [
        [1.0, -1.0, -1.0],
        [1.0, 1.0, -1.0, ],
        [-1.0, 1.0, -1.0, ],
        [-1.0, -1.0, -1.0, ],
        [1.0, - 1.0, 1.0, ],
        [1.0, 1.0, 1.0, ],
        [-1.0, -1.0, 1.0, ],
        [-1.0, 1.0, 1.0]
    ]

    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    if conrine is True:
        print("shader error")
        mw = mainLib.MapWorker()
        pygame.init()
        pygame.font.init()
        display = (scr_w, scr_h)
        scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        #console = Console(pygame, scree.get_width(),
        #                  Consoll.pygame_console.Console.get_console_config_json("", config_file_path="Consoll/console_configs/console_config06.json"))

        og.PyGameRenderAgent = pygame
        og.PyGameDisplay = pygame.surface.Surface
        GAME_FONT = pygame.freetype.Font('rsr\\fonts\\arial.ttf', 24)
        MapSelect('rsr\\map\\' + "proto1" + '.json')
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

        sphere = gluNewQuadric()

        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glLoadIdentity()
    else:
        # Определение размеров окна
        window_width, window_height = 800, 600

        # Инициализация библиотеки GLFW
        if not glfw.init():
            raise Exception("GLFW initialization failed")

        # Создание окна
        window = glfw.create_window(window_width, window_height, "3D Shader Example", None, None)
        glfw.make_context_current(window)
        if not window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")

        frag_shad = shad.shader_reader("rsr\\shaders\\main.frag")
        vert_shad = shad.shader_reader("rsr\\shaders\\main.vert")

        shader_program = compileProgram(vert_shad, frag_shad)

        glUseProgram(shader_program)

        # Создание буфера вершин
        vertices = np.array([
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0
        ], dtype=np.float32)
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)
        ebo = glGenBuffers(1)
        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    if conrine is True:
        # init mouse movement and center mouse on screen
        displayCenter = [scree.get_size()[i] // 2 for i in range(2)]
        mouseMove = [0, 0]
        #pygame.mouse.set_pos(displayCenter)

    paused = False
    run = True
    # главый цикл
    # изминить логику камеры с wasd на перемещение = текущяя позиция - прошлая
    while run:
        if conrine is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        run = False
                    if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                        paused = not paused
                        #pygame.mouse.set_pos(displayCenter)
                if not paused:
                    if event.type == pygame.MOUSEMOTION:
                        mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                        mX, mY = pygame.mouse.get_pos()
                        glTranslatef(cx, cy, cz)

                    # pygame.mouse.set_pos(displayCenter)
                #console.update(pygame.event.get())
        glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)
        up_down_angle += mouseMove[1] * 0.1
        glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        #if keyboard.is_pressed('F1'):
        #    console.toggle(True)


        if not paused:
            # get keys
            keypress = pygame.key.get_pressed()

            # mouseMove = pygame.mouse.get_rel()

            # init model view matrix
            glLoadIdentity()

            # apply the look up and down

            # init the view matrix
            glPushMatrix()
            glLoadIdentity()
            mX, mY = pygame.mouse.get_pos()
        # управление
        _obj_core.main(i)
        mX, mY = pygame.mouse.get_pos()
        CamOBJ = _obj_core.camera_ret()
        if not (CamOBJ is None):
            CamPos = CamOBJ.transform.position
            CamRot = CamOBJ.transform.rotation
            TransVect = CamPos - (last_cam_pos - CamPos)



        text_surface, rect = GAME_FONT.render("Hello World!", (0, 0, 0))
        scree.blit(text_surface, (40, 250))

        # if noclip == False:
        # glTranslatef(0, speed, 0)
        # if main.collider(0, cx, cy, cz) == True:
        #   print("coliders")
        #   glTranslatef(0, - speed, 0)
        # apply the left and right rotation

        # multiply the current matrix by the get the new view matrix and store the final vie matrix
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix

        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # render

        # CPU рендер
        _obj_core.GetRender(i, TransVect)
        last_cam_pos = CamPos
        i = i + 1

        glPushMatrix()

        if conrine == True:
            # end render

            # glColor4f(0.5, 0.2, 0.2, 1)
            # gluSphere(sphere, 1.0, 32, 16)

            # glTranslatef(3, 0, 0)
            # glColor4f(0.2, 0.2, 0.5, 1)
            # gluSphere(sphere, 1.0, 32, 16)

            glPopMatrix()

            pygame.display.flip()

            pygame.time.wait(10)

    pygame.quit()
