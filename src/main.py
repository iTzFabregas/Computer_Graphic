#!/usr/bin/env python
# coding: utf-8

# Dupla: Fabricio Sampaio     NUSP: 12547423
#        Vitor Nishimura Vian NUSP: 5255289

from globals import *
from sprites import Object

qtd_texturas = 25
altura = 1600
largura = 1900

min_x, max_x = -80, 80
min_y, max_y = 5,50
min_z, max_z = -80,80


# Função que não permite o usuário passar do extremos no mapa 
def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


### Eventos para modificar a posição da câmera.
# * Usei as teclas A, S, D e W para movimentação no espaço tridimensional
# * Usei a posição do mouse para "direcionar" a câmera
def key_event(window,key,scancode,action,mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode, inc_fov, inc_near, inc_far, cameraUp, inc_view_up

    if key == 66:
        inc_view_up += 0.1
        #cameraUp    = glm.vec3(0.0+inc_view_up,  1.0+inc_view_up,  0.0+inc_view_up);
    if key == 78: inc_near += 0.1
    if key == 77: inc_far -= 5
        
    
        
    cameraSpeed = 1
    if key == 87 and (action==1 or action==2): # tecla W
        cameraPos += cameraSpeed * cameraFront
    
    if key == 83 and (action==1 or action==2): # tecla S
        cameraPos -= cameraSpeed * cameraFront
    
    if key == 65 and (action==1 or action==2): # tecla A
        cameraPos -= glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed
        
    if key == 68 and (action==1 or action==2): # tecla D
        cameraPos += glm.normalize(glm.cross(cameraFront, cameraUp)) * cameraSpeed

    cameraPos.x = clamp(cameraPos.x, min_x, max_x)
    cameraPos.y = clamp(cameraPos.y, min_y, max_y)
    cameraPos.z = clamp(cameraPos.z, min_z, max_z)

    if key == 265 and (action==1 or action==2): # tecla seta cima
        shrek.matriz.change_T([shrek.matriz.t[0], shrek.matriz.t[1], shrek.matriz.t[2] - 0.1])

    if key == 264 and (action==1 or action==2): # tecla seta baixo
        shrek.matriz.change_T([shrek.matriz.t[0], shrek.matriz.t[1], shrek.matriz.t[2] + 0.1])

    if key == 262 and (action==1 or action==2): # tecla seta direita
        shrek.matriz.change_T([shrek.matriz.t[0] + 0.1, shrek.matriz.t[1], shrek.matriz.t[2]])

    if key == 263 and (action==1 or action==2): # tecla seta esquerda
        shrek.matriz.change_T([shrek.matriz.t[0] - 0.1, shrek.matriz.t[1], shrek.matriz.t[2]])

    if key == 46 and (action==1 or action==2): # tecla "." ">"
        shrek.matriz.change_S([shrek.matriz.s[0] + 0.001, shrek.matriz.s[1] + 0.001, shrek.matriz.s[2] + 0.001])
        
    if key == 44 and (action==1 or action==2): # tecla "," "<"
        shrek.matriz.change_S([shrek.matriz.s[0] - 0.001, shrek.matriz.s[1] - 0.001, shrek.matriz.s[2] - 0.001])

    if key == 80 and action == 1: polygonal_mode = not polygonal_mode

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

    if pitch >= 90.0: pitch = 89.9
    if pitch <= -90.0: pitch = -89.9

    front = glm.vec3()
    front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    front.y = math.sin(glm.radians(pitch))
    front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    cameraFront = glm.normalize(front)


### Matrizes Model, View e Projection
# Teremos uma aula específica para entender o seu funcionamento.
def model(angle, matriz):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade

    
    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, glm.vec3(matriz.t[0], matriz.t[1], matriz.t[2]))
    
    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, angle, glm.vec3(matriz.r[0], matriz.r[1], matriz.r[2]))
    
    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, glm.vec3(matriz.s[0], matriz.s[1], matriz.s[2]))
    
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


### Inicializando janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
window = glfw.create_window(largura, altura, "Malhas e Texturas", None, None)
glfw.make_context_current(window)

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

fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        
        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            gl_FragColor = texture;
        }
        """


### Requisitando slot para a GPU para nossos programas Vertex e Fragment Shaders
# Request a program and shader slots from GPU
program  = glCreateProgram()
vertex   = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)



### Associando nosso código-fonte aos slots solicitados
# Set shaders source
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)



### Compilando o Vertex Shader
# Se há algum erro em nosso programa Vertex Shader, nosso app para por aqui.
# Compile shaders
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")



### Compilando o Fragment Shader
# Se há algum erro em nosso programa Fragment Shader, nosso app para por aqui.
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")



### Associando os programas compilado ao programa principal
# Attach shader objects to the program
glAttachShader(program, vertex)
glAttachShader(program, fragment)



### Linkagem do programa
# Build program
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
    


# Make program the default program
glUseProgram(program)



### Preparando dados para enviar a GPU
# Nesse momento, nós compilamos nossos Vertex e Program Shaders para que a GPU possa processá-los.
# Por outro lado, as informações de vértices geralmente estão na CPU e devem ser transmitidas para a GPU.
glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )
glEnable(GL_LINE_SMOOTH)
glEnable(GL_TEXTURE_2D)
textures = glGenTextures(qtd_texturas)



### Vamos carregar cada modelo e sua(s) respectiva(s) textura(s)
terreno_pedra = Object('../objects/terreno/terreno.obj', ['../objects/terreno/pedra.jpg'], 0)
terreno_interno = Object('../objects/terreno/terreno.obj', ['../objects/terreno/pedra.jpg'], 0)
house1 = Object('../objects/casa/casa.obj', ['../objects/casa/casa.jpg'], 1)
spiderman = Object('../objects/spiderman/spiderman.obj', ['../objects/spiderman/spiderman.png'], 2)
arvore = Object('../objects/arvore/arvore.obj', ['../objects/arvore/bark_0021.jpg', '../objects/arvore/DB2X2_L01.png'], 3) # TEM UM TRONCO E FOLHA
monstro = Object('../objects/monstro/monstro.obj', ['../objects/monstro/monstro.jpg'], 5)
chair = Object('../objects/chair/chair_01.obj', ['../objects/chair/Textures/chair_01_Base_Color.png'], 6)
yoshi = Object('../objects/yoshi/Yoshi(Super Mario Maker).obj', ['../objects/yoshi/SMMYoshi.png'], 7)
house2 = Object('../objects/squidward/MSH_SquidwardHouse.obj', ['../objects/squidward/TEX_SquidwardHouse.png'], 8)
bed = Object('../objects/SpongeBobBed/MSH_boss3.obj', ['../objects/SpongeBobBed/TEX_boss3_bob.png', '../objects/SpongeBobBed/TEX_boss3_bed.png', '../objects/SpongeBobBed/TEX_boss3_barrel.png'], 9)
sky = Object('../objects/sky/275out.obj', ['../objects/sky/275_lp_di1mt55p.png', '../objects/sky/275_di1mt81p.png'], 12)
field = Object('../objects/field/field.obj', ['../objects/field/76BACB49_c.png', '../objects/field/35BF7BB8_c.png', '../objects/field/32F6789_c.png'], 14)
car = Object('../objects/PoliceCar/policecar.obj', ['../objects/PoliceCar/Tex_0017_0.png'], 17)
shrek = Object('../objects/Shrek/shrek.obj', ['../objects/Shrek/s2.png', '../objects/Shrek/s1.png'], 18)
television = Object('../objects/television/a_prop_TV.obj', ['../objects/television/prop_TV_Lib.tga.png'], 20)
rocket = Object('../objects/Rocket/obj0.obj', ['../objects/Rocket/0.png'], 21)



### Para enviar nossos dados da CPU para a GPU, precisamos requisitar slots.
# Nós agora vamos requisitar dois slots.
# * Um para enviar coordenadas dos vértices.
# * Outros para enviar coordenadas de texturas.
# Request a buffer slot from GPU
buffer = glGenBuffers(2)



###  Enviando coordenadas de vértices para a GPU
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



###  Enviando coordenadas de textura para a GPU
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



### Eventos para modificar a posição da câmera.
# * Usei as teclas A, S, D e W para movimentação no espaço tridimensional
# * Usei a posição do mouse para "direcionar" a câmera

cameraPos   = glm.vec3(-30.0,  5.0,  30.0);
cameraFront = glm.vec3(0.0,  0.0, -1.0);
cameraUp    = glm.vec3(0.0,  1.0,  0.0);

polygonal_mode = False

inc_fov = 0
inc_near = 0
inc_far = 0
inc_view_up = 0
        
firstMouse = True
yaw = -90.0 
pitch = 0.0
lastX =  largura/2
lastY =  altura/2
    
glfw.set_key_callback(window,key_event)
glfw.set_cursor_pos_callback(window, mouse_event)



### Nesse momento, nós exibimos a janela!
glfw.show_window(window)
glfw.set_cursor_pos(window, lastX, lastY)



### Loop principal da janela.
# Enquanto a janela não for fechada, esse laço será executado. É neste espaço que trabalhamos com algumas interações com a OpenGL.
glEnable(GL_DEPTH_TEST) ### importante para 3D



### Setando matrizes iniciais
inc = 0
terreno_pedra.matriz.change_All(
                [0.0, -0.9, -100,0], 
                [0.0, 0.0, 1.0], 
                [4.0, 4.0, 200.0])

field.matriz.change_All(
                [4.0, -1.0, 0,0], 
                [0.0, 0.0, 1.0], 
                [20.0, 20.0, 20.0])

sky.matriz.change_All(
                [0.0, -10.0, 0,0], 
                [1.0, 0.0, 0.0], 
                [5.0, 5.0, 5.0])
sky.change_angle(-90)

spiderman.matriz.change_All(
                [-5.0, -0.9, 30.0],
                [0.0, 1.0, 0.0], 
                [1.0, 1.0, 1.0])
spiderman.change_angle(90)

arvore.matriz.change_All(
                [-10.0, -1.0, 0.0],
                [0.0, 0.0, 1.0], 
                [7.0, 7.0, 7.0])

### CASA E A PARTE INTERNA

house1.matriz.change_All(
                [-30.0, -1.0, 30.0], 
                [0.0, 1.0, 0.0], 
                [1.0, 1.0, 1.0])
house1.change_angle(176)

terreno_interno.matriz.change_All(
                [-28.0, -0.9, 30.0], 
                [0.0, 1.0, 0.0], 
                [15.5, 1.0, 8.1])

chair.matriz.change_All(
                [-30.0, -1.0, 24.0], 
                [0.0, 1.0, 0.0], 
                [5.0, 5.0, 5.0])
                
bed.matriz.change_All(
                [-38.0, -1.0, 31.5], 
                [0.0, 1.0, 0.0], 
                [1.5, 1.5, 1.5])
bed.change_angle(90)

yoshi.matriz.change_All(
                [-25.0, -1.0, 35.0], 
                [0.0, 1.0, 0.0], 
                [3.0, 3.0, 3.0])
yoshi.change_angle(135)

television.matriz.change_All(
                [-15.0, -1.0, 24.0], 
                [0.0, 1.0, 0.0], 
                [0.03, 0.03, 0.03])
television.change_angle(-45)

##################################################

car.matriz.change_All(
                [0.0, -1.0, -100.0],
                [0.0, 1.0, 0.0],
                [0.3, 0.3, 0.3])

house2.matriz.change_All(
                [15.0, -1.0, -10.0], 
                [0.0, 1.0, 0.0], 
                [1.0, 1.0, 1.0])
house2.change_angle(-90)

shrek.matriz.change_All(
                [20.0, -1.0, 20.0], 
                [0.0, 1.0, 0.0], 
                [0.2, 0.2, 0.2])

rocket.matriz.change_All(
                [75.0, 20.0, -50.0], 
                [0.0, 1.0, 0.0], 
                [0.005, 0.005, 0.005])
rocket.change_angle(180)

while not glfw.window_should_close(window):

    inc += 0.02
    # sky.matriz.change_R([1.0, (inc/2), 0.0])
    car.matriz.change_T([0.0, -1.0, (-100.0+inc/1.5)])
    rocket.matriz.change_T([75.0, 20.0, (50.0-inc/2)])
    shrek.change_angle(inc*25)

    glfw.poll_events() 
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    
    if polygonal_mode: glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    if not polygonal_mode: glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    field.desenha(model, program)
    sky.desenha(model, program)
    terreno_pedra.desenha(model, program)

    house1.desenha(model, program)
    terreno_interno.desenha(model, program)
    chair.desenha(model, program)
    bed.desenha(model, program)
    yoshi.desenha(model, program)
    television.desenha(model,program)

    spiderman.desenha(model, program)   
    house2.desenha(model, program)
    car.desenha(model, program)
    shrek.desenha(model, program)
    rocket.desenha(model, program)

    for i in range(5):        
        arvore.matriz.change_T([arvore.matriz.t[0], arvore.matriz.t[1], i*20])
        arvore.desenha(model, program)
        arvore.matriz.change_T([arvore.matriz.t[0], arvore.matriz.t[1], i*(-20)])
        arvore.desenha(model, program)

    
    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    glfw.swap_buffers(window)

glfw.terminate()
