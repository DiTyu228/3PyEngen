// Вершинный шейдер (.vert)
#version 330

in vec3 position;

void main()
{
    gl_Position = vec4(position, 1.0f) + vec4(1.0f, 0.0f, 0.0f, 0.0f);
}