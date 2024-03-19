import math
import random
import time

import pygame
import keyboard
import numpy as ny
import m_math
import os

import PyENGPhys
import PyENGPhys as phy
import render_model
from render_model import *
import primitivs.primitiv as pr
import object_core

from OpenGL.GL.SUN import vertex
from OpenGL.GL.feedback import Vertex
from OpenGL.arrays import vbo
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw
from OpenGL.GL.shaders import compileShader, compileProgram
import json


resurs = "rsr\\"
textur = "material\\"
dir = os.getcwd()


def write_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


def read_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


class shader_worker():
    def GetShaderTexture(self, texture_file):
        texture_surface = pygame.image.load(texture_file)
        texture_data = pygame.image.tostring(texture_surface, "RGB", 1)

        # Создание и настройка текстурного объекта
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_surface.get_width(), texture_surface.get_height(), 0, GL_RGB,
                     GL_UNSIGNED_BYTE, texture_data)

    def shader_reader(self, shad_file):
        # импортируем этот же класс
        sw = shader_worker()
        # Определение расширения файла
        file_extension = os.path.splitext(shad_file)[1]
        shader_type = 0
        # Чтение содержимого файла
        with open(shad_file, 'r') as file:
            file_content = file.read()
        # Обработка содержимого файла в зависимости от расширения
        if file_extension == '.vert':
            # Обработка файла вершинного шейдера
            shader_type = GL_VERTEX_SHADER
        elif file_extension == '.tesc':
            # Обработка файла шейдера управления тесселяцией
            shader_type = GL_TESS_CONTROL_SHADER
        elif file_extension == '.tese':
            # Обработка файла шейдера оценки тесселяции
            shader_type = GL_TESS_EVALUATION_SHADER
        elif file_extension == '.geom':
            # Обработка файла геометрического шейдера
            shader_type = GL_GEOMETRY_SHADER
        elif file_extension == '.frag':
            # Обработка файла фрагментного шейдера
            shader_type = GL_FRAGMENT_SHADER
        elif file_extension == '.comp':
            # Обработка файла шейдера вычислений
            shader_type = GL_COMPUTE_SHADER
        else:
            shader_type = "ERROR"

        shader = sw.shader_creator(shader_type, file_content)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            raise RuntimeError(f"Shader compilation error hihihaha: {glGetShaderInfoLog(shader)}")
        return shader



    def shader_creator(self, type, source):
        # Создаем пустой объект шейдера
        shader = glCreateShader(type)
        glShaderSource(shader, source)
        # Компилируем шейдер
        glCompileShader(shader)
        return shader
# noinspection PyUnresolvedReferences




class particleSystem(object):
     def __init__(self, len=1, args=None, kwargs=None):
         self.length = len
         self.cparticles = [0.0] * 7 * len
         self.nparticles = [0.0] * 7 * len
         self.index = 0
         self.center = 0.0, 0.0
         self.currenttime = 0.0
         self.height = 2.0
         self.init1()
         self.createVAO()
     def init1(self) -> None:
         #pos(x,y,z),vel(x,y,z),time
         for i in range(self.length):
             ind = i * 7
             px,py,pz,tt = ind,ind + 1,ind + 2,ind + 6
             vx,vy,vz = ind + 3,ind + 4,ind + 5
             self.cparticles[px] = 0.0
             self.cparticles[py] = 3.0
             self.cparticles[pz] = random.uniform(0, 5)
             self.cparticles[vx] = random.random()
             self.cparticles[vy] = 0.0
             self.cparticles[vz] = 0.0
             self.cparticles[tt] = random.uniform(1.0, 40.0)#random.uniform(0, 3 * this.height)
     def createVAO(self):
         self.currvbo = vbo.VBO(ny.array(self.cparticles, 'f'))
         self.nextvbo = vbo.VBO(ny.array(self.nparticles, 'f'))
     def render(self,program):
         ind = self.index % 2
         span = time.time() - self.currenttime if self.currenttime != 0.0 else 0.0
         invbo,outvbo = (self.currvbo, self.nextvbo) if ind == 0 else (self.nextvbo, self.currvbo)
        #gpu compute.
         print (span)
         glUseProgram(program)
         glUniform1f(program.span, span)
         glUniform1f(program.live, 40)
         self.update(invbo, outvbo)
         glUseProgram(0)
         #draw particle.
         glColor(0.5,0.8,0.9)
         glPointSize(3.0)
         outvbo.bind()
         glVertexPointer(3,GL_FLOAT,28,outvbo)
         glDrawArrays(GL_POINTS, 0, self.length)
         outvbo.unbind()
         self.index = self.index + 1
         self.currenttime = time.time()
     def update(se,fvbo,svbo):
         #fvbo->shader(GPU)->svbo,should svbo and fvbo both bind.
         svbo.bind()
         fvbo.bind()
         glEnableVertexAttribArray(0)
         glEnableVertexAttribArray(1)
         glEnableVertexAttribArray(2)
         glVertexAttribPointer(0,3,GL_FLOAT,False,4 * 7,fvbo)
         glVertexAttribPointer(1,3,GL_FLOAT,False,4 * 7,fvbo + 12)
         glVertexAttribPointer(2,1,GL_FLOAT,False,4 * 7,fvbo + 24)
         glEnable(GL_RASTERIZER_DISCARD)
         glBindBufferBase(GL_TRANSFORM_FEEDBACK_BUFFER,0,svbo)
         glBeginTransformFeedback(GL_POINTS)
         glDrawArrays(GL_POINTS, 0, se.length)
         glEndTransformFeedback()
         glDisable(GL_RASTERIZER_DISCARD)
         glDisableVertexAttribArray(0)
         glDisableVertexAttribArray(1)
         glDisableVertexAttribArray(2)
         fvbo.unbind()         #query gpu data is chage?         #svbo.bind()         #bf = glMapBuffer(GL_ARRAY_BUFFER,GL_READ_WRITE)
        #pointv = ctypes.cast(bf, ctypes.POINTER(ctypes.c_float))
         #arrayv = ny.ctypeslib.as_array(pointv,(70,))
         #print "tfv",arrayv
        #glUnmapBuffer(GL_ARRAY_BUFFER)




class main():
 def modelParser(self,file):
     vertices = []
     uvs = []

     with open(file, 'r') as file:
         lines = file.readlines()

         for line in lines:
             if line.startswith('v '):
                 _, x, y, z = line.split()
                 vertices.append((float(x), float(y), float(z)))
             elif line.startswith('vt '):
                 _, u, v = line.split()
                 uvs.append((float(u), float(v)))

     return vertices, uvs

 def renderPoint(self, x, y, z, UV0, UV1):
     glVertex3f(x, y, z)
     glTexCoord2f(UV0, UV1)

 def process_data3(self, data):
     result = ""

     for point in data:
         x, y, z = point
         result += f"{x}, {y}, {z}\n"
         return result
 def model_loader(self, file, x, y, z):
     mn = main()
     cord, uvs = mn.modelParser(file)
     i = 0
     data_cord = 0
     uv = 0
     while True:


         if not(i > len(uvs) - 1):
             uv = uvs[i]
         data_cord = cord[i]
         x, y, z = data_cord
         uv0, uv1 = uv
         mn.renderPoint(x, y, z, uv0, uv1)
         if i == len(cord) - 1:
             i  = 0
             break
         i = i + 1
 def move(self, mx,my, mz,cx,cy,cz):
    return [mx + cx, my + cy, mz + cz]
 def collider(self, Cx, Cy, Cz):
     NposX = 1
     Nposy = 1
     NposZ = -2

     SposX = 2
     Sposy = 2
     Sposz = -2

     WposX = 1
     Wposy = 2
     Wposz = -2

     posX = 2
     posy = 1
     posz = -2

     Ni = False
     Yi = False
     Zi = False

     NNi = False
     NYi = False
     NZi = False
     if Cx < SposX and Cx < WposX:
         NNi = True
     else:
         NNi = False
     if Cy <= Sposy and Cy <= Wposy:
         NYi = True
     else:
         NYi = False
     if Cz <= Sposz and Cz <= Wposy:
         NZi = True
     else:
         NZi = False
     if Cx <= posX and Cx <= NposX:
         Ni = True
     else:
         Ni = False
     if Cy <= posy and Cy <= Nposy:
         Yi = True
     else:
         Yi = False
     if Cz <= posz and Cz <= Nposy:
         Zi = True
     else:
        Zi = False
     if Ni == True and Yi == True and Zi == True and NNi == True and NYi == True and NZi == True:
         return True
     else:
         return False
 def loadpak(i):
     resurs = "\\rsr\\"
     way = dir + resurs + "GMinfo"
     if os.path.exists(way):
      file = open(way, "r", encoding="UTF8")

      while True:
         code = file.readline(500)
         mode = "all"
         if code.startswith("tes"):
             info = code.replace("tes", "")
             info2 = info.replace(" ", "")
             tesxpak = info2

         if code.startswith("mode"):
             info = code.replace("mode" and " ", "")

             if info.startswith("all"):
                 mode = "all"
             if info.startswith("png"):
                 mode = "png"
             if info.startswith("jpg"):
                 mode = "jpg"
         if code.startswith("end"):
             file.close()
             out = tesxpak + ";" + mode
             return out
             break
     else:
         print("game info not load")
         return ""

 def GetPos (vertex, leng):
    x, y, z = 0,0,0
    i = 0
    verte_ = vertex
    l = leng
    while i <= l:
        i = i + 1
        if i == 0:
            x = verte_[0]
            y = verte_[1]
            z = verte_[2]
            return  x, y, z
        else:
            x = verte_[i + 3]
            y = verte_[i + 4]
            z = verte_[i + 5]
            return x, y, z


 def openOBJ(self, filename):
    x, y, z, = 0, 0, 0
    vertex, faces = [], []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith('v '):
                print(line)
                vertex.append([float(i) for i in line.split()[1:]] + [1])
                print(vertex)
            elif line.startswith('vt '):
                break
            #elif line.startswith('f '):
            #    faces_ = ""
            #    faces_ = line.split()[1:]
            #    faces2 = line
            #    faces.append([int(faces2.split('/')[0]) - 1 for faces_ in faces])


            return x, y, z

 def render(vertex, edges, lengV):
    glBegin(GL_QUADS)
    for edge in edges:

            x, y, z = main.GetPos(vertex, lengV)
            glVertex3f(x, y, z)

    glEnd()



 def loadTexture(self, imgr):
    textureSurface = pygame.image.load(imgr)
    textureData = pygame.image.tostring(textureSurface,"RGBA",1)
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    return texid




class primitivs():
    def coord_render_tex(self, textyrs, coords, uv):
        main.loadTexture(self, textyrs)
        glBegin(GL_QUADS)
        for i in range(len(coords)):
            coord_data = coords[i]
            uv_data = uv[i]
            glTexCoord2f(float(uv_data[0]), float(uv_data[1]))
            glVertex3f(float(coord_data[0]), float(coord_data[1]), float(coord_data[2]))
        glEnd()

    def sheder_coord_render_tex(self, textyrs, coords, uv, vert_sheder, frag_sheder):
        print("Test shader render")
        print("Sheder Bild")
        shader_vert = shader_worker.shader_reader(self, vert_sheder)  # Замените "shader_file_path" на путь к вашему файлу шейдера
        shader_vert = shader_worker.shader_reader(self, frag_sheder)
        print("Shedrs bild complit")
        print("Texture bild")
        texture_id = main.loadTexture(self, textyrs)
        print("texture bild complit")
        print("Sheder bake")
        shader = compileProgram(shader_vert, shader_vert)
        print("Sheder baking")
        glUseProgram(shader)

        glBindTexture(GL_TEXTURE_2D, texture_id)
        glUniform1i(glGetUniformLocation(shader, "tex"), 0)

        for i in range(len(coords)):
            coord_data = coords[i]
            uv_data = uv[i]

            glUniform3f(glGetUniformLocation(shader, "position"), float(coord_data[0]), float(coord_data[1]),
                        float(coord_data[2]))
            glUniform2f(glGetUniformLocation(shader, "uv"), float(uv_data[0]), float(uv_data[1]))

            # Здесь необходимо выполнить отрисовку вашего объекта

        glUseProgram(0)


    def plainOntex(textyrs, x, y, z, w):
        main.loadTexture(textyrs)
        if w >= 2:
            w = 0
        if w == 0:
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10 + x, -10 + y, 0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(10 + x, -10 + y, 0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(10 + x, 10 + y, + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10 + x, 10 + y, 0 + z)
            glEnd()
        if w == 1:
            glBegin(GL_QUADS)
            #1
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-10 + x, -10 - y, 0 + z)
            #2
            glTexCoord2f(1.0, 0.0)
            glVertex3f(10 - x, -10 - y, 0 - z)
            #3
            glTexCoord2f(1.0, 1.0)
            glVertex3f(10 - x, 10 + y, 0 - z)
            #4
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-10 + x, 10 + y, 0 + z)
            glEnd()

    def CubeOnTextr(textyrs, x, y, z, w):
        if w <= 2:
            w = 0

        main.loadTexture(textyrs)
        if w == 0:
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(-1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(-1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-1.0 + x, 1.0 + y, -1.0 + z)
            glEnd()

        if w == 1:
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(1.0 - x, -1.0 - y, 1.0 - z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-1.0 - x, 1.0 - y, 1.0 - z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(-1.0 - x, 1.0 - y, -1.0 - z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(1.0 - x, -1.0 - y, -1.0 - z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-1.0 - x, 1.0 - y, -1.0 - z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0 + x, 1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(1.0 - x, 1.0 - y, 1.0 - z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(-1.0 - x, -1.0 - y, -1.0 - z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(1.0 + x, -1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(1.0 - x, -1.0 - y, 1.0 - z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(1.0 - x, -1.0 - y, -1.0 - z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(1.0 + x, 1.0 + y, -1.0 + z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(1.0 - x, 1.0 - y, 1.0 - z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(0.0, 0.0)
            glVertex3f(-1.0 - x, -1.0 - y, -1.0 - z)
            glTexCoord2f(1.0, 0.0)
            glVertex3f(-1.0 + x, -1.0 + y, 1.0 + z)
            glTexCoord2f(1.0, 1.0)
            glVertex3f(-1.0 - x, 1.0 - y, 1.0 - z)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(-1.0 + x, 1.0 + y, -1.0 + z)
            glEnd()
def MapLoad(filename):
     x, y, z, w = 0
     texway = main.loadpak(0)
     if os.path.exists(filename):
        with (filename,"r") as info:
            for line in info:
                if line.startswith("create"):
                    if line.startswith("create cube"):
                      primitivs.CubeOnTextr(texway, z,y,z,w)

     else:
         print("map: " + filename + " not found")

class MapWorker():
    def GetMapData(self, map):
        data = read_from_json(map)
        print("")
        print("Map load satisfy!")
        print("")
        print("Object count on map: " + str(len(data)))
        return data
    def SetMapData(self, map, scene):
        write_to_json(scene, 'rsr\\map\\' + str(map) + '.json')

class ModelWorker():
    def GetOBJModel(self, path):
        coords = []
        uv = []
        with open(path, 'r') as file:
            data = file.readline(500000)
            for line in file:
                if line.startswith("v "):
                    cr = line.split(" ")
                    coords.append([float(cr[1]), float(cr[2]), float(cr[3])])
                if line.startswith("vt "):
                    cv = line.split(" ")
                    cv[1] = float(cv[1])
                    if cv[1] >= 0.5:
                        cv[1] = 0
                    else:
                        cv[1] = 1
                    cv[2] = float(cv[2])
                    if cv[2] >= 5:
                        cv[2] = 0
                    else:
                        cv[2] = 1
                    uv.append([float(cv[1]), float(cv[2])])
        return coords, uv

    def parse_model_file(self, file_path):

            result = {
                "models": [],
                "uv": []
            }

            with open(file_path, 'r') as file:
                for line in file:
                    data = line.strip().split()

                    if data[0] == 'v':
                        x, y, z = map(float, data[1:4])
                        result["models"].append([x, y, z])
                    elif data[0] == 'vt':
                        u, v = map(float, data[1:3])
                        result["uv"].append([u, v])

            return result["models"], result["uv"]

if __name__ == '__main__':
    objw = ModelWorker()
    print(objw.parse_model_file('rsr\\models\\cube.obj'))
