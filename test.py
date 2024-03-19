from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import mainLib as ml
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import glfw


haight = 800
whaid = 600


def create_shader_program():
    sw = ml.shader_worker()
    vertex_shader_id = sw.shader_reader('rsr\\shaders\\main.vert')
    fragment_shader_id = sw.shader_reader('rsr\\shaders\\main.frag')
    shader_program_id = compileProgram(vertex_shader_id, fragment_shader_id)
    return shader_program_id


# Camera variables
camera_position = np.array([0.0, 0.0, 0.0])
camera_rotation = np.array([0.0, 0.0, 0.0])

# Mouse variables
mouse_x = 0
mouse_y = 0


def mouse_motion(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y


def keyboard(key):
    global camera_position
    print(camera_position)
    if key == b'w' or key == b'W':
        camera_position += 0.1 * np.array([0.0, 0.0, -1.0])
    elif key == b's' or key == b'S':
        camera_position += 0.1 * np.array([0.0, 0.0, 1.0])
    elif key == b'a' or key == b'A':
        camera_position += 0.1 * np.array([-1.0, 0.0, 0.0])
    elif key == b'd' or key == b'D':
        camera_position += 0.1 * np.array([1.0, 0.0, 0.0])
    elif key == b'q' or key == b'Q':
        camera_position += 0.1 * np.array([0.0, 1.0, 0.0])
    elif key == b'e' or key == b'E':
        camera_position += 0.1 * np.array([0.0, -1.0, 0.0])


def update_view():
    global camera_position, camera_rotation
    keyboard('w')
    print(camera_position)
    # Set camera rotation based on mouse
    rotation_speed = 0.01
    camera_rotation[0] -= rotation_speed * (mouse_y - haight // 2)
    camera_rotation[1] -= rotation_speed * (mouse_x - whaid // 2)

    # Limit vertical rotation to -90 to 90 degrees
    camera_rotation[0] = np.clip(camera_rotation[0], -np.pi / 2, np.pi / 2)

    # Reset mouse position to center of the window

    # Calculate camera direction
    direction = np.array([
        math.cos(camera_rotation[0]) * math.sin(camera_rotation[1]),
        math.sin(camera_rotation[0]),
        math.cos(camera_rotation[0]) * math.cos(camera_rotation[1])
    ])

    # Set up view matrix
    view_matrix = np.identity(4)
    view_matrix[:3, 3] = -camera_position
    view_matrix[:3, :3] = np.transpose(np.reshape(direction, (3, 1)))

    return view_matrix

def render():
    shader_program_id = create_shader_program()
    program = create_shader_program()

    objects = [
        {"position": np.array([0.0, 0.0, -5.0]), "color": np.array([1.0, 0.0, 0.0])},  # Red sphere
        {"position": np.array([0.0, 0.0, -10.0]), "color": np.array([0.0, 1.0, 0.0])}  # Green sphere
    ]

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set up projection matrix
    projection_matrix = np.identity(4)
    aspect_ratio = haight / whaid
    perspective_matrix = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, -1.0, -2.0],
        [0.0, 0.0, -1.0, 0.0]
    ])
    projection_matrix = np.matmul(perspective_matrix, projection_matrix)
    projection_matrix = np.transpose(np.array([
        [1.0 / (aspect_ratio * math.tan(math.radians(45.0 / 2))), 0.0, 0.0, 0.0],
        [0.0, 1.0 / math.tan(math.radians(45.0 / 2)), 0.0, 0.0],
        [0.0, 0.0, -1.0, -1.0],
        [0.0, 0.0, -2.0, 0.0]
    ]))
    projection_matrix = np.transpose(projection_matrix)

    # Update the view matrix
    view_matrix = update_view()

    # Set up the model matrix
    model_matrix = np.identity(4)

    glUseProgram(shader_program_id)

    # Set uniforms
    ray_origin_location = glGetUniformLocation(shader_program_id, "u_ray_origin")
    glUniform3fv(ray_origin_location, 1, camera_position)

    ray_direction_location = glGetUniformLocation(shader_program_id, "u_ray_direction")
    glUniform3fv(ray_direction_location, 1, np.array([0.0, 0.0, -1.0]))

    max_distance_location = glGetUniformLocation(shader_program_id, "u_max_distance")
    glUniform1f(max_distance_location, 100.0)

    for i in range(len(objects)):
        texture_location = glGetUniformLocation(shader_program_id, "u_texture")
        texture_scale_location = glGetUniformLocation(shader_program_id, "u_texture_scale")

        # Загрузка текстуры

        # Установка uniform-переменных для объектов
        object_positions_location = glGetUniformLocation(shader_program_id, "objects[0].position")
        object_colors_location = glGetUniformLocation(shader_program_id, "objects[0].color")
        object_reflectivity_location = glGetUniformLocation(shader_program_id, "objects[0].reflectivity")
        object_material_type_location = glGetUniformLocation(shader_program_id, "objects[0].material_type")

    # Render a quad
    glBegin(GL_QUADS)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glEnd()




    glfw.poll_events()
    glfw.swap_buffers(window)

    #glutSwapBuffers()


if not glfw.init():
    raise Exception("GLFW initialization failed")

# Initialize OpenGL and create a window
window = glfw.create_window(haight, whaid, "3D Shader Example", None, None)
glfw.make_context_current(window)
if not window:
    glfw.terminate()
    raise Exception("Failed to create GLFW window")

# Create the shader program
shader_program_id = create_shader_program()

# Set up OpenGL
glEnable(GL_DEPTH_TEST)
glClearColor(0.0, 0.0, 0.0, 1.0)

# Set up the rendering function
#glfw.set_key_callback(window, render)

# Start the main loop
while not glfw.window_should_close(window):
    render()
