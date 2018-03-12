class Obj(object):
    def __init__(self, object_file, material_file=None):
        self.file = object_file
        self.vertex_list, self.normals = [], []  # Extracting vertices from a .obj file
        self.mats = MaterialReader(material_file) if material_file is not None else None

        self.import_model()

    def import_model(self):
        pass


class Material(object):
    def __init__(self, name):
        self.name = name


class MaterialReader:
    def __init__(self, filename):
        self.file = filename
        self.materials = {}  # Storage for all materials
