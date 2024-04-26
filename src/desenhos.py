from globals import *

# ### Desenhando nossos modelos MEXEREI AQUI -----------------------------------------
# * Cada modelo tem um Model para posicioná-los no mundo.
# * É necessário saber qual a posição inicial e total de vértices de cada modelo
# * É necessário indicar qual o ID da textura do modelo

def desenha_terreno_pedra(model, program, matrix):
    
    # rotacao
    angle = 0.0;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 1)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 36, 42-36) ## renderizando
    

def desenha_terreno_grama(model, program, matrix):
    
    # rotacao
    angle = 0.0;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 10)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 36, 42-36) ## renderizando
    

def desenha_terreno2(model, program, matrix):
    
    # rotacao
    angle = 0.0;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 7)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 662985 , 683871-662985) ## renderizando


def desenha_casa(model, program, matrix):
    
    # rotacao
    angle = 180.0;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 2)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 42, 1476-42) ## renderizando


def desenha_monstro(model, program, matrix, rotacao_inc):
    
    # rotacao
    angle = rotacao_inc;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 3)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 1476, 7584-1476) ## renderizando


def desenha_sky(model, program, matrix, rotacao_inc): 
    
   # rotacao
    angle = rotacao_inc;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 4)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 7584 , 13536-7584) ## renderizando
    

def desenha_spiderman(model, program, matrix):
    
    # rotacao
    angle = 90.0;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 5)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 13536 , 463518-13536) ## renderizando


def desenha_tanks(model, program, matrix):
    
   # rotacao
    angle = -90.0;
    
    mat_model = model(angle, matrix)
    loc_model = glGetUniformLocation(program, "model")
    glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_model)
       
    #define id da textura do modelo
    glBindTexture(GL_TEXTURE_2D, 6)
    
    
    # desenha o modelo
    glDrawArrays(GL_TRIANGLES, 463518 , 662985-463518) ## renderizando


def desenha_arvore1(model, program, matrix):
    
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

