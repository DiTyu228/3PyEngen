import pydx12
from OpenGL.GL.SUN import vertex
from OpenGL.GL.feedback import Vertex
from OpenGL.arrays import vbo
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import glfw
from OpenGL.GL.shaders import compileShader, compileProgram
from pydx12 import api as DXapi
from pydx12 import CreateDXGIFactory2


import numpy as ny
import pygame
import mainLib



class shader_worker():
    def GetShaderTexture(self, texture_file):
        texture_surface = pygame.image.load(texture_file)
        texture_data = pygame.image.tostring(texture_surface, "RGB", 1)

        # Создание и настройка текстурного объекта
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_surface.get_width(), texture_surface.get_height(), 0,
                     GL_RGB,
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



global mn
global shad
shad = shader_worker()
mn = mainLib.main()
class main():
    def coord_render_GPU(self, textyrs, coords, uv):
        factory = CreateDXGIFactory2()
        DXapi.D3D12_RENDER_TARGET_BLEND_DESC.BlendEnable
        DXapi.D3D10_PRIMITIVE_TOPOLOGY_POINTLIST





