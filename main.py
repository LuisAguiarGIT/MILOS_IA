#!/usr/bin/env python3
# BIBLIOTECAS #
from time import sleep
from array import *

from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedRPS, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
from ev3dev2.sound import Sound
import os 

os.system('setfont Lat15-TerminusBold14')

# ================== #
# Definicao de dados #
# ================== #

global matriz
matriz = []
global xPos, yPos
xPos = 0
yPos = 0

# =================== #
# Orientação do robot #
# =================== #

orientacoes = ["Norte", "Este", "Sul", "Oeste"]
ori_index = 0
orientacao_robot = orientacoes[ori_index]

# Constantes relevantes
ROTACOES_NOV_GRAUS = 1.3
ROTACOES_CASA = 2.1
ROTACOES_VERIF = 0.7
VELOCIDADE_PROCURA = 20
MOTOR_ESQ = OUTPUT_D
MOTOR_DIR = OUTPUT_C

# =================== #
# Criacao de objetos  #
# =================== #

voice = Sound()
# ev3 = EV3Brick()
us = UltrasonicSensor()
us.mode = 'US-DIST-CM'
units = us.units
steer_pair = MoveSteering(OUTPUT_D, OUTPUT_C)
cl = ColorSensor()
# confirm = TouchSensor(INPUT_4)
# det_toq = TouchSensor(INPUT_3)

# =================================== #
# Definicao de funcoes para debugging #
# =================================== #

# Irá, como o nome indica, preencher a matriz com cardinal. Cardinal indica que a posicao está vazia
def preenche_matriz(matriz):
    for x in range(6):
        lista_interior = []
        for y in range(6):
            lista_interior.append("#")
        matriz.append(lista_interior)

# Simplesmente imprime a matriz para fins de debugging
def imprime_matriz(matriz):
    for listas in matriz:
        for i in listas:
            print(i,end='\t')
        print()

def atualiza_orientacao(array, index, orientacao):
    # Isto serve para "voltar ao início" do array para atualizar a orientação
    return array[index % len(array)]

def atualiza_posicao_eixo_y(orientacao):
    global yPos

    if orientacao == "Norte":
        return yPos + 1
    
    if orientacao == "Sul":
        return yPos - 1

def atualiza_posicao_eixo_x(orientacao):
    global xPos

    if orientacao == "Este":
        return xPos + 1
    
    if orientacao == "Oeste":
        return xPos - 1
        
# ==================== #
# Funcoes de movimento #
# ==================== #

def move_frente_casa(motor_esquerda, motor_direita, rotacoes, orientacao):
    # global posicao
    global xPos, yPos

    mv_fr = MoveTank(motor_esquerda, motor_direita)
    # Primeiro e segundo parâmetro são a velocidade dos motores, o terceiro sendo o numero de rotacoes
    mv_fr.on_for_rotations(25,25, rotacoes)
    # posicao = atualiza_posicao(posicao, orientacao)

    if orientacao == "Norte" or orientacao == "Sul":
        yPos = atualiza_posicao_eixo_y(orientacao)
    else:
        xPos = atualiza_posicao_eixo_x(orientacao)

def move_atras_casa(motor_esquerda, motor_direita, rotacoes):
    mv_fr = MoveTank(motor_esquerda, motor_direita)
    # Primeiro e segundo parâmetro são a velocidade dos motores, o terceiro sendo o numero de rotacoes
    mv_fr.on_for_rotations(-25,-25, rotacoes)

def vira_direita(motor_esquerda, motor_direita, rotacoes, index):
    # Funções para mover o robot
    mv_dir = MoveTank(motor_esquerda, motor_direita)
    mv_dir.on_for_rotations(25,-25, rotacoes)
    # Atualizamos o indice para a orientacao do robot
    return index + 1

def vira_esquerda(motor_esquerda, motor_direita, rotacoes, index):
    # Funções para mover o robot
    mv_dir = MoveTank(motor_esquerda, motor_direita)
    mv_dir.on_for_rotations(-25,25, rotacoes)
    # Atualizamos o indice para a orientacao do robot
    return index - 1

# Funções para virar o robot sem atualizar a sua orientação
def vira_dir_sem_indice(motor_esquerda, motor_direita, rotacoes):
    mv_dir = MoveTank(motor_esquerda, motor_direita)
    mv_dir.on_for_rotations(25,-25, rotacoes)

def vira_esq_sem_indice(motor_esquerda, motor_direita, rotacoes):
    mv_dir = MoveTank(motor_esquerda, motor_direita)
    mv_dir.on_for_rotations(25,-25, rotacoes)

def desloca_posicao_y(sensor_us, destino_y,
motor_esquerda, motor_direita, rotacoes_casa,
rotacoes_virar, array, matriz):
    global ori_index, orientacao_robot

    while(yPos < destino_y):

        while (orientacao_robot != "Norte"):
            ori_index = vira_direita(motor_esquerda, motor_direita, rotacoes_virar, ori_index)
            orientacao_robot = atualiza_orientacao(array, ori_index, orientacao_robot)
            print(orientacao_robot)

        # procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, matriz, ori_index)
        procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, matriz)
        move_frente_casa(motor_esquerda, motor_direita, rotacoes_casa, orientacao_robot)
    
    # Verifica se a posição do robot é maior do que o destino
    while(yPos > destino_y):

        while(orientacao_robot != "Sul"):
            ori_index = vira_direita(motor_esquerda, motor_direita, rotacoes_virar, ori_index)
            orientacao_robot = atualiza_orientacao(array, ori_index, orientacao_robot)
            print(orientacao_robot)

        procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, matriz)
        move_frente_casa(motor_esquerda, motor_direita, rotacoes_casa, orientacao_robot)

def desloca_posicao_x(sensor_us, destino_x,
motor_esquerda, motor_direita, rotacoes_casa,
rotacoes_virar, array, matriz):
    global ori_index, orientacao_robot, xPos, yPos

    while(xPos < destino_x):

        while (orientacao_robot != "Este"):
            ori_index = vira_direita(motor_esquerda, motor_direita, rotacoes_virar, ori_index)
            orientacao_robot = atualiza_orientacao(array, ori_index, orientacao_robot)
            print(orientacao_robot)

        # procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, matriz, ori_index)
        procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, matriz)
        move_frente_casa(motor_esquerda, motor_direita, rotacoes_casa, orientacao_robot)
    
    # Verifica se a posição do robot é maior do que o destino
    while(xPos > destino_x):

        while(orientacao_robot != "Oeste"):
            ori_index = vira_direita(motor_esquerda, motor_direita, rotacoes_virar, ori_index)
            orientacao_robot = atualiza_orientacao(array, ori_index, orientacao_robot)
            print(orientacao_robot)

        procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, matriz)
        move_frente_casa(motor_esquerda, motor_direita, rotacoes_casa, orientacao_robot)

def desloca_para_coor(sensor_us, destino_x, destino_y,
motor_esquerda, motor_direita, rotacoes_casa,
rotacoes_virar, array, matriz):
    global ori_index, orientacao_robot, xPos, yPos

    desloca_posicao_y(sensor_us, destino_y, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, array, matriz)
    desloca_posicao_x(sensor_us, destino_x, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, array, matriz)

    while(orientacao_robot != "Norte"):
        ori_index = vira_direita(motor_esquerda, motor_direita, rotacoes_virar, ori_index)
        orientacao_robot = atualiza_orientacao(array, ori_index, orientacao_robot)


# =================== #
# Funcoes de sensores #
# =================== #

def deteta_parede(sensor_us):
        distance = sensor_us.value()/10 # converter mm para cm
        # print(str(distance) + " " + units)
        if distance < 20:
            voice.speak("Something here!")
            return True

# def deteta_toque(sensor_toq):
#     while True:
#         if sensor_toq.is_pressed:
#             move_frente(OUTPUT_D, OUTPUT_C, ROTACOES_CASA)

# Esta verificação é feita constantemente para procurar alguma peça, parede ou ovelha
# SENSOR ULTRASÓNICO # 
def procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes_casa, rotacoes_virar, matriz):
    global xPos, yPos
    mv_dir = MoveTank(motor_esquerda, motor_direita)

    # Se estamos em alguma posição onde x = 0, quer dizer que só precisamos de verificar a célula acima (y+1) ou então a célula ao lado (x+1)
    # if xPos == 0:

    # Procurar peças diretamente à frente do robot
    mv_dir.on_for_rotations(20, 20, rotacoes_casa)

    if deteta_parede(sensor_us):
        # Voltar à posição original
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)
        # Iniciar ler a lista de peças
        # TODO
        check_colour()

    else:
        # Voltar à posição inicial
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)

    # Procurar peças diretamente à direita do robot
    vira_dir_sem_indice(motor_esquerda, motor_direita, rotacoes_virar)
    mv_dir.on_for_rotations(20, 20, rotacoes_casa)

    if deteta_parede(sensor_us):
        # Voltar à posição original
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)
        # Iniciar ler a lista de peças
        # TODO
    else:
        # Voltar à posição inicial
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)
    
    # Procurar peças diretamente abaixo do robot
    vira_dir_sem_indice(motor_esquerda, motor_direita, rotacoes_virar)
    mv_dir.on_for_rotations(20, 20, rotacoes_casa)

    if deteta_parede(sensor_us):
        # Voltar à posição original
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)
        # Iniciar ler a lista de peças
        # TODO
    else:
        # Voltar à posição inicial
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)
    
    # Procurar peças diretamente à esquerda do robot
    vira_dir_sem_indice(motor_esquerda, motor_direita, rotacoes_virar)
    mv_dir.on_for_rotations(20, 20, rotacoes_casa)

    if deteta_parede(sensor_us):
        # Voltar à posição original
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)

        # Iniciar ler a lista de peças
        # TODO
    else:
        # Voltar à posição inicial
        mv_dir.on_for_rotations(-20, -20, rotacoes_casa)

    vira_dir_sem_indice(motor_esquerda, motor_direita, rotacoes_virar)

# SENSOR DE CORES #

def cor_rgb():

    #intervalos RGB para cada cor utilizada, garantindo que o sensor reconheça a cor correta o maior numero de vezes
    r = cl.rgb[0]
    g = cl.rgb[1]
    b = cl.rgb[2]

    if r >= 200 and g <= 60 and b <= 60:
        color = 'red'
    elif r >= 40 and r <= 70 and g >= 40 and g <= 80 and b >= 70:
        color = 'blue'
    elif r >= 50 and r <= 80 and g >= 100 and b <= 70 and b >= 25:
        color = 'green'
    else:
        color = cor_rgb()

    return color

def check_colour():
    steer_pair.on(steering=0, speed=VELOCIDADE_PROCURA) 
    sleep(0.3)

    cor = cor_rgb()
    while cor != 'red': #anda em frente até encontrar a cor vermelha -- Fim da lista
        cor = cor_rgb()
        if cor == 'green' or cor == 'blue': #caso seja uma cor respresentativa de uma peça, adiciona a peça à lista
            print (cor)

            while cor != 'white': #enquanto nao encontrar a cor branca não adiciona peças a lista (para não ler varias vezes a mesma cor)
                cor = cor_rgb()

    steer_pair.off()
    move_to_start()

def move_to_start():
    #anda paa tras até encontrar cor vermelha
    steer_pair.on(steering=0, speed=-VELOCIDADE_PROCURA)
    sleep(0.3) #sleep para nao parar caso comece na cor vermelha que representa o fim da lista de peças
    
    cor = cor_rgb()
    
    while cor != 'red':
        cor = cor_rgb()   


    steer_pair.off()

# Esta função serve para determinar se existe alguma ovelha por trás da parede
# def parede_ovelha()

# =================== #
#      DEBUGGING      #
# =================== #

# print(xPos, yPos)
# move_frente_casa(MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA, orientacao_robot)
# print(xPos, yPos)
# ori_index = vira_direita(MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA, ori_index)
# print(ori_index)
# orientacao_robot = atualiza_orientacao(orientacoes, ori_index, orientacao_robot)
# print(orientacao_robot)
# move_frente_casa(MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA, orientacao_robot)
# print(xPos, yPos)

# procura_peca(us, MOTOR_ESQ, MOTOR_DIR, ROTACOES_VERIF)
# preenche_matriz(matriz)
# imprime_matriz(matriz)
# print("\n")

# procura_peca(us, MOTOR_ESQ, MOTOR_DIR,
# ROTACOES_CASA, ROTACOES_NOV_GRAUS, matriz, ori_index)

imprime_matriz(matriz)
print("\n")
preenche_matriz(matriz)

# desloca_posicao(us, 3, 3,
# MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA,
# ROTACOES_NOV_GRAUS, orientacoes, matriz)

# desloca_posicao(us, 1, 1,
# MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA,
# ROTACOES_NOV_GRAUS, orientacoes, matriz)

desloca_para_coor(us, 3, 3,
MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA,
ROTACOES_NOV_GRAUS, orientacoes, matriz)

desloca_para_coor(us, 0, 0,
MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA,
ROTACOES_NOV_GRAUS, orientacoes, matriz)

while(1):
    sleep(1)
