import m_math
import pygame
import keyboard
import numpy as np
import math
import os

import render_model
from render_model import *

from OpenGL.GL.SUN import vertex
from OpenGL.GL.feedback import Vertex
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class matricx():
    def scale_matrix(self,sx, sy, sz):
        # Создаем матрицу масштабирования для объекта
        scale_matrix = np.identity(4)
        scale_matrix[0][0] = sx  # масштаб по оси X
        scale_matrix[1][1] = sy  # масштаб по оси Y
        scale_matrix[2][2] = sz  # масштаб по оси Z
    def translete_matricks(self, x, y, z):
        translation_matrix = np.identity(4)
        translation_matrix[0][3] = x  # смещение по оси X
        translation_matrix[1][3] = y  # смещение по оси Y
        translation_matrix[2][3] = z  # смещение по оси Z
        return translation_matrix
    def rotation_matrix(theta, x, y, z):
        c = math.cos(theta)
        s = math.sin(theta)
        norm = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        x /= norm
        y /= norm
        z /= norm
        return np.array([[x * x * (1 - c) + c, x * y * (1 - c) - z * s, x * z * (1 - c) + y * s, 0],
                         [y * x * (1 - c) + z * s, y * y * (1 - c) + c, y * z * (1 - c) - x * s, 0],
                         [x * z * (1 - c) - y * s, y * z * (1 - c) + x * s, z * z * (1 - c) + c, 0],
                         [0, 0, 0, 1]])
class main:
    def loadTexture(imgr):
        textureSurface = pygame.image.load(imgr)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
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

class plain():
    def __init__(self):
        self.transform_matrix = np.identity(4)
        self.transform_rotation = np.identity(4)
        self.transform_scale = np.identity(4)

    def load(self, imgr):

        main.loadTexture(imgr)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-10, -10, 0 )
        glTexCoord2f(1.0, 0.0)
        glVertex3f(10, -10, 0 )
        glTexCoord2f(1.0, 1.0)
        glVertex3f(10, 10, 0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-10, 10, 0)
        glEnd()

    def apply_matrics(self, matrix):
        self.transform_matrix = np.dot(self.transform_matrix, matrix)
        self.transform_rotation = np.dot(self.transform_rotation, matrix)
        self.transform_scale = np.dot(self.transform_scale, matrix)
    def apply_rotation(self, matrix):
        self.transform_rotation = np.dot(self.transform_rotation, matrix)
    def apply_transform(self, matrix):
        self.transform_matrix = np.dot(self.transform_matrix, matrix)
    def apply_scale(self, matrix):
        self.transform_scale = np.dot(self.transform_scale, matrix)
    def update_object_position(self, idx, matrix):

        glLoadIdentity()
        glMultMatrixf(matrix)
