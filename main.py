#!/usr/bin/env python3
# BIBLIOTECAS #
from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedRPS, MoveTank
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor

# ================== #
# Definicao de dados #
# ================== #

# matriz = []

# Posição robot
matriz = []

# Orientação do robot
orientacoes = ["Norte", "Este", "Sul", "Oeste"]
ori_index = 0
orientacao_robot = orientacoes[ori_index]

# Constantes relevantes
ROTACOES_NOV_GRAUS = 1.3
ROTACOES_CASA = 2.1
MOTOR_ESQ = OUTPUT_D
MOTOR_DIR = OUTPUT_C

# ============================ #
# Definicao da classe de robot #
# ============================ #

# class Robot:
#     def __init__(self, orientacao, posicao, ovelhas):
#     self.orientacao = orientacao  
#     self.posicao = posicao
#     self.ovelhas = ovelhas 

# =================== #
# Criacao de objetos  #
# =================== #

# ev3 = EV3Brick()
# robot = Robot(orientacoes[0], matriz[0][0], 2)
# us = UltrasonicSensor()
# us.mode = 'US-DIST-CM'
# units = us.units
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
    # Isto serve para "voltar ao início" para atualizar a orientação
    return array[index % len(array)]


# def lista_circular(lista):


# ==================== #
# Funcoes de movimento #
# ==================== #

def move_frente(motor_esquerda, motor_direita, rotacoes, matriz_posic, posicao):
    mv_fr = MoveTank(motor_esquerda, motor_direita)
    # Primeiro e segundo parâmetro são a velocidade dos motores, o terceiro sendo o numero de rotacoes
    mv_fr.on_for_rotations(25,25, rotacoes)
    return posicao + 7

def move_atras(motor_esquerda, motor_direita, rotacoes):
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

# def deteta_parede(sensor_us):
#     while True:
#         distance = sensor_us.value()/10 # converter mm para cm
#         print(str(distance) + " " + units)
#         if distance < 12:
#             move_atras(OUTPUT_D, OUTPUT_C, ROTACOES_CASA)

# def deteta_toque(sensor_toq):
#     while True:
#         if sensor_toq.is_pressed:
#             move_frente(OUTPUT_D, OUTPUT_C, ROTACOES_CASA)


# move_frente(MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA, posicao)~
# while(1):
    # ori_index = vira_direita(MOTOR_ESQ, MOTOR_DIR, ROTACOES_NOV_GRAUS, ori_index)
    # orientacao_robot = atualiza_orientacao(orientacoes, ori_index, orientacao_robot)
    # print(orientacao_robot)

    # posicao = move_frente(MOTOR_ESQ, MOTOR_DIR, ROTACOES_CASA, matriz, posicao)
    # print(posicao)




