from globals import *
from load import load_model_from_file, processando_modelo, load_texture_from_file


# Classe que guarda as informações de cada objeto, como vertices e texturas e a função de mudar o angulo e de desenhar na tela
class Material:
    def __init__(self, name, ka, kd, ks, ns):
        self.name = name
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.ns = ns
class Object:

    def __init__(self, url_model, urls_textures, start_id_texture, material, is_inside=False):

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
        self.is_inside = is_inside
        self.material = material

    def change_angle(self, angle):
        self.angle = angle

    def desenha(self, model, program):

        mat_model = model(self.angle, self.matriz)
        loc_model = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)

        #### define parametros de ilumincao do modelo
        ka = self.material.ka # coeficiente de reflexao ambiente do modelo
        kd = self.material.kd # coeficieznte de reflexao difusa do modelo
        ks = self.material.ks # coeficiente de reflexao especular do modelo
        ns = self.material.ns #expoente de reflexao especular

        loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, ka) ### envia ka pra gpu

        loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
        glUniform1f(loc_kd, kd) ### envia kd pra gpu    

        loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
        glUniform1f(loc_ks, ks) ### envia ns pra gpu        

        loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU
        glUniform1f(loc_ns, ns) ### envia ns pra gpu            

        loc_is_inside = glGetUniformLocation(program, "is_inside")
        glUniform1i(loc_is_inside, self.is_inside)

        for i in range(0, len(self.textures_verts)-1):
            glBindTexture(GL_TEXTURE_2D, self.start_id_texture + i)
            glDrawArrays(GL_TRIANGLES, self.textures_verts[i], self.textures_verts[i+1] - self.textures_verts[i])
