import m_math as mt
import keyboard


def read_obj_file(file_path):
    vertices = []
    uvs = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex = list(map(float, line.strip().split()[1:]))
                vertices.append(vertex)
            elif line.startswith('vt '):
                uv = list(map(float, line.strip().split()[1:]))
                uvs.append(uv)

    return vertices, uvs


def convert_data_to_engine_format(vertices, uvs):
    engine_data = {'models': [], 'uv': []}

    for vertex, uv in zip(vertices, uvs):
        engine_data['models'].append([vertex[0], vertex[1], vertex[2]])
        engine_data['uv'].append([uv[0], uv[1]])

    return engine_data


# Пример использования
# obj_file_path = 'rsr\\models\\cube.obj'
# vertices, uvs = read_obj_file(obj_file_path)
# engine_data = convert_data_to_engine_format(vertices, uvs)

# print(engine_data)


import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
import mainLib as mL

vertex_shader_source = """
#version 330

in vec3 position;

void main()
{
    gl_Position = vec4(position, 1.0f) + vec4(1.0f, 0.0f, 0.0f, 0.0f);
}
"""

fragment_shader_source = """
#version 330

out vec4 outColor;

void main()
{
    outColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

with open('rsr\\shaders\\main.frag', 'r') as file:
    file_content_one = file.read()
with open('rsr\\shaders\\main.vert', 'r') as file:
    file_content_two = file.read()

def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader
sd_worker = mL.shader_worker()

#frag_s = sd_worker.shader_reader('rsr\\shaders\\main.frag')
#vert_s = sd_worker.shader_reader('rsr\\shaders\\main.vert')

def create_program(vertex_shader, fragment_shader):
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)
    return program


def main():
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
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    print("PyGame init")
    vertex_shader = create_shader(GL_VERTEX_SHADER, file_content_two)
    fragment_shader = create_shader(GL_FRAGMENT_SHADER, file_content_one)
    program = create_program(vertex_shader, fragment_shader)

    vertices = np.array([-0.5, -0.5, 0.0,
                         0.5, -0.5, 0.0,
                         0.0, 0.5, 1.0], dtype=np.float32)
    vertices2 = [[-0.5, -0.5, 0.0, ],
                 [0.5, -0.5, 0.0],
                 [0.0, 1.0, 1.0]]
    #pos = np.array([0.0, 0.0, 0.0], dtype=np.float32)


    VBO = glGenBuffers(1)
    print("VBO init")

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    #glBufferData(GL_ARRAY_BUFFER, pos.nbytes, pos, GL_STATIC_DRAW)
    #CamPos = glGetAttribLocation(program, "CameraPos")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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
        sx = vertices.size
        sam = np.zeros(sx)
        vertices = vertices * (cx, cy, cz, cx, cy, cz, cx, cy, cz)


        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(program)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        #glEnableVertexAttribArray(CamPos)
        #glVertexAttribPointer(CamPos, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, vertices)
        glColorPointer(3, GL_FLOAT, 0, vertices)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        print("Frame draw end")
        pygame.display.flip()


main()
