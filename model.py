import itertools

from pyglet.gl import *


class Obj(object):
    def __init__(self, object_file, material_file=None):
        self.file = object_file
        self.batch = pyglet.graphics.Batch()  # This will work for now, but it will be changed later
        self.vertex_list, self.normals = [], []  # Extracting vertices from a .obj file
        self.mats = MaterialReader(material_file) if material_file is not None else None

        self.import_model()

    def import_model(self):
        diffuse_val = (0.0, 0.0, 0.0)
        for line in open(self.file):
            data = list(filter(None, line.rstrip().split(' ')))
            try:
                if data[0] == 'v':
                    x, y, z = float(data[1]), float(data[2]), float(data[3])
                    self.vertex_list.append([x, y, z])

                elif data[0] == 'f':
                    verts = [int(v.split('/')[0]) for v in data[1:4]]
                    values = tuple(itertools.chain(*[self.vertex_list[vert - 1] for vert in verts]))
                    self.batch.add(3, GL_TRIANGLES, None, ('v3f', values), ('c3f', tuple(diffuse_val) * 3))

                elif data[0] == 'vn':
                    x, y, z = float(data[1]), float(data[2]), float(data[3])
                    self.normals.append([x, y, z])

            except IndexError:
                pass


class Material(object):
    def __init__(self, name):
        self.name = name


class MaterialReader:
    def __init__(self, filename):
        self.file = filename
        self.materials = {}  # Storage for all materials
