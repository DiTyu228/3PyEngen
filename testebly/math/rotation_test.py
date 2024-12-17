import math


def rotate_point(point, axis, angle):
    x, y, z = point
    a, b, c = axis

    # Нормализуем ось вращения
    magnitude = math.sqrt(a ** 2 + b ** 2 + c ** 2)
    a /= magnitude
    b /= magnitude
    c /= magnitude

    # Матрица вращения (формула Родригеса)
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)

    x_rotated = (a * (a * x + b * y + c * z) * (1 - cos_theta) + x * cos_theta + (-c * y + b * z) * sin_theta)
    y_rotated = (b * (a * x + b * y + c * z) * (1 - cos_theta) + y * cos_theta + (c * x - a * z) * sin_theta)
    z_rotated = (c * (a * x + b * y + c * z) * (1 - cos_theta) + z * cos_theta + (-b * x + a * y) * sin_theta)

    return (x_rotated, y_rotated, z_rotated)


def rotate_model(model_points, rotation_vector):
    """Вращает всю 3D модель."""

    # Вектор вращения - это [a,b,c,theta] где [a,b,c] - ось вращения, theta - угол в радианах.

    if len(rotation_vector) != 4:
        raise ValueError("Вектор вращения должен содержать 4 элемента: [a, b, c, theta]")

    axis = rotation_vector[:3]
    angle = rotation_vector[3]

    rotated_model = []
    for point in model_points:
        rotated_point = rotate_point(point, axis, angle)
        rotated_model.append(rotated_point)
    return rotated_model


# Пример использования:

model_points = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 1)
]

# Вектор вращения: ось (1, 0, 0), угол 90 градусов (пи/2 радианов)
rotation_vector = [1, 0, 0, math.pi / 2]

rotated_model = rotate_model(model_points, rotation_vector)
print("Оригинальные точки:", model_points)
print("Вращаемые точки:", rotated_model)

# Пример с другой осью и углом
rotation_vector2 = [0, 1, 0, math.pi / 4]  # Ось (0,1,0), угол 45 градусов
rotated_model2 = rotate_model(model_points, rotation_vector2)
print("Оригинальные точки:", model_points)
print("Вращаемые точки:", rotated_model2)