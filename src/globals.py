import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
from PIL import Image

class MatrizTRS:
    t = [0.0,0.0,0.0] # x,y,z
    r = [0.0,0.0,0.0] # x,y,z
    s = [0.0,0.0,0.0] # x,y,z

    def __init__(self):
        self.t = [0.0,0.0,0.0]
        self.r = [0.0,0.0,0.0]
        self.s = [0.0,0.0,0.0]
    
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