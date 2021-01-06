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


# ========================================================== #
# ASPETOS GERAIS DO JOGO / ROBOT                             #
# ========================================================== #
# 0 indica que existe uma ovelha na célula, True indica que existe uma parede
# 
#
#
#
#
#
#
#

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
        for listas in self.matriz:
            for i in listas:
                print(i.conteudo,end='\t')
            print()
        
class Cell:

    def __init__(self):
        self.parede_esq = False
        self.parede_acim = False
        self.parede_dir = False
        self.parede_abaix = False
        self.conteudo = "#"

class Robot:

    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.orientacoes = ["Norte", "Este", "Sul", "Oeste"]
        self.ori_index = 0
        self.orientacao_robot = self.orientacoes[self.ori_index]
        self.jogadas = 2
    
    def vira_esquerda(self):
        self.ori_index -= 1
        self.orientacao = self.atualiza_orientacao()
    
    def vira_direita(self):
        self.ori_index += 1
        self.orientacao = self.atualiza_orientacao()

    def atualiza_orientacao(self):
        self.orientacao_robot = self.orientacoes[self.ori_index % len(self.orientacoes)]
    
    def cor_rgb():

        #intervalos RGB para cada cor utilizada, garantindo que o sensor reconheça a cor correta o maior numero de vezes
        r = cl.rgb[0]
        g = cl.rgb[1]
        b = cl.rgb[2]

        if r >= 200 and g <= 60 and b <= 60:
            cor = 'red'
        elif r <= 35 and g <= 35 and b <= 35 :
            cor = 'black'
        elif r >= 210 and g >= 210 and b >= 140:
            cor = 'white'
        else:
            cor = cor_rgb()

        return cor
    
    
    def verifica_cor(self, matriz, us):
        steer_pair.on(steering=0, speed=VELOCIDADE_PROCURA) 
        sleep(0.3)

        cor = cor_rgb()
        while cor != 'red' or cor != 'black': 

            cor = cor_rgb()
            if cor == 'red': 
                print (cor)
                # Tem de assinalar a parede
                assinala_parede(matriz)
                # Começa a leitura para ver se existe uma ovelha
                if deteta_ovelha(us):
                    assinala_ovelha(matriz)

            if cor == 'black'
                print (cor)
                # Está livre
                # Começa a leitura para ver se existe uma ovelha
                if deteta_ovelha(us):
                    assinala_ovelha(matriz)

                while cor != 'white': 
                    cor = cor_rgb()

    def move_frente(self, matriz):
        prox_pos_y = matriz[self.y_pos + 1][self.x_pos]
        prox_pos_x = matriz[self.y_pos][self.x_pos + 1]
        pos_ant_y = matriz[self.y_pos - 1][self.x_pos]
        pos_ant_y = matriz[self.y_pos][self.x_pos - 1]
        
        if(self.orientacao_robot == "Norte"):

            if prox_pos_y.parede_abaix == True:
                print("Tem parede!")
                # Rotina de desvio
            else:
                # Move-se
                
                # Atualiza posição
                self.y_pos += 1

        if(self.orientacao_robot == "Este"):

            if prox_pos_x.parede_esq == True:
                print("Tem parede!")
                # Rotina de desvio
            else:
                # Move-se
                
                # Atualiza posição
                self.x_pos += 1

        if(self.orientacao_robot == "Sul"):

            if prox_ant_y.parede_acim == True:
                print("Tem parede!")
                # Rotina de desvio
            else:
                # Move-se
                
                # Atualiza posição
                self.y_pos -= 1

        if(self.orientacao_robot == "Oeste"):

            if prox_ant_x.parede_esq == True:
                print("Tem parede!")
                # Rotina de desvio
            else:
                # Move-se
                
                # Atualiza posição
                self.x_pos -= 1
    
    #   □ □ <-- Tentando visualizar, se existir uma parede de uma célula para outra, precisamos de assinalar duas paredes (pois cada célula tem 4 paredes)
    #   No caso da parede à esquerda, na célula imediata existe uma parede à esquerda, e para a célula seguinte [x_pos - 1] existe uma parede à direita

    def assinala_parede(self, matriz):
        i = matriz[self.y_pos][self.x_pos]

        if self.orientacao_robot == "Norte":
            i.parede_acim = True

            n = matriz[self.y_pos + 1][self.x_pos]
            n.parede_abaix = True

        if self.orientacao_robot == "Este":
            i.parede_dir = True
            
            n = matriz[self.y_pos][self.x_pos + 1]
            n.parede_esq = True
        
        if self.orientacao_robot == "Sul":
            i.parede_abaix = True
            
            n = matriz[self.y_pos - 1][self.x_pos]
            n.parede_acim = True
        
        if self.orientacao_robot == "Oeste":
            i.parede_esq = True
            
            n = matriz[self.y_pos - 1][self.x_pos]
            n.parede_dir = True
    
    def assinala_ovelha(self, matriz):
        if self.orientacao_robot == "Norte":
            n = matriz[self.y_pos + 1][self.x_pos]
            n.conteudo = 0

        if self.orientacao_robot == "Este":
            n = matriz[self.y_pos + 1][self.x_pos + 1]
            n.conteudo = 0
        
        if self.orientacao_robot == "Sul":
            n = matriz[self.y_pos - 1][self.x_pos]
            n.conteudo = 0
        
        if self.orientacao_robot == "Oeste":
            n = matriz[self.y_pos - 1][self.x_pos + 1]
            n.conteudo = 0

    def deteta_ovelha(sensor_us):
        distance = sensor_us.value()/10 # converter mm para cm
        # print(str(distance) + " " + units)
        if distance < 20:
            return True

# Criação de constantes

# Criação dos objetos

# Programa
jg = Jogo()
rb = Robot()

# Sensores/ Robot
voice = Sound()
us = UltrasonicSensor()
steer_pair = MoveSteering(OUTPUT_D, OUTPUT_C)
cl = ColorSensor()
confirm = TouchSensor(INPUT_4)
det_touch = TouchSensor(INPUT_3)

# Atribuição de modos aos sensores 
us.mode = 'US-DIST-CM'
units = us.units

# jg = Jogo()
# jg.preenche_matriz()
# jg.imprime_matriz()
# rb = Robot()

# jg.assinala_parede_abaix(1, 0)
# print("\n")
# jg.imprime_matriz()
# print("\n")
# rb.move_frente(jg.matriz)
# jg.imprime_matriz()
