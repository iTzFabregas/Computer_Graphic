from globals import *
from load import load_model_from_file, processando_modelo, load_texture_from_file

class Object:

    # matriz
    # angle
    # vert_inicial
    # num_vert

    def __init__(self, url_model, url_texture, id_texture):
        
        modelo = load_model_from_file(url_model)
        print('Processando modelo: ' + url_model)
        vert_inicial, num_vert = processando_modelo(modelo)
        load_texture_from_file(id_texture, url_texture)

        self.matriz = MatrizTRS()
        self.angle = 0
        self.vert_inicial = vert_inicial
        self.num_vert = num_vert
        self.id_texture = id_texture
    
    def change_Angle(self, angle):
        self.angle = angle

    def desenha(self, model, program):

        mat_model = model(self.angle, self.matriz)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, self.id_texture)
        
        
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, self.vert_inicial, self.num_vert) ## renderizando
    



    def second_texture(self, url):
        self.second_texture = url

    
    def desenha_arvore2(model, program, matrix):
        
        # rotacao
        angle = 0.0;
        
        mat_model = model(angle, matrix)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
        
        
        ### desenho o tronco da arvore
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, 8)
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, 683871, 704133-683871) ## renderizando
        
        ### desenho as folhas
        #define id da textura do modelo
        glBindTexture(GL_TEXTURE_2D, 9)
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, 704133, 725043-704133) ## renderizando
        
            
