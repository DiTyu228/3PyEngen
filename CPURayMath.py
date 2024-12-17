import m_math as mt
import math

T = mt.Vector2(6, 3)
A = mt.Vector2(2, 2)
R = 0
l = 3
k = 2


class hit():
    def __init__(self, distans, IsHit, HitPos, len):
        self.distans = mt.Vector3(distans.x, distans.y, distans.z)
        self.IsHit = IsHit
        self.HitPos = mt.Vector3(HitPos.x, HitPos.y, HitPos.z)
        self.len = len


class Ray():
    def __init__(self, A, k, i, r, r2, obj_list):
        self.A = A
        self.L = k * i
        self.r = r
        self.r1 = r2
        self.obj_list = obj_list



    def RayCalculate(self):
        P_mass = []
        P_mass2 = []
        s = 0
        for i in range(len(self.obj_list)):
            P_mass2.append(self.obj_list)
            s += 1
            if s == 3:
                P_mass.append(P_mass2)
                P_mass2 = []
        for CollP in P_mass:
            A = self.A
            L = self.L
            r = self.r
            r2 = self.r1
            B = mt.Vector3(A.x + L * math.cos(math.degrees(r)) * math.sin(math.degrees(r2)),
                           A.y + L * math.sin(math.degrees(r)) * math.sin(math.degrees(r2)),
                           A.z + L * math.cos(math.degrees(r2)))
            x = mt.GetFourPointCollision(B, A, CollP[0], CollP[1], CollP[2], CollP[3])
            IsHit = x.CMPFloatAnyUp(0, 1) and x.CMPFloatAny(0, 2)
            out = hit(x, IsHit, self.obj_list[i], x.GetRetFirstNotNull())
            if IsHit is True:
                return out
        out = hit(B, IsHit, mt.Vector3(0, 0, 0), x.GetRetFirstNotNull())
        return out



