#!/usr/bin/env python
# coding: utf-8

# # Aula 09.Ex01 - Malhas e Texturas - Mapeamento de Texturas

# ### Primeiro, vamos importar as bibliotecas necessárias.
# Verifique no código anterior um script para instalar as dependências necessárias (OpenGL e GLFW) antes de prosseguir.



import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import glm
import math
from PIL import Image

import desenhos


# ### Inicializando janela



glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
altura = 1600
largura = 1200
window = glfw.create_window(largura, altura, "Malhas e Texturas", None, None)
glfw.make_context_current(window)


# ### GLSL (OpenGL Shading Language)
# 
# Aqui veremos nosso primeiro código GLSL.
# 
# É uma linguagem de shading de alto nível baseada na linguagem de programação C.
# 
# Nós estamos escrevendo código GLSL como se "strings" de uma variável (mas podemos ler de arquivos texto). Esse código, depois, terá que ser compilado e linkado ao nosso programa. 
# 
# Iremos aprender GLSL conforme a necessidade do curso. Usarmos uma versão do GLSL mais antiga, compatível com muitos dispositivos.

# ### GLSL para Vertex Shader
# 
# No Pipeline programável, podemos interagir com Vertex Shaders.
# 
# No código abaixo, estamos fazendo o seguinte:
# 
# * Definindo uma variável chamada position do tipo vec3.
# * Definindo matrizes Model, View e Projection que acumulam transformações geométricas 3D e permitem navegação no cenário.
# * void main() é o ponto de entrada do nosso programa (função principal)
# * gl_Position é uma variável especial do GLSL. Variáveis que começam com 'gl_' são desse tipo. Nesse caso, determina a posição de um vértice. Observe que todo vértice tem 4 coordenadas, por isso nós combinamos nossa variável vec2 com uma variável vec4. Além disso, nós modificamos nosso vetor com base nas transformações Model, View e Projection.



vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        varying vec2 out_texture;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
        }
        """


# ### GLSL para Fragment Shader
# 
# No Pipeline programável, podemos interagir com Fragment Shaders.
# 
# No código abaixo, estamos fazendo o seguinte:
# 
# * void main() é o ponto de entrada do nosso programa (função principal)
# * gl_FragColor é uma variável especial do GLSL. Variáveis que começam com 'gl_' são desse tipo. Nesse caso, determina a cor de um fragmento. Nesse caso é um ponto, mas poderia ser outro objeto (ponto, linha, triangulos, etc).

# ### Possibilitando modificar a cor.
# 
# Nos exemplos anteriores, a variável gl_FragColor estava definida de forma fixa (com cor R=0, G=0, B=0).
# 
# Agora, nós vamos criar uma variável do tipo "uniform", de quatro posições (vec4), para receber o dado de cor do nosso programa rodando em CPU.



fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        
        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            gl_FragColor = texture;
        }
        """


# ### Requisitando slot para a GPU para nossos programas Vertex e Fragment Shaders



# Request a program and shader slots from GPU
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)


# ### Associando nosso código-fonte aos slots solicitados



# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)


# ### Compilando o Vertex Shader
# 
# Se há algum erro em nosso programa Vertex Shader, nosso app para por aqui.



# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")


# ### Compilando o Fragment Shader
# 
# Se há algum erro em nosso programa Fragment Shader, nosso app para por aqui.



glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")


# ### Associando os programas compilado ao programa principal



# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)


# ### Linkagem do programa



# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    
# Make program the default program
glUseProgram(program)


# ### Preparando dados para enviar a GPU
# 
# Nesse momento, nós compilamos nossos Vertex e Program Shaders para que a GPU possa processá-los.
# 
# Por outro lado, as informações de vértices geralmente estão na CPU e devem ser transmitidas para a GPU.
# 

# ### Carregando Modelos (vértices e texturas) a partir de Arquivos
# 
# A função abaixo carrega modelos a partir de arquivos no formato WaveFront.
# 
# 
# Para saber mais sobre o modelo, acesse: https://en.wikipedia.org/wiki/Wavefront_.obj_file
# 
# 
# Nos slides e vídeo-aula da Aula 11 - Parte 1, nós descrevemos o funcionamento desse formato.



def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue


        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])


        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces

    return model





qtd_texturas = 11

glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
glEnable(GL_LINE_SMOOTH)
glEnable(GL_TEXTURE_2D)
textures = glGenTextures(qtd_texturas)

def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    print(img_textura,img.mode)
    img_width = img.size[0]
    img_height = img.size[1]
    #image_data = img.tobytes("raw", "RGB", 0, -1)
    image_data = img.convert("RGBA").tobytes("raw", "RGBA",0,-1)

    #image_data = np.array(list(img.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)


# ### A lista abaixo armazena todos os vertices carregados dos arquivos



vertices_list = []    
textures_coord_list = []


# ### Vamos carregar cada modelo e definir funções para desenhá-los MEXEREI AQUI -----------------------------------------



modelo = load_model_from_file('caixa/caixa.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo cube.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo cube.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas




modelo = load_model_from_file('terreno/terreno2.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo terreno.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo terreno.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas




modelo = load_model_from_file('casa/casa.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo casa.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo casa.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas




modelo = load_model_from_file('monstro/monstro.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo monstro.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo monstro.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas





modelo = load_model_from_file('sky/sky.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo monstro.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo monstro.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas




modelo = load_model_from_file('spiderman/spiderman.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo spiderman.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo spiderman.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas




modelo = load_model_from_file('tanks/tanks.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo tanks.obj. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo tanks.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas




modelo = load_model_from_file('terreno2/terreno2.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo terreno2. Vertice inicial:',len(vertices_list))
for face in modelo['faces']:
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo terreno2. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas




modelo = load_model_from_file('arvore/arvore10.obj')

### inserindo vertices do modelo no vetor de vertices
print('Processando modelo arvore.obj. Vertice inicial:',len(vertices_list))
faces_visited = []
for face in modelo['faces']:
    if face[2] not in faces_visited:
        print(face[2],' vertice inicial =',len(vertices_list))
        faces_visited.append(face[2])
    for vertice_id in face[0]:
        vertices_list.append( modelo['vertices'][vertice_id-1] )
    for texture_id in face[1]:
        textures_coord_list.append( modelo['texture'][texture_id-1] )
print('Processando modelo arvore.obj. Vertice final:',len(vertices_list))

### inserindo coordenadas de textura do modelo no vetor de texturas


# ### Load nas texturas



load_texture_from_file(0,'caixa/caixa2.jpg')
load_texture_from_file(1,'terreno/pedra.jpg')
load_texture_from_file(2,'casa/casa.jpg')
load_texture_from_file(3,'monstro/monstro.jpg')
load_texture_from_file(4,'sky/sky.png')
load_texture_from_file(5,'spiderman/spiderman.png')
load_texture_from_file(6,'tanks/tanks.jpg')
load_texture_from_file(7,'terreno2/terreno3.png')
load_texture_from_file(8,'arvore/bark_0021.jpg')
load_texture_from_file(9,'arvore/DB2X2_L01.png')
load_texture_from_file(10,'terreno/grama.jpg')


# ### Para enviar nossos dados da CPU para a GPU, precisamos requisitar slots.
# 
# Nós agora vamos requisitar dois slots.
# * Um para enviar coordenadas dos vértices.
# * Outros para enviar coordenadas de texturas.



# Request a buffer slot from GPU
buffer = glGenBuffers(2)


# ###  Enviando coordenadas de vértices para a GPU



vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
vertices['position'] = vertices_list


# Upload data
glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)
loc_vertices = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc_vertices)
glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)


# ###  Enviando coordenadas de textura para a GPU



textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)]) # duas coordenadas
textures['position'] = textures_coord_list


# Upload data
glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
stride = textures.strides[0]
offset = ctypes.c_void_p(0)
loc_texture_coord = glGetAttribLocation(program, "texture_coord")
glEnableVertexAttribArray(loc_texture_coord)
glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)





# ### Eventos para modificar a posição da câmera. MEXEREI AQUI -----------------------------------------
# 
# * Usei as teclas A, S, D e W para movimentação no espaço tridimensional
# * Usei a posição do mouse para "direcionar" a câmera



cameraPos   = glm.vec3(0.0,  0.0,  1.0);
cameraFront = glm.vec3(0.0,  0.0, -1.0);
cameraUp    = glm.vec3(0.0,  1.0,  0.0);


polygonal_mode = False


inc_fov = 0
inc_near = 0
inc_far = 0
inc_view_up = 0

def key_event(window,key,scancode,action,mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode, inc_fov, inc_near, inc_far, cameraUp, inc_view_up
    
    # print(key)
    if key == 66:
        inc_view_up += 0.1
        #cameraUp    = glm.vec3(0.0+inc_view_up,  1.0+inc_view_up,  0.0+inc_view_up);
    if key == 78: inc_near += 0.1
    if key == 77: inc_far -= 5
        
    
        
    cameraSpeed = 0.2
    if key == 87 and (action==1 or action==2): # tecla W
        cameraPos += cameraSpeed * cameraFront
    
    if key == 83 and (action==1 or action==2): # tecla S
        cameraPos -= cameraSpeed * cameraFront
    
    if key == 65 and (action==1 or action==2): # tecla A
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
        
    if key == 68 and (action==1 or action==2): # tecla D
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
        
    if key == 80 and action==1 and polygonal_mode==True:
        polygonal_mode=False
    else:
        if key == 80 and action==1 and polygonal_mode==False:
            polygonal_mode=True
        
        
        
firstMouse = True
yaw = -90.0 
pitch = 0.0
lastX =  largura/2
lastY =  altura/2

def mouse_event(window, xpos, ypos):
    global firstMouse, cameraFront, yaw, pitch, lastX, lastY
    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos
    lastX = xpos
    lastY = ypos

    sensitivity = 0.3 
    xoffset *= sensitivity
    yoffset *= sensitivity

    yaw += xoffset;
    pitch += yoffset;

    
    if pitch >= 90.0: pitch = 90.0
    if pitch <= -90.0: pitch = -90.0

    front = glm.vec3()
    front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    front.y = math.sin(glm.radians(pitch))
    front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)


    
glfw.set_key_callback(window,key_event)
glfw.set_cursor_pos_callback(window, mouse_event)


# ### Matrizes Model, View e Projection
# 
# Teremos uma aula específica para entender o seu funcionamento.



def model(angle, r_x, r_y, r_z, t_x, t_y, t_z, s_x, s_y, s_z):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

    
    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, glm.vec3(t_x, t_y, t_z))    
    
    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(r_x, r_y, r_z))
    
    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, glm.vec3(s_x, s_y, s_z))
    
    matrix_transform = np.array(matrix_transform) # pegando a transposta da matriz (glm trabalha com ela invertida)
    
    return matrix_transform

def view():
    global cameraPos, cameraFront, cameraUp
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp);
    mat_view = np.array(mat_view)
    return mat_view

def projection():
    global altura, largura, inc_fov, inc_near, inc_far
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(45.0), largura/altura, 0.1, 1000.0)
    mat_projection = np.array(mat_projection)    
    return mat_projection


# ### Nesse momento, nós exibimos a janela!
# 



glfw.show_window(window)
glfw.set_cursor_pos(window, lastX, lastY)


# ### Loop principal da janela. MEXEREI AQUI -----------------------------------------
# Enquanto a janela não for fechada, esse laço será executado. É neste espaço que trabalhamos com algumas interações com a OpenGL.



glEnable(GL_DEPTH_TEST) ### importante para 3D
   

rotacao_inc = 0
while not glfw.window_should_close(window):

    glfw.poll_events() 
    
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if polygonal_mode==True:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    if polygonal_mode==False:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    
    rotacao_inc += 0.1
    
    desenhos.desenha_terreno_pedra(model, program)
    desenhos.desenha_terreno_grama(model, program)
    desenhos.desenha_sky(model, program, rotacao_inc)
    desenhos.desenha_casa(model, program)
    # desenha_monstro(rotacao_inc)
    # desenha_spiderman()
    # desenha_tanks(rotacao_inc)
    # desenha_terreno2()
    # desenha_arvore()
    
    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()