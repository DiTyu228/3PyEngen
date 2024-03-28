import mainLib as mn

map_w = mn.MapWorker()
scene = [
{
            "name": "pr1",
            'id': 0,
            'type': 0,
            'xyz':[0, 0, -5],
            'tex':'rsr\\material\\material\\concreit1.jpg',
            'models': [
            [-20, -20, 0],
            [20, -20, 0],
            [20, 20, 0],
            [-20, 20, 0]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "pr2",
            'id': 1,
            'type': 0,
            'xyz':[0, 0, 10],
            'tex':'rsr\\material\\material\\concreit1.jpg',
            'models': [
            [-20, -20, 0],
            [20, -20, 0],
            [20, 20, 0],
            [-20, 20, 0]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "pr3",
            'id': 2,
            'type': 1,
            'xyz': [0, 0, 10],
            'loop': True,
            'end': False,
            "stop_coord": [10, 10, -10],
            "start_coord": [0, 0, 10],
            "speed": 0.1,
            'tex':'rsr\\material\\material\\brick.jpg',
            'models': [
            [-20, -20, 0],
            [20, -20, 0],
            [20, 20, 0],
            [-20, 20, 0]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "hogwaga",
            'id': 3,
            'type': 2,
            'xyz': [0, 0, 10],
            'loop': True,
            "stop_dist": [-10, -10, -10],
            "speed": 0.5,
            'tex':'rsr\\material\\material\\test_textr3.png',
            'models': [
            [-20, -20, 0],
            [20, -20, 0],
            [20, 20, 0],
            [-20, 20, 0]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "hogwagaOBJ",
            'id': 4,
            'type': 3,
            'xyz': [0, 0, 0],
            'size': 10,
            'loop': True,
            "stop_dist": [-10, -10, -10],
            "speed": 0.5,
            'tex':'rsr\\material\\material\\concreit1.jpg',
            'model':'rsr\\models\\cube.obj'
        },
{
            "name": "pr3",
            'id': 1,
            'type': 4,
            'xyz':[0, 0, 0],
            'tex':'rsr\\material\\material\\concreit1.jpg',
            'models': [
            [-20, -20, 0],
            [20, -20, 0],
            [20, 20, 0],
            [-20, 20, 0]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "game_object_proto",
            'id': '4',
            'type': 5,
            'xyz': [5, -10, 0],
            "l_xyz": [0, 0, 0],
            'tex':'rsr\\material\\material\\brick.jpg',
            'models': [
            [-20, 0, -10],
            [20, 0, -10],
            [20, 0, 10],
            [-20, 0, 10]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ],
            'component':[{'name':'test', 'file':'rsr\\scripts\\test.py'}]
        },


]


map_w.SetMapData("proto1", scene)
scene = [
{
            "name": "pr1",
            'id': 0,
            'type': 0,
            'xyz':[0, 0, -5],
            'tex':'rsr\\material\\material\\concreit1.jpg',
            'models': [
            [-20, -20, 0],
            [20, -20, 0],
            [20, 20, 0],
            [-20, 20, 0]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "pr2",
            'id': 1,
            'type': 0,
            'xyz':[0, 0, 10],
            'tex':'rsr\\material\\material\\concreit1.jpg',
            'models': [
            [-20, -20, 0],
            [20, -20, 0],
            [20, 20, 0],
            [-20, 20, 0]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "pr1",
            'id': 2,
            'type': 0,
            'xyz':[0, 20, 0],
            'tex':'rsr\\material\\material\\test_textr.jpg',
            'models': [
            [-20, 0, -10],
            [20, 0, -10],
            [20, 0, 10],
            [-20, 0, 10]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "pr2",
            'id': 3,
            'type': 0,
            'xyz':[0, -20, 0],
            'tex':'rsr\\material\\material\\test_textr.jpg',
            'models': [
            [-20, 0, -10],
            [20, 0, -10],
            [20, 0, 10],
            [-20, 0, 10]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ]
        },
{
            "name": "game_object_proto",
            'id': '4',
            'type': 5,
            'xyz':[5, -10, 0],
            "l_xyz":[0, 0, 0],
            'tex':'rsr\\material\\material\\test_textr.jpg',
            'models': [
            [-20, 0, -10],
            [20, 0, -10],
            [20, 0, 10],
            [-20, 0, 10]
            ],
            'uv':[
                [0, 0],
                [1, 0],
                [1, 1],
                [0, 1]
            ],
            'component':[{'name':'test', 'file':'rsr\\scripts\\test.py'}]
        },
]


map_w.SetMapData("proto2", scene)