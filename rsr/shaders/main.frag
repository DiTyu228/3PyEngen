// Фрагментный шейдер (.frag)
#version 330 core
in vec2 uv;
out vec4 fragColor;

void main()
{
    // Проверка попадания в заданные координаты
    if (uv.x > 0.3 && uv.x < 0.7 && uv.y > 0.3 && uv.y < 0.7)
    {
        fragColor = vec4(0.0, 1.0, 0.0, 1.0); // Зеленый цвет для попадания
    }
    else
    {
        fragColor = vec4(1.0, 0.0, 0.0, 1.0); // Красный цвет для промаха
    }
}