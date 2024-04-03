import importlib.util
import os
import numpy as np
import mainLib
import m_math


class ScriptRunner:
    def __init__(self):
        self.script_objects = []

    def load_scripts(self, script_paths, _self, _self_transform, _self_render, _self_id, _self_name, _self_components):
        for script_path in script_paths:
            class_name = os.path.splitext(os.path.basename(script_path))[0]
            spec = importlib.util.spec_from_file_location(class_name, script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            script_obj = getattr(module, class_name)(_self_transform, _self_render, _self_id, _self_name,
                                                     _self_components)
            self.script_objects.append(script_obj)
            return script_obj

    def run_method_on_scripts(self, method_name):
        for script_obj in self.script_objects:
            try:
                method_to_call = getattr(script_obj, method_name)
                method_to_call()
            except Exception as e:
                print(f"Error while calling method {method_name} in script: {script_obj.__class__.__name__}: {e}")


class Transform():
    def __init__(self, xyz, Local_xyz, rotation, scale):
        xyz = m_math.Vector3(xyz[0], xyz[1], xyz[2])
        lxyz = m_math.Vector3(Local_xyz[0], Local_xyz[1], Local_xyz[2])
        self.position = xyz + lxyz
        self.LocalPosition = lxyz
        self.rotation = m_math.Vector3(rotation[0], rotation[1], rotation[2])
        self.scale = m_math.Vector3(scale[0], scale[1], scale[2])
        self.all = [self.position, self.LocalPosition, self.rotation, self.scale]

    def __getitem__(self, item):
        return self.all[item]


class Renden():
    def __init__(self, model, uv, text_way):
        self.model = model
        self.uv = uv
        self.texture = text_way


class GameObject:
    def __init__(self, transform, render, ids, name, component_path):
        self.render = render
        self.transform = Transform(transform[0], transform[1], transform[2], transform[3])
        self.id = ids
        self.name = name
        self.component_path = []
        self.component = component_path
        for scr in self.component:
            self.component_path.append(scr['file'])


class GameObjectCore:
    def __init__(self, model, xyz, Local_xyz, properti, uv, text_way, ids, name):
        pos = xyz
        l_pos = Local_xyz
        self.uv = uv
        self.textur = text_way
        self.id = ids
        self.model = np.array(model, dtype=np.float64)
        self.xyz = pos
        self.local_xyz = l_pos
        self.prop_dt = properti
        self.scrip_name = []
        self.transform = Transform(xyz, Local_xyz, [0, 0, 0], [1, 1, 1])
        self.render = Renden(model, uv, text_way)
        self.object = GameObject(self.transform, self.render, ids, name, properti)
        self.Runner = []
        for scr in self.prop_dt:
            self.scrip_name.append(scr['file'])
        runner = ScriptRunner()
        self.scr_raner = runner
        self.componentRunner = runner.load_scripts(self.scrip_name, self.object, self.object.transform,
                                                   self.object.render, self.object.id,
                                                   self.object.name, self.object.component)
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

    def position(self, new_pos):
        self.xyz = new_pos

    def local_position(self, new_pos):
        self.local_xyz = new_pos

    def render_(self):
        pr = mainLib.primitivs()
        pr.coord_render_tex(self.object.render.texture, self.model, self.object.render.uv)

    def update_(self):
        runner = ScriptRunner()
        self.componentRunner.update()
        self.object.transform.position.x = self.componentRunner.transform.position.x
        self.object.transform.position.y = self.componentRunner.transform.position.y
        self.object.transform.position.z = self.componentRunner.transform.position.z
        self.object.transform.rotation.x = self.componentRunner.transform.rotation.x
        self.object.transform.rotation.y = self.componentRunner.transform.rotation.y
        self.object.transform.rotation.z = self.componentRunner.transform.rotation.z
        self.object.transform.scale.x = self.componentRunner.transform.scale.x
        self.object.transform.scale.y = self.componentRunner.transform.scale.y
        self.object.transform.scale.z = self.componentRunner.transform.scale.z
        self.model = np.array(self.object.render.model) + np.array(self.object.transform.position.Vector)
        self.model = np.array(self.model) * np.array(self.object.transform.scale.Vector)

        angles = np.radians(self.object.transform.rotation.Vector)

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
        self.model = np.dot(self.model, np.dot(rotation_x, np.dot(rotation_y, rotation_z)))

        self.pos = np.array(self.object.transform.position.Vector)
        runner.load_scripts(self.scrip_name, self.object, self.object.transform, self.object.render,
                            self.object.id,
                            self.object.name, self.object.component)
        self.scr_raner = runner

    def __start__(self):
        self.pos = np.array(self.object.transform.position.Vector)

        self.scr_raner.run_method_on_scripts("start")

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
                    name = _obj_["name"]
                except:
                    name = str(ids)
                try:
                    prop_dt = _obj_['component']
                except:
                    prop_dt = [{'name': 'plays_holder', 'file': None}]
                ids = _obj_['id']
                _obj__ = GameObjectCore(model=models, xyz=_obj_['xyz'], Local_xyz=local_pos, properti=prop_dt, uv=uv,
                                        text_way=texr, ids=int(ids), name=name)
                self.objects.append(_obj__)
                _obj__.__start__()

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

                    _obj_.update_()
                    _obj_.render_()
                    if ij == len(self.objects) - 1:
                        break
                    ij = ij + 1


if __name__ == '__main__':
    obj_ = GameObjectCore(Local_xyz=[0, 0, 0], xyz=[0, 0, 0], name='dsd',
                          model=[[-20, -20, 0], [20, -20, 0], [20, 20, 0], [-20, 20, 0]],
                          properti=[{'name': 'test',
                                     'file': 'C:\\Users\\tyuly\\PycharmProjects\\3pyEngie\\rsr\\scripts\\test.py'}])
    print(obj_.model)

    obj_.rotate([0, 2, 0])
    print(obj_.model)
