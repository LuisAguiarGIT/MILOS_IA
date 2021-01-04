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
    
    def atualiza_pos_x(self):
        if(self.orientacao_robot == "Este"):
            return self.x_pos + 1
        
        if(self.orientacao_robot == "Oeste"):
            return self.x_pos - 1
    
    def atualiza_pos_y(self):
        if(self.orientacao_robot == "Norte"):
            return self.y_pos + 1
        
        if(self.orientacao_robot == "Sul"):
            return self.y_pos - 1
    
    def vira_esquerda(self):
        return self.ori_index - 1
    
    def vira_direita(self):
        return self.ori_index + 1

    def atualiza_orientacao(self):
        return self.orientacoes[self.ori_index % len(orientacoes)]

    def move_frente(self):
        if(self.orientacao_robot == "Norte"):
            return self.y_pos + 1
        if(self.orientacao_robot == "Este"):
            return self.x_pos + 1
        if(self.orientacao_robot == "Sul"):
            return self.y_pos - 1
        if(self.orientacao_robot == "Oeste"):
            return self.x_pos - 1
        


