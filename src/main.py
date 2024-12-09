#!/usr/bin/env python
# coding: utf-8

# Dupla: Fabricio Sampaio     NUSP: 12547423
#        Vitor Nishimura Vian NUSP: 5255289

from globals import *
from sprites import Object, Material

qtd_texturas = 25
altura = 1600
largura = 1900

min_x, max_x = -80, 80
min_y, max_y = 5,50
min_z, max_z = -80,80

lantern_on = True

inc_amb = inc_spec = inc_dif = 0.6

# Função que não permite o usuário passar do extremos no mapa 
def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def normalize(vector):
    return vector / np.linalg.norm(vector)


### Eventos para modificar a posição da câmera.
# * Usei as teclas A, S, D e W para movimentação no espaço tridimensional
# * Usei a posição do mouse para "direcionar" a câmera
def key_event(window,key,scancode,action,mods):
    global cameraPos, cameraFront, cameraUp, polygonal_mode, inc_fov, inc_near, inc_far, cameraUp, inc_view_up, lantern_on, inc_amb, inc_dif, inc_spec

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
        cameraPos -= normalize(np.cross(cameraFront, cameraUp)) * cameraSpeed
        
    if key == 68 and (action==1 or action==2): # tecla D
        cameraPos += normalize(np.cross(cameraFront, cameraUp)) * cameraSpeed

    cameraPos[0] = clamp(cameraPos[0], min_x, max_x)  # x -> índice 0
    cameraPos[1] = clamp(cameraPos[1], min_y, max_y)  # y -> índice 1
    cameraPos[2] = clamp(cameraPos[2], min_z, max_z)  # z -> índice 2


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

    #Tecla L, alternar lanterna ligada ou desligada
    if key == 76 and action == 1: lantern_on = not lantern_on

    # tecla 1 diminui iluminação ambiental e 2 aumenta
    if key == 49 and (action == 1 or action == 2) : inc_amb -=0.1
    if key == 50 and (action == 1 or action == 2) : inc_amb +=0.1

    # tecla 3 diminui iluminação difusa e 4 aumenta
    if key == 51 and (action == 1 or action == 2) : inc_dif -=0.1
    if key == 52 and (action == 1 or action == 2) : inc_dif +=0.1

    # tecla 5 diminui iluminação ambiental e 6 aumenta
    if key == 53 and (action == 1 or action == 2) : inc_spec -=0.1
    if key == 54 and (action == 1 or action == 2) : inc_spec +=0.1

    inc_amb = clamp(inc_amb, 0.0, 50)
    inc_dif = clamp(inc_dif, 0.0, 50)
    inc_spec = clamp(inc_spec, 0.0, 50)



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




    pitch = clamp(pitch, -60.0, 60.0)  # Limitar o pitch
    front = np.array([
        math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
        math.sin(math.radians(pitch)),
        math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    ], dtype=np.float32)
    cameraFront = normalize(front)






### Matrizes Model, View e Projection
# Teremos uma aula específica para entender o seu funcionamento.
def model(angle, matriz):
    
    matrix_transform = mat4_identity()
    matrix_transform = translate(matrix_transform, matriz.t)
    matrix_transform = rotate(matrix_transform, angle, matriz.r)
    matrix_transform = scale(matrix_transform, matriz.s)
    
    return matrix_transform

def view():
    return lookAt(cameraPos, cameraPos + normalize(cameraFront), cameraUp)


def projection():
    global altura, largura, inc_fov, inc_near, inc_far
    # perspective parameters: fovy, aspect, near, far
    return perspective(45.0, largura / altura, 0.1, 1000.0)

### Inicializando janela
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
window = glfw.create_window(largura, altura, "Malhas e Texturas", None, None)
glfw.make_context_current(window)

vertex_code = """

        #version 330 core

        attribute vec3 position;
        attribute vec2 texture_coord;
        attribute vec3 normals;

        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = texture_coord;
            out_fragPos = vec3(model * vec4(position, 1.0));
            out_normal = mat3(transpose(inverse(model))) * normals;
        }
        """

fragment_code = """

        #version 330 core
        uniform bool lantern_on;

        uniform vec3 lightPos1;
        vec3 lightColor1 = vec3(1.0, 1.0, 1.0);

        uniform vec3 lightPos2;
        uniform vec3 lightColor2;

        uniform vec3 lightPos3;
        vec3 lightColor3 = vec3(1.0, 1.0, 0.7);


        uniform float ka;
        uniform float kd;
        uniform float ks;
        uniform float ns;

        uniform float inc_amb;
        uniform float inc_spec;
        uniform float inc_dif;

        uniform vec3 viewPos;

        varying vec2 out_texture;
        varying vec3 out_normal;
        varying vec3 out_fragPos;
        uniform sampler2D samplerTexture;

        uniform bool is_inside;

        void main(){

        vec3 interior_amb = ka * lightColor3 * inc_amb;
        vec3 exterior_amb = ka * lightColor1 * inc_amb;

            // LUZ 1 - LUZ DO PERSONAGEM (LANTERNA)
            vec3 lightDir = lightPos1 - out_fragPos;
            float lightDistance = length(lightDir);

            lightDir = lightDir / lightDistance;
            vec3 norm = normalize(out_normal);
            vec3 viewDir = normalize(viewPos - out_fragPos);
            float attenuation = 1.0 / (0.005 * (lightDistance * lightDistance));

            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse1 = kd * diff * lightColor1 * attenuation * (lantern_on ? 1.0 : 0.0) * inc_dif;

            vec3 reflectDir = normalize(reflect(-lightDir, norm));
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular1 = ks * spec * lightColor1 * attenuation * (lantern_on ? 1.0 : 0.0) * inc_spec;

            // LUZ 2 - LUZ DA POLICIA (GIROFLEX)
            lightDir = lightPos2 - out_fragPos;
            lightDistance = length(lightDir);

            lightDir = lightDir / lightDistance;
            viewDir = normalize(viewPos - out_fragPos);
            attenuation = 1.0 / (0.0025 * (lightDistance * lightDistance));

            diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse2 = 0.5 * diff * lightColor2 * attenuation * inc_dif;

            reflectDir = normalize(reflect(-lightDir, norm));
            spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular2 = 0.01 * spec * lightColor2 * attenuation * inc_spec;


            // LUZ 3 - LUZ INTERNA
            lightDir = (lightPos3 - out_fragPos);
            lightDistance = length(lightDir);

            lightDir = lightDir / lightDistance;
            viewDir = normalize(viewPos - out_fragPos);
            attenuation = 1.0 / (0.0025 * (lightDistance * lightDistance));

            diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse3 = kd * diff * lightColor3 * attenuation * inc_dif;

            reflectDir = normalize(reflect(-lightDir, norm));
            spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular3 = 0.01 * spec * lightColor3 * attenuation * inc_spec;

            // ADICIONANDO AS LUZES NOS OBJETOS
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec3 lighting1 = diffuse1 + specular1;
            vec3 lighting2 = diffuse2 + specular2;
            vec3 lighting3 = diffuse3 + specular3;

            vec3 lighting;
            if(!is_inside){
                lighting = lighting1 + lighting2 + exterior_amb;
            }else{
                lighting = lighting1 + lighting3 + interior_amb;
            }
            vec4 result = vec4(lighting,1.0) * texture;
            gl_FragColor = result;
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


#Definindo materiais
madeira = Material("madeira", 0.1, 0.6, 0.05, 15)
metal = Material("metal", 0.05, 0.3, 0.9, 200)
tecido = Material("tecido", 0.15, 0.7, 0.1, 10)
pedra = Material("pedra", 0.2, 0.6, 0.1, 15)
pele = Material("pele", 0.15, 0.7, 0.3, 50)
ceu = Material("céu", 0.5, 0.001, 0.001, 10)
grama = Material("grama", 0.25, 0.7, 0.15, 20)

### Vamos carregar cada modelo e sua(s) respectiva(s) textura(s)
terreno_pedra = Object('../objects/terreno/terreno.obj', ['../objects/terreno/caminho_tijolo.jpg'], 0, pedra)
terreno_interno = Object('../objects/terreno/terreno.obj', ['../objects/terreno/pedra.jpg'], 30,pedra, True)
house1 = Object('../objects/casa/casa1.obj', ['../objects/casa/casa.jpg'], 1, madeira)
house_interior = Object('../objects/casa/casa_interior.obj', ['../objects/casa/casa.jpg'], 1, madeira, True)
spiderman = Object('../objects/spiderman/spiderman.obj', ['../objects/spiderman/spiderman.png'],2, tecido)
arvore = Object('../objects/arvore/arvore.obj', ['../objects/arvore/bark_0021.jpg', '../objects/arvore/DB2X2_L01.png'], 3, madeira)
chair = Object('../objects/chair/chair_01.obj', ['../objects/chair/Textures/chair_01_Base_Color.png'], 6, madeira, True)
yoshi = Object('../objects/yoshi/Yoshi(Super Mario Maker).obj', ['../objects/yoshi/SMMYoshi.png'], 7, pele, True)
house2 = Object('../objects/squidward/MSH_SquidwardHouse.obj', ['../objects/squidward/TEX_SquidwardHouse.png'], 8, pedra)
bed = Object('../objects/SpongeBobBed/MSH_boss3.obj', ['../objects/SpongeBobBed/TEX_boss3_barrel.png', '../objects/SpongeBobBed/TEX_boss3_bed.png', '../objects/SpongeBobBed/TEX_boss3_bob.png'], 9,tecido, True)
sky = Object('../objects/sky/275out.obj', ['../objects/sky/275_lp_di1mt55p.png', '../objects/sky/275_di1mt81p.png'], 12, ceu)
field = Object('../objects/field/field1.obj'    , ['../objects/field/76BACB49_c.png', '../objects/field/35BF7BB8_c.png', '../objects/field/32F6789_c.png'], 14, grama)
car = Object('../objects/PoliceCar/policecar.obj', ['../objects/PoliceCar/Tex_0017_0.png'], 17, metal)
shrek = Object('../objects/Shrek/shrek1.obj', ['../objects/Shrek/s1.png', '../objects/Shrek/s2.png'], 18, tecido)
television = Object('../objects/television/a_prop_TV1.obj', ['../objects/television/prop_TV_Lib.tga.png'], 20,metal, True)
rocket = Object('../objects/Rocket/obj0.obj', ['../objects/Rocket/0.png'], 21, metal)
star = Object('../objects/star/star.obj', ['../objects/star/star.png'], 23, metal, True)


### Para enviar nossos dados da CPU para a GPU, precisamos requisitar slots.
# Nós agora vamos requisitar tres slots.
# Um para enviar coordenadas dos vértices.
# Um para enviar coordenadas de texturas.
# Um para enviar coordenadas de normals para iluminacao.
buffer = glGenBuffers(3)



###  Enviando coordenadas de vértices para a GPU
vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
vertices['position'] = vertices_list
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
glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
stride = textures.strides[0]
offset = ctypes.c_void_p(0)
loc_texture_coord = glGetAttribLocation(program, "texture_coord")
glEnableVertexAttribArray(loc_texture_coord)
glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)



###  Enviando coordenadas da normal para a GPU
normals = np.zeros(len(normals_list), [("position", np.float32, 3)]) # três coordenadas
normals['position'] = normals_list
glBindBuffer(GL_ARRAY_BUFFER, buffer[2])
glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
stride = normals.strides[0]
offset = ctypes.c_void_p(0)
loc_normals_coord = glGetAttribLocation(program, "normals")
glEnableVertexAttribArray(loc_normals_coord)
glVertexAttribPointer(loc_normals_coord, 3, GL_FLOAT, False, stride, offset)



### Eventos para modificar a posição da câmera.
# * Usei as teclas A, S, D e W para movimentação no espaço tridimensional
# * Usei a posição do mouse para "direcionar" a câmera

cameraPos = np.array([-30.0, 5.0, 30.0], dtype=np.float32)
cameraFront = np.array([0.0, 0.0, -1.0], dtype=np.float32)
cameraUp = np.array([0.0, 1.0, 0.0], dtype=np.float32)

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
                [2.0, 0.1, 45.0])

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

star.matriz.change_All(
                [-30.0, 8.0, 30.0], 
                [0.0, 1.0, 0.0],
                [0.1, 0.1, 0.1])
star.change_angle(86)

house_interior.matriz.change_All(
                [-30.0, -0.98, 30.0], 
                [0.0, 1.0, 0.0],
                [0.99, 0.99, 0.99])
house_interior.change_angle(176)


terreno_interno.matriz.change_All(
                [-28.0, -0.9, 30.0], 
                [0.0, 1.0, 0.0], 
                [5.0, 0.1, 1.9])

chair.matriz.change_All(
                [-30.0, -1.0, 24.0], 
                [0.0, 1.0, 0.0], 
                [4.8, 5.0, 5.0])

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
                [0.0, -1.0, -60.0],
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

color_cnt = 0
color_change = False

while not glfw.window_should_close(window):

    inc += 0.05
    color_cnt += 1

    car.matriz.change_T([0.0, -1.0, (-100.0+inc/2)])
    rocket.matriz.change_T([75.0, 20.0, (50.0-inc/3)])
    shrek.change_angle(inc*20)

    glfw.poll_events() 
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Atualiza estado da lanterna
    loc_lantern_on = glGetUniformLocation(program, "lantern_on")
    glUniform1i(loc_lantern_on, int(lantern_on))

    # Atualiza estado dos inc das iluminações

    loc_inc_amb = glGetUniformLocation(program, "inc_amb")
    glUniform1f(loc_inc_amb, inc_amb)

    loc_inc_dif = glGetUniformLocation(program, "inc_dif")
    glUniform1f(loc_inc_dif, inc_dif)

    loc_inc_spec = glGetUniformLocation(program, "inc_spec")
    glUniform1f(loc_inc_spec, inc_spec)





    
    if polygonal_mode: glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    if not polygonal_mode: glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    field.desenha(model, program)
    sky.desenha(model, program)
    terreno_pedra.desenha(model, program)

    house1.desenha(model, program)
    star.desenha(model, program)
    house_interior.desenha(model,program)
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

    loc_light_pos1 = glGetUniformLocation(program, "lightPos1")
    glUniform3f(loc_light_pos1, cameraPos[0], cameraPos[1], cameraPos[2])

    loc_light_pos2 = glGetUniformLocation(program, "lightPos2")
    glUniform3f(loc_light_pos2, car.matriz.t[0], car.matriz.t[1], car.matriz.t[2])

    loc_light_pos3 = glGetUniformLocation(program, "lightPos3")
    glUniform3f(loc_light_pos3,star.matriz.t[0], star.matriz.t[1], star.matriz.t[2])

    if color_cnt % 50 == 0: color_change = not color_change

    loc_light_color2 = glGetUniformLocation(program, "lightColor2")
    if color_change: glUniform3f(loc_light_color2, 1.0, 0.0, 0.0)
    else: glUniform3f(loc_light_color2, 0.0, 0.0, 1.0)

    mat_view = view()
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

    mat_projection = projection()
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
    
    loc_view_pos = glGetUniformLocation(program, "viewPos")
    glUniform3f(loc_view_pos, cameraPos[0], cameraPos[1], cameraPos[2])

    glfw.swap_buffers(window)

glfw.terminate()
