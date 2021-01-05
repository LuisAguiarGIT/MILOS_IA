#!/usr/bin/env python3
# BIBLIOTECAS #
# from time import sleep
# from array import *
# from collections import OrderedDict

# from ev3dev2.motor import LargeMotor, OUTPUT_D, OUTPUT_C, SpeedRPS, MoveTank, MoveSteering
# from ev3dev2.sensor import INPUT_3, INPUT_4
# from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor
# from ev3dev2.sound import Sound
# from sys import stderr


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
            
    def muda_valor(self, y_pos, x_pos):
        i = self.matriz[y_pos][x_pos]
        i.conteudo = 0
    
    def assinala_parede_esq(self, y_pos, x_pos):
        i = self.matriz[y_pos][x_pos] 
        i.parede_esq = True
    
    def assinala_parede_acim(self, y_pos, x_pos):
        i = self.matriz[y_pos][x_pos] 
        i.parede_acim = True
    
    def assinala_parede_dir(self, y_pos, x_pos):
        i = self.matriz[y_pos][x_pos] 
        i.parede_dir = True

    def assinala_parede_abaix(self, y_pos, x_pos):
        i = self.matriz[y_pos][x_pos] 
        i.parede_abaix = True
        
class Cell:

    def __init__(self):
        self.parede_esq = False
        self.parede_acim = False
        self.parede_dir = False
        self.parede_abaix = False
        self.conteudo = "#"

    def set_parede(self, parede):
        self.parede = True
    
    def set_conteudo(self):
        self.conteudo = 0

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

    def move_frente(self, matriz):
        prox_pos_y = matriz[self.y_pos + 1][self.x_pos]
        prox_pos_x = matriz[self.y_pos][self.x_pos + 1]
        pos_ant_y = matriz[self.y_pos - 1][self.x_pos]
        pos_ant_y = matriz[self.y_pos][self.x_pos - 1]
        
        if(self.orientacao_robot == "Norte"):
            if prox_pos_y.parede_abaix == True:
                print("Tem parede!")
            else:
                self.y_pos += 1
        if(self.orientacao_robot == "Este"):
            if prox_pos_x.parede_esq == True:
                print("Tem parede!")
            else:
                self.x_pos += 1
        if(self.orientacao_robot == "Sul"):
            if prox_ant_y.parede_acim == True:
                print("Tem parede!")
            else:
                self.y_pos -= 1
        if(self.orientacao_robot == "Oeste"):
            if prox_ant_x.parede_esq == True:
                print("Tem parede!")
            else:
                self.x_pos -= 1

jg = Jogo()
jg.preenche_matriz()
jg.imprime_matriz()
rb = Robot()

jg.assinala_parede_abaix(1, 0)
print("\n")
jg.imprime_matriz()
print("\n")
rb.move_frente(jg.matriz)
jg.imprime_matriz()

        

jg = Jogo()
jg.preenche_matriz()
jg.imprime_matriz()
rb = Robot()
jg.muda_valor(rb.y_pos, rb.x_pos)
print("\n")
jg.imprime_matriz()
print("\n")
rb.move_frente()
jg.muda_valor(rb.y_pos, rb.x_pos)
jg.imprime_matriz()
