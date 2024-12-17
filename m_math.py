import math
import random as rd
import numpy as np

pi = math.pi

class vectors():

    def vsum(self, vect1, vect2):
        data_out = []
        len_vect = 0
        if len(vect1) < len(vect2):
            len_vect = len(vect1)
        else:
            len_vect = len(vect2)
        for i in range(len_vect):
            data_out.append(vect1[i] + vect2[i])

        return data_out

    def nsum(self, vect, num):
        data_out = []
        len_vect = 0
        len_vect = len(vect)
        for i in range(len_vect):
            data_out.append(vect[i] + num)

        return data_out

    def avx_vsum(self, vectlib):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            if j + 1 <= len_vect:
                vect2 = vectlib[j]
            else:
                vect2 = vect1
            if len(vect1) < len(vect2):
                len_vect2 = len(vect1)
            else:
                len_vect2 = len(vect2)
            for i in range(len_vect2):
                data_out.append(vect1[i] + vect2[i])
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def avx_nsum(self, vectlib, num):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            len_vect2 = len(vect1)
            for i in range(len_vect2):
                data_out.append(vect1[i] + num)
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def avx_hvsum(self, vectlib, vect):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            vect2 = vect
            data_out.append(vectors.vsum(self, vect1, vect2))
            data_out2.append(data_out)

        return data_out

    def vsub(self, vect1, vect2):
        data_out = []
        len_vect = 0
        if len(vect1) < len(vect2):
            len_vect = len(vect1)
        else:
            len_vect = len(vect2)
        for i in range(len_vect):
            data_out.append(vect1[i] - vect2[i])

        return data_out

    def nsub(self, vect, num):
        data_out = []
        len_vect = 0
        len_vect = len(vect)
        for i in range(len_vect):
            data_out.append(vect[i] - num)

        return data_out

    def avx_vsub(self, vectlib):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            if j + 1 <= len_vect:
                vect2 = vectlib[j]
            else:
                vect2 = vect1
            if len(vect1) < len(vect2):
                len_vect2 = len(vect1)
            else:
                len_vect2 = len(vect2)
            for i in range(len_vect2):
                data_out.append(vect1[i] - vect2[i])
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def avx_nsub(self, vectlib, num):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            len_vect2 = len(vect1)
            for i in range(len_vect2):
                data_out.append(vect1[i] - num)
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def avx_hvsub(self, vectlib, vect):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            vect2 = vect
            data_out.append(vectors.vsub(self, vect1, vect2))
            data_out2.append(data_out)

        return data_out

    def vmul(self, vect1, vect2):
        data_out = []
        len_vect = 0
        if len(vect1) < len(vect2):
            len_vect = len(vect1)
        else:
            len_vect = len(vect2)
        for i in range(len_vect):
            data_out.append(vect1[i] * vect2[i])

        return data_out

    def nmul(self, vect, num):
        data_out = []
        len_vect = 0
        len_vect = len(vect)
        for i in range(len_vect):
            data_out.append(vect[i] * num)

        return data_out

    def avx_vmul(self, vectlib):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            if j + 1 <= len_vect:
                vect2 = vectlib[j]
            else:
                vect2 = vect1
            if len(vect1) < len(vect2):
                len_vect2 = len(vect1)
            else:
                len_vect2 = len(vect2)
            for i in range(len_vect2):
                data_out.append(vect1[i] * vect2[i])
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def avx_hvmul(self, vectlib, vect):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            vect2 = vect
            data_out.append(vectors.vmul(self, vect1, vect2))
            data_out2.append(data_out)

        return data_out

    def avx_nmul(self, vectlib, num):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            len_vect2 = len(vect1)
            for i in range(len_vect2):
                data_out.append(vect1[i] * num)
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def vdiv(self, vect1, vect2):
        data_out = []
        len_vect = 0
        if len(vect1) < len(vect2):
            len_vect = len(vect1)
        else:
            len_vect = len(vect2)
        for i in range(len_vect):
            data_out.append(vect1[i] / vect2[i])

        return data_out

    def ndiv(self, vect, num):
        data_out = []
        len_vect = 0
        len_vect = len(vect)
        for i in range(len_vect):
            data_out.append(vect[i] / num)

        return data_out

    def avx_vdiv(self, vectlib):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            if j + 1 <= len_vect:
                vect2 = vectlib[j]
            else:
                vect2 = vect1
            if len(vect1) < len(vect2):
                len_vect2 = len(vect1)
            else:
                len_vect2 = len(vect2)
            for i in range(len_vect2):
                data_out.append(vect1[i] / vect2[i])
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def avx_ndiv(self, vectlib, num):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            len_vect2 = len(vect1)
            for i in range(len_vect2):
                data_out.append(vect1[i] / num)
            data_out2.append(data_out)
            data_out = []

        return data_out2

    def avx_hvdiv(self, vectlib, vect):
        data_out = []
        data_out2 = []
        len_vect = len(vectlib)
        for j in range(len_vect):
            vect1 = vectlib[j]
            vect2 = vect
            data_out.append(vectors.vdiv(self, vect1, vect2))
            data_out2.append(data_out)
            data_out = []

        return data_out

    def num_model(self, num):
        num = float(num)
        if num < 0:
            return num - (num * 2)
        else:
            return num

    def vect_model(self, vect):
        vm = vectors()
        for i in range(len(vect)):
            vect[i] = vm.num_model(vect[i])

    def vect_sip(self, vect1, vect2):
        isTrue = True
        for i in range(len(vect1)):
            if vect1[i] == vect2[i] and isTrue is True:
                isTrue = True
            else:
                isTrue = False

        return isTrue

    def rotate_point(self, point, axis, angle):
        x = point[0]
        y = point[1]
        z = point[2]
        a = axis[0]
        b = axis[1]
        c = axis[2]

        magnitude = math.sqrt(a ** 2 + b ** 2 + c ** 2)

        if magnitude == 0:
            return point

        a /= magnitude
        b /= magnitude
        c /= magnitude


        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)

        x_rotated = (a * (a * x + b * y + c * z) * (1 - cos_theta) + x * cos_theta + (-c * y + b * z) * sin_theta)
        y_rotated = (b * (a * x + b * y + c * z) * (1 - cos_theta) + y * cos_theta + (c * x - a * z) * sin_theta)
        z_rotated = (c * (a * x + b * y + c * z) * (1 - cos_theta) + z * cos_theta + (-b * x + a * y) * sin_theta)
        return (x_rotated, y_rotated, z_rotated)

    def rotate_model(self, model_points, rotation_vector):
        if len(rotation_vector) != 4:
            return model_points

        axis = rotation_vector[:3]
        angle = rotation_vector[3]

        rotated_model = []
        for point in model_points:
            rotated_point = self.rotate_point(point, axis, angle)
            rotated_model.append(rotated_point)
        return rotated_model


class Vector4():

    def __init__(self, _x, _y, _z, _w):
        self.x = float(_x)
        self.y = float(_x)
        self.z = float(_z)
        self.w = float(_w)
        self.Vector = np.array([float(_x), float(_y), float(_z), float(_w)])

    def __add__(self, other):
        self.Vector = self.Vector + other.Vector
        self.x = self.Vector[0]
        self.y = self.Vector[1]
        self.z = self.Vector[2]
        self.w = self.Vector[3]
        return Vector4(self.x, self.y, self.z, self.w)

    def __len__(self):
        return len(self.Vector)

    def __getitem__(self, item):
        return self.Vector[item]

    def __sub__(self, other):
        self.Vector = self.Vector - other.Vector
        self.x = self.Vector[0]
        self.y = self.Vector[1]
        self.z = self.Vector[2]
        self.w = self.Vector[3]
        return Vector4(self.x, self.y, self.z, self.w)

    def __mul__(self, other):
        self.Vector = self.Vector * other.Vector
        self.x = self.Vector[0]
        self.y = self.Vector[1]
        self.z = self.Vector[2]
        self.w = self.Vector[3]
        return Vector4(self.x, self.y, self.z, self.w)

    def __divmod__(self, other):
        self.Vector = self.Vector / other.Vector
        self.x = self.Vector[0]
        self.y = self.Vector[1]
        self.z = self.Vector[2]
        self.w = self.Vector[3]
        return Vector4(self.x, self.y, self.z, self.w)

    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.z) + " " + str(self.w)

    def __cmp__(self, other):
        if self.x == other.x:
            if self.y == other.y:
                if self.z == self.z:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def CMPFloatAny(self, CMP_num, CMP_Allowed_num):
        CMPs = 0
        for i in range(2):
            if self[i] == CMP_num:
                CMPs += 1

        if CMPs == CMP_Allowed_num:
            return True
        else:
            return False

    def CMPFloatAnyUp(self, CMP_num, CMP_Allowed_num):
        CMPs = 0
        for i in range(2):
            if self[i] > CMP_num:
                CMPs += 1

        if CMPs == CMP_Allowed_num:
            return True
        else:
            return False

    def CMPFloatAnyDown(self, CMP_num, CMP_Allowed_num):
        CMPs = 0
        for i in range(2):
            if self[i] < CMP_num:
                CMPs += 1

        if CMPs == CMP_Allowed_num:
            return True
        else:
            return False

    def GetRetFirstNotNull(self):
        for i in range(2):
            if not (self[i] == 0):
                return self[i]


class Vector3():

    def __init__(self, _x, _y, _z):
        self.x = float(_x)
        self.y = float(_y)
        self.z = float(_z)
        self.Vector = [self.x, self.y, self.z]

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        self.Vector = [self.x, self.y, self.z]
        return Vector3(x, y, z)

    def __len__(self):
        self.Vector = [self.x, self.y, self.z]
        return len(self.Vector)

    def __getitem__(self, item):
        self.Vector = [self.x, self.y, self.z]
        return self.Vector[item]

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        self.Vector = [self.x, self.y, self.z]
        return Vector3(x, y, z)

    def __mul__(self, other):
        x = other.x * self.x
        y = other.y * self.y
        z = other.z * self.z
        self.Vector = [self.x, self.y, self.z]
        return Vector3(x, y, z)

    def __str__(self):
        self.Vector = [self.x, self.y, self.z]
        return str(self.x) + " " + str(self.y) + " " + str(self.z)

    def __cmp__(self, other):
        if self.x == other.x:
            if self.y == other.y:
                if self.z == self.z:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def CMPFloatAny(self, CMP_num, CMP_Allowed_num):
        CMPs = 0
        for i in range(2):
            if self[i] == CMP_num:
                CMPs += 1

        if CMPs == CMP_Allowed_num:
            return True
        else:
            return False

    def CMPFloatAnyUp(self, CMP_num, CMP_Allowed_num):
        CMPs = 0
        for i in range(2):
            if self[i] > CMP_num:
                CMPs += 1

        if CMPs == CMP_Allowed_num:
            return True
        else:
            return False

    def CMPFloatAnyDown(self, CMP_num, CMP_Allowed_num):
        CMPs = 0
        for i in range(2):
            if self[i] < CMP_num:
                CMPs += 1

        if CMPs == CMP_Allowed_num:
            return True
        else:
            return False

    def GetRetFirstNotNull(self):
        for i in range(2):
            if not (self[i] == 0):
                return self[i]


class Vector2():

    def __init__(self, _x, _y, ):
        self.x = float(_x)
        self.y = float(_y)
        self.Vector = [self.x, self.y]

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        self.Vector = [self.x, self.y]
        return Vector2(x, y)

    def __len__(self):
        self.Vector = [self.x, self.y]
        return len(self.Vector)

    def __getitem__(self, item):
        self.Vector = [self.x, self.y]
        return self.Vector[item]

    def __sub__(self, other):
        x = other.x - self.x
        y = other.y - self.y
        self.Vector = [self.x, self.y]
        return Vector2(x, y)

    def __mul__(self, other):
        x = other.x * self.x
        y = other.y * self.y
        self.Vector = [self.x, self.y]
        return Vector2(x, y)

    def __str__(self):
        self.Vector = [self.x, self.y]
        return str(self.x) + " " + str(self.y)


def Diapos_SMP(min, max, inpt):
    a = inpt - min
    if a > max - min:
        return max - inpt
    else:
        return a


def GetFourPointCollision(ray_origin, ray_direction, p1, p2, p3, p4):
    plane_normal = (p2 - p1).cross(p3 - p1)

    # Calculate ray-plane intersection
    denom = plane_normal.dot(ray_direction)
    if abs(denom) > 1e-6:  # To avoid division by zero
        t = (plane_normal.dot(p1 - ray_origin)) / denom
        hit_point = ray_origin + t * ray_direction

        # Check if hit_point is within the bounds of the plane defined by p1, p2, p3, p4
        # Implement logic to check if hit_point is inside the polygon formed by p1, p2, p3, p4

        # For simplicity, assuming hit is always true if the ray intersects the plane
        return hit_point
    else:
        return Vector3(0, 0, 0)


if __name__ == '__main__':
    print(Diapos_SMP(2, 2, 3), Diapos_SMP(2, 2, 2), Diapos_SMP(2, 8, 5))
