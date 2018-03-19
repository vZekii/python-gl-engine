import itertools

from pyglet.gl import *


class Obj(object):
    def __init__(self, object_file, material_file):
        """
        An object for storing information of a single model
        :param object_file: the .obj file path of the model
        :param material_file: the .mtl file path of the model
        """
        self.file = object_file
        self.batch = pyglet.graphics.Batch()  # This will work for now, but it will be changed later
        self.vertex_list, self.normals = [], []  # Extracting vertices from a .obj file
        self.mats = MaterialReader(material_file)

        self.position, self.rotation = [0, 0, 0], [0, 0, 0]

        self.import_model()

    def import_model(self):
        """
        Reads the .obj file and records the data
        """
        diffuse_val = (0.0, 0.0, 0.0)
        for line in open(self.file):
            data = list(filter(None, line.rstrip().split(' ')))
            try:
                if data[0] == 'v':
                    x, y, z = float(data[1]), float(data[2]), float(data[3])
                    self.vertex_list.append([x, y, z])

                elif data[0] == 'f':
                    verts = [int(v.split('//')[0]) for v in data[1:4]]
                    values = tuple(itertools.chain(*[self.vertex_list[vert - 1] for vert in verts]))
                    self.batch.add(3, GL_TRIANGLES, None, ('v3f', values), ('c3f', tuple(diffuse_val) * 3))

                elif data[0] == 'vn':
                    x, y, z = float(data[1]), float(data[2]), float(data[3])
                    self.normals.append([x, y, z])

                elif data[0] == 'usemtl':
                    diffuse_val = self.mats.materials[data[1]].diffuse
                    print(tuple(diffuse_val))
                    print(self.mats.materials[data[1]].diffuse)

            except IndexError:
                pass

    def draw(self):
        """
        Custom drawing function to allow translation and rotation on each model
        """
        glPushMatrix()
        x, y, z = self.position
        xrot, yrot, zrot = self.rotation
        glTranslatef(x, y, z)
        glRotatef(xrot, 1, 0, 0)
        glRotatef(yrot, 0, 1, 0)
        glRotatef(zrot, 0, 0, 1)
        self.batch.draw()
        glPopMatrix()


class MaterialReader:
    def __init__(self, filename):
        """
        Class to read a material file associated with the model
        :param filename: the path of the file
        """
        self.file = filename
        self.materials = {}  # Storage for all materials

        self.setup_materials()

    def setup_materials(self):
        """
        Reads the .mtl file
        """
        cur_mat = None
        for line in open(self.file):
            try:
                if line.startswith('newmtl'):
                    data = list(filter(None, line.rstrip().split(' ')))
                    self.materials[data[1]] = Material(data[1])
                    cur_mat = self.materials[data[1]]
                if cur_mat:
                    data = list(filter(None, line.rstrip().split(' ')))
                    if data[0] == 'Kd':
                        cur_mat.diffuse = list(map(float, data[1:4]))

            except IndexError:
                pass


class Material(object):
    def __init__(self, name):
        """
        object for storing information about a specific material
        :param name: the name of the material
        """
        self.name = name
        self.diffuse = [0.7, 0.7, 0.7]  # Default diffuse value

    def draw(self, face):
        """
        Draws the given face with the material
        :param face: a face of an object
        """
        glMaterialfv(face, GL_DIFFUSE, self.diffuse)
