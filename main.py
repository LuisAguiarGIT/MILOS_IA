#!/usr/bin/env python3
# BIBLIOTECAS #
from time import sleep
from array import *

from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedRPS, MoveTank
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor
from ev3dev2.sound import Sound

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
ROTACOES_VERIF = 1.3
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

def move_atras_1_casa(motor_esquerda, motor_direita, rotacoes):
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
def procura_peca(sensor_us, motor_esquerda, motor_direita, rotacoes):
    global xPos, yPos
    mv_dir = MoveTank(motor_esquerda, motor_direita)
    detetou = 0

    # Se estamos em alguma posição onde x = 0, quer dizer que só precisamos de verificar a célula acima (y+1) ou então a célula ao lado (x+1)
    if xPos == 0:
        mv_dir.on_for_rotations(10, 10, rotacoes)
        if deteta_parede(sensor_us):
            mv_dir.on_for_rotations(-10, -10, rotacoes)

# Esta função serve para determinar se existe alguma ovelha por trás da parede
def parede_ovelha()


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

procura_peca(us, MOTOR_ESQ, MOTOR_DIR, ROTACOES_VERIF)

while(1):
    sleep(1)



