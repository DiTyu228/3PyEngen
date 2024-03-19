import math


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


class Vector3():
    x = 0
    y = 0
    z = 0

    def __init__(self, _x, _y, _z):
        self.x = _x
        x = _x
        self.y = _y
        y = _y
        self.z = _z
        z = _z
