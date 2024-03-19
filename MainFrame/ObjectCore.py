import importlib.util
import os
import numpy as np
import mainLib
import m_math


class ScriptRunner:
    def __init__(self):
        self.script_objects = []

    def load_scripts(self, script_paths):
        for script_path in script_paths:
            class_name = os.path.splitext(os.path.basename(script_path))[0]
            spec = importlib.util.spec_from_file_location(class_name, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            script_obj = getattr(module, class_name)()
            self.script_objects.append(script_obj)

    def run_method_on_scripts(self, method_name):
        for script_obj in self.script_objects:
            try:
                method_to_call = getattr(script_obj, method_name)
                method_to_call()
            except Exception as e:
                print(f"Error while calling method {method_name} in script: {script_obj.__class__.__name__}: {e}")


class GameObject:
    def __init__(self, model, xyz, Local_xyz, properti, uv, text_way, ids):
        pos = xyz
        l_pos = Local_xyz
        self.uv = uv
        self.textur = text_way
        self.transform = [1, 1, 1]
        self.id = ids
        self.model = np.array(model, dtype=np.float64)
        self.xyz = pos
        self.local_xyz = l_pos
        self.prop_dt = properti
        self.scrip_name = []
        for scr in self.prop_dt:
            self.scrip_name.append(scr['file'])
        runner = ScriptRunner()
        self.scr_raner = runner
        runner.load_scripts(self.scrip_name)
        runner.run_method_on_scripts("aweik")

    def GetComponent(self, componet):
        for scr in range(self.prop_dt):
            if componet in scr['component']:
                return scr
        return None

    def GetAllComponentPath(self):
        return self.scrip_name

    def rotate(self, xyz):
        # Преобразование углов поворота из градусов в радианы
        angles = np.radians(xyz)

        # Матрицы поворота для каждой из осей X, Y, Z
        rotation_x = np.array([
            [1, 0, 0],
            [0, np.cos(angles[0]), -np.sin(angles[0])],
            [0, np.sin(angles[0]), np.cos(angles[0])]
        ])

        rotation_y = np.array([
            [np.cos(angles[1]), 0, np.sin(angles[1])],
            [0, 1, 0],
            [-np.sin(angles[1]), 0, np.cos(angles[1])]
        ])

        rotation_z = np.array([
            [np.cos(angles[2]), -np.sin(angles[2]), 0],
            [np.sin(angles[2]), np.cos(angles[2]), 0],
            [0, 0, 1]
        ])

        # Применение вращений к матрице точек
        rotated_points = np.dot(self.model, np.dot(rotation_x, np.dot(rotation_y, rotation_z)))

        self.model = rotated_points

    def scale(self, scale):
        self.transform = scale

    def position(self, new_pos):
        self.xyz = new_pos

    def local_position(self, new_pos):
        self.local_xyz = new_pos

    def __render__(self):
        pr = mainLib.primitivs()
        pr.coord_render_tex(self.textur, self.model, self.uv)

    def __update__(self):
        vm = m_math.vectors()
        self.model = vm.avx_hvsum(self.model, self.xyz)
        self.model = vm.avx_hvsum(self.model, self.local_xyz)
        self.model = vm.avx_hvmul(self.model, self.transform)

    def __start__(self):
        runner = self.scr_raner
        runner.load_scripts(self.scrip_name)
        runner.run_method_on_scripts("start")

    def __self__(self):
        return self


class main():
    def __init__(self, scene):
        self.scene = scene
        self.objects = []
        for _obj_ in self.scene:
            _type = _obj_['type']
            if _type == 5:
                try:
                    models = _obj_["models"]
                    try:
                        uv = _obj_["uv"]
                    except:
                        uv = [0, 0, 0]
                    try:
                        texr = _obj_['tex']
                    except:
                        texr = 'rsr\\material\\material\\test_textr.jpg'
                except:
                    models = [0, 0, 0]
                try:
                    local_pos = _obj_["l_xyz"]
                except:
                    local_pos = [0, 0, 0]
                try:
                    prop_dt = _obj_['component']
                except:
                    prop_dt = [{'name': 'plays_holder', 'file': None}]
                ids = _obj_['id']
                _obj__ = GameObject(model=models, xyz=_obj_['xyz'], Local_xyz=local_pos, properti=prop_dt, uv=uv, text_way=texr, ids=int(ids))
                self.objects.append(_obj__)


    def main(self, frame_id):
        i = frame_id
        obj_on_scene = self.scene
        pr = mainLib.primitivs()
        vm = m_math.vectors()
        objW = mainLib.ModelWorker()
        if frame_id == 0:
            for _obj_ in self.objects:
                _obj_.__start__()

        for obj in range(len(obj_on_scene)):
            _objeck = obj_on_scene[obj]
            _type = _objeck['type']
            if _type == 0:
                coords = _objeck["models"]
                uv_coords = _objeck["uv"]
                textyres = _objeck['tex']
                xyz = _objeck['xyz']
                coords = vm.avx_hvsum(coords, xyz)
                pr.coord_render_tex(textyres, coords, uv_coords)
            if _type == 1:
                coords = _objeck["models"]
                uv_coords = _objeck["uv"]
                textyres = _objeck['tex']
                xyz = _objeck['xyz']
                coords = vm.avx_hvsum(coords, xyz)
                pr.coord_render_tex(textyres, coords, uv_coords)
            if _type == 2:
                coords = _objeck["models"]
                uv_coords = _objeck["uv"]
                textyres = _objeck['tex']
                stop_coord = _objeck["stop_dist"]
                is_looped = _objeck["loop"]
                xyz = _objeck['xyz']
                speed_obj = _objeck["speed"]
                curent_tg = stop_coord
                dist = vm.vsub(curent_tg, xyz)
                if xyz[0] <= curent_tg[0]:
                    if dist[0] > 0:
                        xyz = vm.vsum(xyz, [i * (speed_obj / 10), 0, 0])
                    elif dist[0] < 0:
                        xyz = vm.vsub(xyz, [i * (speed_obj / 10), 0, 0])
                if xyz[1] <= curent_tg[1]:
                    if dist[1] > 0:
                        xyz = vm.vsum(xyz, [0, i * (speed_obj / 10), 0])
                    elif dist[1] < 0:
                        xyz = vm.vsub(xyz, [0, i * (speed_obj / 10), 0])
                if xyz[2] <= curent_tg[2]:
                    if dist[2] > 0:
                        xyz = vm.vsum(xyz, [0, 0, i * (speed_obj / 10)])
                    elif dist[2] < 0:
                        xyz = vm.vsub(xyz, [0, 0, i * (speed_obj / 10)])
                coords = vm.avx_hvsum(coords, xyz)
                pr.coord_render_tex(textyres, coords, uv_coords)
                _objeck['xyz'] = xyz
            if _type == 3:
                try:
                    coords = _objeck["models"]
                except:
                    models = _objeck["model"]
                    coords, uv_coords = objW.GetOBJModel(models)
                textyres = _objeck['tex']
                xyz = _objeck['xyz']
                size = _objeck['size']
                coords = vm.avx_nmul(coords, size)
                coords = vm.avx_hvsum(coords, xyz)
                pr.coord_render_tex(textyres, coords, uv_coords)
            if _type == 4:
                coords = _objeck["models"]
                uv_coords = _objeck["uv"]
                textyres = _objeck['tex']
                xyz = _objeck['xyz']
                try:
                    iter = _objeck["i"]
                except:
                    _objeck["i"] = 0
                    iter = 0
                try:
                    rev = _objeck["rev"]
                except:
                    _objeck["rev"] = False
                    rev = False
                xyz = vm.vsum(xyz, [0, 0, iter])

                if rev is False:
                    if iter <= 5 and iter >= -5:
                        iter = iter + 0.1
                    else:
                        rev = True
                if rev is True:
                    if iter > -5:
                        iter = iter - 0.1
                    elif iter < -5:
                        iter = -5
                    else:
                        rev = False
                coords = vm.avx_hvsum(coords, xyz)
                pr.coord_render_tex(textyres, coords, uv_coords)
                _objeck['xyz'] = xyz
                _objeck["i"] = iter
                _objeck["rev"] = rev
            if _type == 5:
                ij = 0
                while True:
                    _obj_ = self.objects[ij]
                    obj_id = _obj_.id
                    if obj_id == ['id']:
                        _obj_.__update__()
                        _obj_.__render__()
                    if ij == len(self.objects) - 1:
                        break
                    ij = ij + 1


if __name__ == '__main__':
    obj_ = GameObject(Local_xyz=[0, 0, 0], xyz=[0, 0, 0], name='dsd',
                      model=[[-20, -20, 0], [20, -20, 0], [20, 20, 0], [-20, 20, 0]],
                      properti=[{'name': 'test',
                                 'file': 'C:\\Users\\tyuly\\PycharmProjects\\3pyEngie\\rsr\\scripts\\test.py'}])
    print(obj_.model)

    obj_.rotate([0, 2, 0])
    print(obj_.model)
