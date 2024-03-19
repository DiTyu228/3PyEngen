import m_math
import random
import time

import pygame
import mouse
import keyboard
import numpy as np
import math
import os
import sys

import mainLib
from MainFrame import __init__ as inint
from MainFrame import GPURenderHelper as GPUhelp
import PyENGPhys
import PyENGPhys as phy
import render_model
from render_model import *
import primitivs.primitiv as pr
import object_core
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
eng_ver = "0.0.1 work in progress"
models = dir + "\\" + resurs + "\\" + "models\\"


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
    module_name = os.path.splitext(script_files[0])[0]
    spec = importlib.util.spec_from_file_location(module_name, os.path.join(scripts_path, script_files[0]))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    dim_scripst = getattr(module, class_name)()
    #запуск медода aweik во всех скриптах
    try:
        dim_scripst.aweik()
    except Exception:
        pass
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
        obj_on_scene = mw.GetMapData('rsr\\map\\' + "proto1" + '.json')
        pygame.init()
        display = (800, 600)
        scree = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

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
        pygame.mouse.set_pos(displayCenter)

    paused = False
    run = True
    try:
        dim_scripst.start()
    except Exception:
        pass
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
                        pygame.mouse.set_pos(displayCenter)
                if not paused:
                    if event.type == pygame.MOUSEMOTION:
                        mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
                    pygame.mouse.set_pos(displayCenter)

        if not paused:

            if conrine is True:
                # get keys
                keypress = pygame.key.get_pressed()
                # mouseMove = pygame.mouse.get_rel()

                # init model view matrix
                glLoadIdentity()

                # apply the look up and down
                up_down_angle += mouseMove[1] * 0.1
                glRotatef(up_down_angle, 1.0, 0.0, 0.0)

                # init the view matrix
                glPushMatrix()
                glLoadIdentity()
        # управление
        if keyboard.is_pressed('esc'):
            quit()
        if keyboard.is_pressed('w'):
            glTranslatef(0, 0, speed)
            cz = cz + speed
        if keyboard.is_pressed('s'):
            glTranslatef(0.0, 0, -speed)
            cz = cz - speed
        if keyboard.is_pressed('a'):
            glTranslatef(speed, 0, 0)
            cy = cy - speed
        if keyboard.is_pressed('d'):
            glTranslatef(-speed, 0, 0)
            cy = cy + speed
        if keyboard.is_pressed('ctrl'):
            glTranslatef(0, speed, 0)
            cx = cx - speed
        if keyboard.is_pressed('space'):
            glTranslatef(0, -speed, 0)
            cx = cx + speed
        if keyboard.is_pressed('v'):
            dppress = True
            noclip = True
            if dppress == True and noclip == True:
                dppress = False
                noclip = False
        mX, mY = mouse.get_position()

        # if noclip == False:
        # glTranslatef(0, speed, 0)
        # if main.collider(0, cx, cy, cz) == True:
        #   print("coliders")
        #   glTranslatef(0, - speed, 0)
        # apply the left and right rotation
        if conrine is True:
            glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)

            # multiply the current matrix by the get the new view matrix and store the final vie matrix
            glMultMatrixf(viewMatrix)
            viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

            # apply view matrix
            glPopMatrix()
            glMultMatrixf(viewMatrix)

            glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
        # render

        # CPU рендер
        if (conrine == True or conrine == True):

            pr = mainLib.primitivs()
            vm = m_math.vectors()
            objW = mainLib.ModelWorker()


            for obj in range(len(obj_on_scene)):
                _objeck = obj_on_scene[obj]
                _type = _objeck['type']


                try:
                    dim_scripst.update()
                except Exception:
                    pass
                if _type == 0:
                    coords = _objeck["models"]
                    uv_coords = _objeck["uv"]
                    textyres = _objeck['tex']
                    xyz = _objeck['xyz']
                    coords = vm.avx_hvsum(coords, xyz)
                    GPUrd.coord_render_GPU(textyres, coords, uv_coords)
                if _type == 1:
                    coords = _objeck["models"]
                    uv_coords = _objeck["uv"]
                    textyres = _objeck['tex']
                    xyz = _objeck['xyz']
                    coords = vm.avx_hvsum(coords, xyz)
                    pr.coord_render_tex(textyres, coords, uv_coords)
                if _type == 2:
                    coords = _objeck["models"]
                    uv_coords = _objeck["uv"]
                    textyres = _objeck['tex']
                    stop_coord = _objeck["stop_dist"]
                    is_looped = _objeck["loop"]
                    xyz = _objeck['xyz']
                    speed_obj = _objeck["speed"]
                    curent_tg = stop_coord
                    dist = vm.vsub(curent_tg, xyz)
                    if xyz[0] <= curent_tg[0]:
                        if dist[0] > 0:
                            xyz = vm.vsum(xyz, [i * (speed_obj / 10), 0, 0])
                        elif dist[0] < 0:
                            xyz = vm.vsub(xyz, [i * (speed_obj / 10), 0, 0])
                    if xyz[1] <= curent_tg[1]:
                        if dist[1] > 0:
                            xyz = vm.vsum(xyz, [0, i * (speed_obj / 10), 0])
                        elif dist[1] < 0:
                            xyz = vm.vsub(xyz, [0, i * (speed_obj / 10), 0])
                    if xyz[2] <= curent_tg[2]:
                        if dist[2] > 0:
                            xyz = vm.vsum(xyz, [0, 0, i * (speed_obj / 10)])
                        elif dist[2] < 0:
                            xyz = vm.vsub(xyz, [0, 0, i * (speed_obj / 10)])
                    coords = vm.avx_hvsum(coords, xyz)
                    pr.coord_render_tex(textyres, coords, uv_coords)
                    _objeck['xyz'] = xyz
                if _type == 3:
                    try:
                        coords = _objeck["models"]
                    except:
                        models = _objeck["model"]
                        coords, uv_coords = objW.GetOBJModel(models)
                    textyres = _objeck['tex']
                    xyz = _objeck['xyz']
                    size = _objeck['size']
                    coords = vm.avx_nmul(coords, size)
                    coords = vm.avx_hvsum(coords, xyz)
                    pr.coord_render_tex(textyres, coords, uv_coords)
                if _type == 4:
                    coords = _objeck["models"]
                    uv_coords = _objeck["uv"]
                    textyres = _objeck['tex']
                    xyz = _objeck['xyz']
                    try:
                        iter = _objeck["i"]
                    except:
                        _objeck["i"] = 0
                        iter = 0
                    try:
                        rev = _objeck["rev"]
                    except:
                        _objeck["rev"] = False
                        rev = False
                    xyz = vm.vsum(xyz, [0, 0, iter])

                    if rev is False:
                        if iter <= 5 and iter >= -5:
                            iter = iter + 0.1
                        else:
                            rev = True
                    if rev is True:
                        if iter > -5:
                            iter = iter - 0.1
                        elif iter < -5:
                            iter = -5
                        else:
                            rev = False
                    coords = vm.avx_hvsum(coords, xyz)
                    pr.coord_render_tex(textyres, coords, uv_coords)
                    _objeck['xyz'] = xyz
                    _objeck["i"] = iter
                    _objeck["rev"] = rev
                if type == 5:
                    name = _objeck["name"]
                    obj_id = _objeck["id"]
                    parametrs = _objeck['pars']
                    keys = []
                    transform = False
                    rendr = False
                    for k in parametrs.keys():
                        if 'transform' in k:
                            transform = True
                        if 'render' in k:
                            rendr = True
                        keys.append(k)
                    if rendr is True:
                        transf = parametrs['render']
                        coords = transf["models"]
                        uv_coords = transf["uv"]
                        textyres = transf['tex']
                    if transform is True:
                        transf = parametrs['transform']
                        xyz = transf['xyz']
                        local_xyz = transf['local_xyz']
                        size = transf['size']
                        coords = vm.avx_hvsum(coords, xyz)
                        coords = vm.avx_hvsum(coords, local_xyz)
                        coords = vm.avx_hvmul(coords, transf)
                    if rendr is True:
                        pr.coord_render_tex(textyres, coords, uv_coords)




            i = i + 1


        else:
            # рандер на шейдере

            # Установка начальных значения входных данных
            cPos = np.array([cx, cy, cz], dtype=np.float32)
            cRot = np.array([mX, mY], dtype=np.float32)
            # Получение индексов uniform-переменных из шейдера
            cPos_loc = glGetUniformLocation(shader_program, "cPos")
            cRot_loc = glGetUniformLocation(shader_program, "cRot")


            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUniform3fv(cPos_loc, 1, cPos)
            glUniform2fv(cRot_loc, 1, cRot)

            # Рендеринг объекта
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            glBindVertexArray(0)

            # Опрос событий и обновление окна
            glfw.poll_events()
            glfw.swap_buffers(window)

            # Обновление входных данных в шейдере
            glUniform3fv(cPos_loc, 1, cPos)
            glUniform2fv(cRot_loc, 1, cRot)

        # obj_core.__init__(vertex)
        # obj_core.draw(texway + 'concreit1.jpg')

        # pl1 = primitivs.plainOntex(texway + 'concreit1.jpg', 0, 0, -1, 0)
        # pl2 = primitivs.plainOntex(texway + 'concreit1.jpg', 0, 0, 5, 0)
        # cube1 = primitivs.CubeOnTextr(texway + 'brick.jpg', 1, 1, 0, 1)

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
