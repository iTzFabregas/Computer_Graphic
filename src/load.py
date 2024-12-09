from globals import *
from PIL import Image

def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    img_width, img_height = img.size
    image_data = img.convert("RGBA").tobytes("raw", "RGBA", 0, -1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

def load_model_from_file(filename):
    objects = {}
    vertices = []
    normals = []
    texture_coords = []
    faces = []

    material = None

    for line in open(filename, "r"):
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue

        if values[0] == 'v':
            vertices.append(values[1:4])
        if values[0] == 'vn':
            normals.append(values[1:4])
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normals = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)
            faces.append((face, face_texture, face_normals, material))

    model = {
        'vertices': vertices,
        'texture': texture_coords,
        'faces': faces,
        'normals': normals
    }

    return model

def processando_modelo(modelo):
    global vertices_list, textures_coord_list, normals_list
    textures_verts = []
    faces_visited = []
    for face in modelo['faces']:
        if face[3] not in faces_visited:
            faces_visited.append(face[3])
            textures_verts.append(len(vertices_list))
        for vertice_id in face[0]:
            vertices_list.append(modelo['vertices'][vertice_id-1])
        for texture_id in face[1]:
            textures_coord_list.append(modelo['texture'][texture_id-1])
        for normal_id in face[2]:
            normals_list.append(modelo['normals'][normal_id-1])

    textures_verts.append(len(vertices_list))
    return textures_verts
