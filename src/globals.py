import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import math
from PIL import Image

### A lista abaixo armazena todos os vertices carregados dos arquivos
vertices_list = []    
textures_coord_list = []
normals_list = []

# Classe que guarda a matriz translação de cada objeto
class MatrizTRS:

    def __init__(self):
        self.t = [0.0, 0.0, 0.0]
        self.r = [0.0, 1.0, 0.0]
        self.s = [1.0, 1.0, 1.0]
    
    def change_T(self, t):
        self.t = t
    
    def change_R(self, r):
        self.r = r
    
    def change_S(self, s):
        self.s = s

    def change_All(self, t, r, s):
        self.t = t
        self.r = r
        self.s = s

# Funções para substituição de glm usando numpy
def vec3(x, y, z):
    return np.array([x, y, z], dtype=np.float32)

def mat4_identity():
    return np.eye(4, dtype=np.float32)

def translate(matrix, vector):
    translation = np.eye(4, dtype=np.float32)
    translation[:3, 3] = vector[:3]  # Garante que apenas os primeiros 3 componentes sejam usados
    return np.dot(matrix, translation)

def scale(matrix, vector):
    scaling = np.eye(4, dtype=np.float32)
    scaling[0, 0], scaling[1, 1], scaling[2, 2] = vector
    return np.dot(matrix, scaling)

def rotate(matrix, angle, axis):
    angle = np.radians(angle)
    axis = axis / np.linalg.norm(axis)
    c, s = np.cos(angle), np.sin(angle)
    x, y, z = axis
    rotation = np.array([
        [c + (1-c)*x*x, (1-c)*x*y - s*z, (1-c)*x*z + s*y, 0],
        [(1-c)*y*x + s*z, c + (1-c)*y*y, (1-c)*y*z - s*x, 0],
        [(1-c)*z*x - s*y, (1-c)*z*y + s*x, c + (1-c)*z*z, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)
    return np.dot(matrix, rotation)

def lookAt(eye, center, up):
    f = center - eye
    f = f / np.linalg.norm(f)

    u = up / np.linalg.norm(up)
    s = np.cross(f, u)
    u = np.cross(s, f)

    result = np.eye(4, dtype=np.float32)
    result[0, :3] = s
    result[1, :3] = u
    result[2, :3] = -f
    result[:3, 3] = -np.dot(result[:3, :3], eye)

    return result

def perspective(fovy, aspect, near, far):
    fovy_rad = np.radians(fovy)
    f = 1 / np.tan(fovy_rad / 2)
    result = np.zeros((4, 4), dtype=np.float32)
    result[0, 0] = f / aspect
    result[1, 1] = f
    result[2, 2] = (far + near) / (near - far)
    result[2, 3] = (2 * far * near) / (near - far)
    result[3, 2] = -1
    return result

