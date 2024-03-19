import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtWidgets import QOpenGLWidget


class MyGLObject:
    def __init__(self, vertices, colors):
        self.vertices = vertices
        self.colors = colors
        self.transform_matrix = np.identity(4)

    def draw(self):
        glPushMatrix()
        glMultMatrixf(self.transform_matrix)
        glBegin(GL_QUADS)
        for i in range(len(self.vertices)):
            glColor3fv(self.colors[i])
            glVertex3fv(self.vertices[i])
        glEnd()
        glPopMatrix()

    def apply_transform(self, matrix):
        self.transform_matrix = np.dot(self.transform_matrix, matrix)


class MyGLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.objects = []

    def initializeGL(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width()/self.height(), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        for obj in self.objects:
            obj.draw()

    def update_object_position(self, idx, matrix):
        self.objects[idx].apply_transform(matrix)

if __name__ == '__main__':
    # создаем куб
    vertices = [
        [-1.0, -1.0, 1.0],
        [1.0, -1.0, 1.0],
        [1.0, 1.0, 1.0],
        [-1.0, 1.0, 1.0]
    ]

    colors = [
        [0.5, 0.5, 1.0],
        [0.5, 0.5, 1.0],
        [0.5, 0.5, 1.0],
        [0.5, 0.5, 1.0]
    ]

    cube = MyGLObject(vertices, colors)

    # добавляем куб в список объектов
    widget = MyGLWidget()
    widget.objects.append(cube)

    # перемещаем куб вправо на 2 единицы
    translation_matrix = np.array([[1, 0, 0, 2], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    widget.update_object_position(0, translation_matrix)