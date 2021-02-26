class Robot:

    def __init__(self):
        self.x_pos = 0
        self.y_pos = 0
        self.orientacoes = ["Norte", "Este", "Sul", "Oeste"]
        self.ori_index = 0
        self.orientacao_robot = self.orientacoes[self.ori_index]

        # SCAN DA MATRIZ
        self.direcao_desejada = "Direita"
        self.pos_ant = [None,None]
        self.retrocede = False
        self.retrocedeDirecaoTrocado = False
        self.movendo_acima = False
        self.movendo_abaixo = False 

        # MODO PASTOR
        self.ultima_acao = None 
        self.direcao_seguir = None
        self.esperando = False

    def atualiza_orientacao(self):
        self.orientacao_robot = self.orientacoes[self.ori_index % len(self.orientacoes)]

    def verifica_periferia(self, matriz):

        while(self.orientacao_robot != "Norte"):
            self.vira_direita()

        i = 0
        while i < 4 :
            voice.speak("Can I check?")

            while not confirm.is_pressed:
                pass
            
            self.verifica_cor(matriz, us)
            self.vira_direita()
            i += 1
        
        self.vira_direita()

    # ============= #
    # LEITURA CORES #
    # ============= #

    def cor_rgb(self):

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
            cor = self.cor_rgb()

        return cor

    def verifica_cor(self, matriz, us):
        steer_pair.on(steering=0, speed=VELOCIDADE_PROCURA) 
        sleep(0.3)

        cor = self.cor_rgb()
        
        while cor != 'black' or cor != 'red' :
            cor = self.cor_rgb()

            if cor == 'black' :
                steer_pair.off()

                voice.speak("Reading")
                sleep(1)
                if self.deteta_ovelha(us):
                    self.assinala_ovelha(matriz)
                    voice.speak("Sheep here")
                    sleep(1)

                self.move_atras()
                break
            
            if cor == 'red' :
                steer_pair.off()
                self.assinala_parede(matriz)

                voice.speak("Reading")
                sleep(1)
                if self.deteta_ovelha(us):
                    self.assinala_ovelha(matriz)
                    voice.speak("Sheep here")
                    sleep(1)
                
                self.move_atras()
                break
        

    # ========= #
    # MOVIMENTO #
    # ========= #

    def vira_esquerda(self):
        mv_dir.on_for_rotations(-25, 25, 1.3)
        self.ori_index -= 1
        self.orientacao = self.atualiza_orientacao()
    
    def vira_direita(self):
        mv_dir.on_for_rotations(25,-25, 1.3)
        self.ori_index += 1
        self.orientacao = self.atualiza_orientacao()
    
    def move_atras(self):
        mv_dir.on_for_rotations(-25,-25, 0.7)
    
    def move_frente(self, matriz):
        pos_atual = matriz[self.y_pos][self.x_pos]
        
        if(self.orientacao_robot == "Norte"):

            mv_dir.on_for_rotations(25,25, ROTACOES_CASA)   
            self.pos_ant[0] = y_pos    
            self.y_pos += 1

        if(self.orientacao_robot == "Este"):

            mv_dir.on_for_rotations(25,25, ROTACOES_CASA)
            self.pos_ant[1] = x_pos    
            self.x_pos += 1

        if(self.orientacao_robot == "Sul"):

            mv_dir.on_for_rotations(25,25, ROTACOES_CASA)
            self.pos_ant[0] = y_pos    
            self.y_pos -= 1

        if(self.orientacao_robot == "Oeste"):

            mv_dir.on_for_rotations(25,25, ROTACOES_CASA)
            self.pos_ant[1] = x_pos  
            self.x_pos -= 1
    
    def move_acima(self, matriz):
        self.confirma_movimento()

        while(self.orientacao_robot != "Norte"):
            self.vira_direita()
        
        self.move_frente(matriz)

    def move_dir(self, matriz):
        self.confirma_movimento()

        while(self.orientacao_robot != "Este"):
            self.vira_direita()
        
        self.move_frente(matriz)
    
    def move_esq(self, matriz):
        while(self.orientacao_robot != "Oeste"):
            self.vira_direita()
        
        self.move_frente(matriz)

    def move_abaixo(self, matriz):
        self.confirma_movimento()

        while(self.orientacao_robot != "Sul"):
            self.vira_direita()
        
        self.move_frente(matriz)

    def dentro_de_limites(posX, posY):
        return (
            (posX >= 0 and posX <= 5) and (posY >= 0 and posY <= 5)
        )

    def prox_dentro_de_limites(posX, posY, direcao):
        if not self.dentro_de_limites(posX, posY):
            return False
        
        if direcao = "Direita":
            return self.dentro_de_limites(posX + 1, posY)
        
        if direcao = "Esquerda":
            return self.dentro_de_limites(posX - 1, posY)
        

    # def move_l_acima(self, matriz):
    #     self.confirma_movimento()
    #     self.move_dir(matriz)
    #     self.verifica_periferia(matriz)
    #     self.move_acima(matriz)
    
    # def move_l_abaixo(self, matriz):
    #     self.confirma_movimento()
    #     self.move_dir(matriz)
    #     self.verifica_periferia(matriz)
    #     self.move_abaixo(matriz)

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
            n = matriz[self.y_pos][self.x_pos + 1]
            n.conteudo = 0
        
        if self.orientacao_robot == "Sul":
            n = matriz[self.y_pos - 1][self.x_pos]
            n.conteudo = 0
        
        if self.orientacao_robot == "Oeste":
            n = matriz[self.y_pos][self.x_pos - 1]
            n.conteudo = 0

    def deteta_ovelha(self,sensor_us):
        distance = sensor_us.value()/10 # converter mm para cm
        # print(str(distance) + " " + units)
        if distance < 20:
            return True

    # VERIFICA SE PODE MOVER PARA A POSIÇÃO
    def pode_mover(self, matriz):
        if(this.pode_mover_acima(matriz) or this.pode_mover_dir(matriz) or this.pode_mover_abaixo(matriz) or this.pode_mover_esq(matriz)):
            return True

    def pode_mover_acima(self, matriz):
        pos_atual = matriz[self.y_pos][self.x_pos]
        prox_pos = matriz[self.y_pos + 1][self.x_pos]

        if not pos_atual.parede_acim and not prox_pos.conteudo == "0" and not prox_pos > 5: 
            return True

    def pode_mover_dir(self, matriz):
        pos_atual = matriz[self.y_pos][self.x_pos]
        prox_pos = matriz[self.y_pos][self.x_pos + 1]

        if not pos_atual.parede_dir and not prox_pos.conteudo == "0" and not prox_pos > 5:
            return True

    def pode_mover_abaixo(self, matriz):
        pos_atual = matriz[self.y_pos][self.x_pos]
        prox_pos = matriz[self.y_pos - 1][self.x_pos]

        if not pos_atual.parede_abaix and not prox_pos.conteudo == "0" and not prox_pos < 0:
            return True
    
    def pode_mover_esq(self, matriz):
        pos_atual = matriz[self.y_pos][self.x_pos]
        prox_pos = matriz[self.y_pos][self.x_pos - 1]

        if not pos_atual.parede_esq and not prox_pos.conteudo == "0" and not prox_pos > 0:
            return True
    
    def confirma_movimento(self):
        voice.speak("Confirm movement")
        while not confirm.is_pressed:
            pass

    def busca_celula_direcao(self, matriz, direcao):
        if(direcao == "Acima")
