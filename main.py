#!/usr/bin/env python3
# BIBLIOTECAS #
from time import sleep
from array import *
from collections import OrderedDict

from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedRPS, MoveTank, MoveSteering
from ev3dev2.sensor import INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
from ev3dev2.sound import Sound
from sys import stderr

import robot.py
import heuristicas.py

# =============================================================================== #
# ASPETOS GERAIS DO JOGO / ROBOT                                                  #
# =============================================================================== #
# 0 indica que existe uma ovelha na célula, True indica que existe uma parede

class Jogo:

    def __init__(self):
        self.n_ovelhas = 2
        self.matriz = []
    
    def preenche_matriz(self):
        for x in range(6):
            lista_interior = []
            for y in range(6):
                lista_interior.append(Cell())
            self.matriz.append(lista_interior)
    
    def imprime_matriz(self):
        out = ""
        for listas in self.matriz:
            for i in listas:
                out += str(i.conteudo)
            out += "\n"
        
        print(out, file=stderr)
        
class Cell:

    def __init__(self):
        self.parede_esq = False
        self.parede_acim = False
        self.parede_dir = False
        self.parede_abaix = False
        self.conteudo = "#"
        self.visitado = False

# Criação de constantes
ROTACOES_CASA = 2.1
MOTOR_ESQ = OUTPUT_D
MOTOR_DIR = OUTPUT_C
VELOCIDADE_PROCURA = 20
# Criação dos objetos

# Programa
jg = Jogo()
rb = Robot()

# Sensores/ Robot
voice = Sound()
us = UltrasonicSensor()
steer_pair = MoveSteering(OUTPUT_D, OUTPUT_C)
mv_dir = MoveTank(MOTOR_ESQ, MOTOR_DIR)
cl = ColorSensor()
confirm = TouchSensor(INPUT_4)
det_touch = TouchSensor(INPUT_3)

# Atribuição de modos aos sensores 
us.mode = 'US-DIST-CM'
units = us.units

jg.preenche_matriz()
jg.imprime_matriz()

while(jg.n_ovelhas > 0):
    # Heurística
