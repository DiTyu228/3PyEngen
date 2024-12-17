import m_math as mt
import math

T = mt.Vector3(2, 2, 5)
A = mt.Vector3(2, 2, 2)
R = 0
R1 = 0
l = 3
k = 2


def RayCalculate(A, k, i, r, r2):
    global T
    A = mt.Vector3(A.x, A.y, A.z)
    L = k * i
    B = mt.Vector3(A.x + L * math.cos(math.degrees(r)) * math.sin(math.degrees(r2)),
                   A.y + L * math.sin(math.degrees(r)) * math.sin(math.degrees(r2)),
                   A.z + L * math.cos(math.degrees(r2)))
    print(B)
    return mt.Vector3(mt.Diapos_SMP(A.x, B.x, T.x), mt.Diapos_SMP(A.y, B.y, T.y), mt.Diapos_SMP(A.z, B.z, T.z))


print(RayCalculate(A, k, l, R, R1))
