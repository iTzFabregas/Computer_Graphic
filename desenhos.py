import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
from PIL import Image

# ### Desenhando nossos modelos MEXEREI AQUI -----------------------------------------
# * Cada modelo tem um Model para posicioná-los no mundo.
# * É necessário saber qual a posição inicial e total de vértices de cada modelo
# * É necessário indicar qual o ID da textura do modelo
# 


def desenha_terreno_pedra(model, program):
    
    # aplica a matriz model
    
    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    
    # translacao
    t_x = 0.0; t_y = -1.0; t_z = 0.0;
    
    # escala
    s_x = 2.0; s_y = 1.0; s_z = 200.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 1)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 36, 42-36) ## renderizando
    

def desenha_terreno_grama(model, program):
    
    # aplica a matriz model
    
    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    
    # translacao
    t_x = 4.0; t_y = -1.0; t_z = 0.0;
    
    # escala
    s_x = 2.0; s_y = 1.0; s_z = 200.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 10)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 36, 42-36) ## renderizando
    

def desenha_casa(model, program):
    
    # aplica a matriz model
    
    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    
    # translacao
    t_x = 5.0; t_y = -1.0; t_z = 4.0;
    
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 2)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 42, 1476-42) ## renderizando


def desenha_monstro(model, program, rotacao_inc):
    
    # aplica a matriz model
    
    # rotacao
    angle = rotacao_inc;
    r_x = 0.0; r_y = 1.0; r_z = 0.0;
    
    # translacao
    t_x = 0.0; t_y = -1.0; t_z = 0.0;
    
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 3)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 1476, 7584-1476) ## renderizando


def desenha_sky(model, program, rotacao_inc): 
    
    # aplica a matriz model
    
    # rotacao
    angle = rotacao_inc;
    r_x = 0.0; r_y = 1.0; r_z = 0.0;
    
    # translacao
    t_x = 0.0; t_y = 0.0; t_z = 0.0;
    
    # escala
    s_x = 3.0; s_y = 3.0; s_z = 3.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 4)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 7584 , 13536-7584) ## renderizando
    

def desenha_spiderman(model, program):
    
    # aplica a matriz model
    
    # rotacao
    angle = 0;
    r_x = 0.0; r_y = 1.0; r_z = 0.0;
    
    # translacao
    t_x = 50.0; t_y = 0.0; t_z = 0.0;
    
    # escala
    s_x = 1.0; s_y = 1.0; s_z = 1.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 5)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 13536 , 463518-13536) ## renderizando


def desenha_tanks(model, program, inc_t):
    
    # aplica a matriz model
    
    # rotacao
    angle = -90;
    r_x = 1.0; r_y = 0.0; r_z = 0.0;
    
    # translacao
    t_x = 50.0; t_y = 0.0; t_z = 0.0+inc_t;
    
    # escala
    s_x = 4.0; s_y = 4.0; s_z = 4.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 6)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 463518 , 662985-463518) ## renderizando


def desenha_terreno2(model, program):
    
    # aplica a matriz model
    
    # rotacao
    angle = 0;
    r_x = 1.0; r_y = 0.0; r_z = 0.0;
    
    # translacao
    t_x = 50.0; t_y = 0.0; t_z = 0.0;
    
    # escala
    s_x = 2.0; s_y = 2.0; s_z = 2.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 7)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 662985 , 683871-662985) ## renderizando


def desenha_arvore(model, program):
    
    # aplica a matriz model
    
    # rotacao
    angle = 0.0;
    r_x = 0.0; r_y = 0.0; r_z = 1.0;
    
    # translacao
    t_x = -10.0; t_y = -1.0; t_z = 15.0;
    
    # escala
    s_x = 7.0; s_y = 7.0; s_z = 7.0;
    
    mat_model = model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z)
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

