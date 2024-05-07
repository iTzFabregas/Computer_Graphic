from globals import *

class House:

    def __init__(self, matriz, angle):
        
        self.matriz = matriz
        self.angle = angle
        self.objects = []
    
    def change_Angle(self, angle):
        self.angle = angle

    def add_object(self, obj):
        self.objects.append(obj)
    
    def desenha(self, model, program):
        for obj in self.objects:
            obj.desenha(model, program)