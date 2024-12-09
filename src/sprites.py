from globals import *
from load import load_model_from_file, processando_modelo, load_texture_from_file

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
        for i in range(len(urls_textures)):
            load_texture_from_file(start_id_texture + i, urls_textures[i])
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

        loc_ka = glGetUniformLocation(program, "ka")
        glUniform1f(loc_ka, self.material.ka)

        loc_kd = glGetUniformLocation(program, "kd")
        glUniform1f(loc_kd, self.material.kd)

        loc_ks = glGetUniformLocation(program, "ks")
        glUniform1f(loc_ks, self.material.ks)

        loc_ns = glGetUniformLocation(program, "ns")
        glUniform1f(loc_ns, self.material.ns)

        loc_is_inside = glGetUniformLocation(program, "is_inside")
        glUniform1i(loc_is_inside, self.is_inside)

        for i in range(len(self.textures_verts)-1):
            glBindTexture(GL_TEXTURE_2D, self.start_id_texture + i)
            glDrawArrays(GL_TRIANGLES, self.textures_verts[i], self.textures_verts[i+1] - self.textures_verts[i])
