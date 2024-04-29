from globals import *
from load import load_model_from_file, processando_modelo, load_texture_from_file

class Object:

    def __init__(self, url_model, urls_textures, start_id_texture):
        
        modelo = load_model_from_file(url_model)

        print('Processando modelo: ' + url_model)
        textures_verts = processando_modelo(modelo)
        print("Vertice inicial: " + str(textures_verts[0]) 
        + "\nVertice Final: " + str(textures_verts[len(textures_verts)-1]) 
        + "\nNumero de texturas: " + str(len(textures_verts)-1))

        for i in range(0, len(urls_textures)):
            print(str(start_id_texture + i) + " " + urls_textures[i], end="\n")
            load_texture_from_file(start_id_texture + i, urls_textures[i])
        print("\n\n")

        self.matriz = MatrizTRS()
        self.angle = 0
        self.textures_verts = textures_verts
        self.start_id_texture = start_id_texture
    
    def change_Angle(self, angle):
        self.angle = angle

    def desenha(self, model, program):

        mat_model = model(self.angle, self.matriz)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
        for i in range(0, len(self.textures_verts)-1):
            glBindTexture(GL_TEXTURE_2D, self.start_id_texture + i)        
            glDrawArrays(GL_TRIANGLES, self.textures_verts[i], self.textures_verts[i+1] - self.textures_verts[i])
            
