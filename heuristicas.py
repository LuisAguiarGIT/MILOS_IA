##########################
#    LEITURA DO MAPA     #
##########################
def modo_scan(robot, jogo):
    print("MODO SCAN...", file=stderr)

    matriz = jogo.matriz
    rb_pos = matriz[robot.y_pos][robot.x_pos]
    rb_pos_abaixo = matriz[robot.y_pos - 1][robot.x_pos]

    # 1 - Estamos no objetivo
    if na_posicao(5,5):
        print("CHEGOU AO OBJETIVO, TROCANDO PARA VOLTA INICIO...", file=stderr)

        # Inicializar
        robot.reset_visitado()
        robot.direcao_desejada = "Esquerda"
        robot.retrocede = False
        robot.movendo_acima = False
        robot.movendo_abaixo = False 

        modo_volta_inicio(robot, jogo)
        return
    
    # 2 - Marcar como visitado
    rb_pos.visitado = True

    # 3 - Scan
    robot.verifica_periferia(matriz)

    rb_pos_acima = matriz[robot.y_pos + 1][robot.x_pos]
    rb_pos_direita = matriz[robot.y_pos][robot.x_pos + 1]

    if((rb_pos_acima and rb_pos_acima.conteudo == 0) or (rb_pos_direita and rb_pos_direita == 0)) :
        print("OVELHAS POSICOES ADJACENTES, TROCANDO PARA MODO PASTOR...", file=stderr)
        # TODO MODO PASTOR
        robot.ultima_acao = None
        robot.direcao_seguir = None
        robot.esperando = False
        modo_pastor(robot, matriz)

        return

    # 4 - Verificação retroceder
    if(robot.pos_ant[1] != None and linha_diferente(robot)):
        print("RETROCEDENDO...", file=stderr)
        robot.retrocede = True
    
    # 5 - Retrocedendo
    if(robot.retrocede):
        if not robot.retrocedeDirecaoTrocado:
            troca_sentido(robot)
            robot.retrocedeDirecaoTrocado = True
        
        direcao = robot.direcao_desejada

        if(pode_mover_direcao(robot, direcao)):
            print("MOVENDO NA DIREÇÃO DE RETROCEDE...", file=stderr)
            mover_direcao(robot, matriz, direcao)
        
        else:
            print("ACABOU DE MOVER NA DIREÇÃO DE RETROCEDE...", file=stderr)
            troca_sentido(robot)
            robot.retrocedeDirecaoTrocado = False

    # 6 - Células não visitadas abaixo
    if (dentro_de_limites(robot.x_pos, robot.y_pos - 1)) and (not rb_pos_abaixo.visitado):
        print("CÉLULAS NÃO VISITADAS ABAIXO...", file=stderr)
        if robot.pode_mover_abaixo:
            robot.move_abaixo(matriz)
            return 
    
    # 7 - Obstáculo ou limite
    if (not pode_mover_direcao(robot, robot.direcao_desejada)):
        if robot.y_pos != 0:
            print("OBSTACULO, MOVENDO ACIMA...", file=stderr)
            robot.movendo_acima = True
        else if robot.y_pos != 5:
            print("OBSTACULO, MOVENDO ABAIXO...", file=stderr)
            robot.movendo_abaixo = True
    
    # 8 - Limite
    if (not robot.prox_dentro_de_limites(robot.x_pos, robot.y_pos, robot.direcao_desejada)):
        print("NO LIMITE, INVERTENDO DIREÇÃO...", file=stderr)
        troca_sentido(robot)
    
    # 9 - Movendo acima
    if robot.movendo_acima:
        if robot.pode_mover_acima(matriz):
            print("MOVENDO ACIMA..", file=stderr)
            robot.move_acima(matriz)
            robot.movendo_acima = False
            return
    
    # 10 - Movendo abaixo
    if robot.movendo_abaixo:
        if robot.pode_mover_abaixo(matriz):
            print("MOVENDO ABAIXO..", file=stderr)
            robot.move_abaixo(matriz)
            robot.movendo_abaixo = False
            return
    
    # 11 - Não pode mover na direção desejada
    if not pode_mover_direcao(robot, robot.direcao_desejada):
        print("OBSTACULO, TROCANDO DIREÇÃO...", file=stderr)
        troca_sentido(robot)
    
    # 12 - Move numa direção desejada
    if pode_mover_direcao(robot, robot.direcao_desejada):
        print("MOVENDO NA DIREÇÃO DESEJADA...", file=stderr)
        mover_direcao(robot, matriz, robot.direcao_desejada)

    if robot.pode_mover_acima(matriz):
        robot.move_acima(matriz)
        robot.movendo_acima = False
        robot.movendo_abaixo = False
        return
    
    if robot.pode_mover_abaixo(matriz):
        robot.move_abaixo(matriz)
        robot.movendo_acima = False
        robot.movendo_abaixo = False
        return
    
    print("ERRO FATAL, TERMINANDO..", file=stderr)
    break


##########################
#    VOLTA AO INÍCIO     #
##########################

def modo_volta_inicio(robot, jogo):
    print("MODO E.T. PHONE HOME...", file=stderr)

    matriz = jogo.matriz
    rb_pos = matriz[robot.y_pos][robot.x_pos]
    rb_pos_abaixo = matriz[robot.y_pos - 1][robot.x_pos]

    # 1 - Estamos no objetivo
    if na_posicao(0,0):
        print("CHEGOU AO OBJETIVO, TROCANDO PARA SCAN...", file=stderr)

        # Inicializar
        robot.reset_visitado()
        robot.direcao_desejada = "Direita"
        robot.retrocede = False
        robot.movendo_acima = False
        robot.movendo_abaixo = False 

        modo_scan(robot, jogo)
        return
    
    # 2 - Marcar como visitado
    rb_pos.visitado = True

    # 3 - Scan
    robot.verifica_periferia(matriz)

    rb_pos_acima = matriz[robot.y_pos + 1][robot.x_pos]
    rb_pos_direita = matriz[robot.y_pos][robot.x_pos + 1]

    if((rb_pos_acima and rb_pos_acima.conteudo == 0) or (rb_pos_direita and rb_pos_direita == 0)) :
        print("OVELHAS POSICOES ADJACENTES, TROCANDO PARA MODO PASTOR...", file=stderr)
        # TODO MODO PASTOR
        robot.ultima_acao = None
        robot.direcao_seguir = None
        robot.esperando = False

        modo_pastor(robot, matriz)
        return

    # 4 - Verificação retroceder
    if(robot.pos_ant[1] != None and linha_diferente(robot)):
        print("RETROCEDENDO...", file=stderr)
        robot.retrocede = True
    
    # 5 - Retrocedendo
    if(robot.retrocede):
        if not robot.retrocedeDirecaoTrocado:
            troca_sentido(robot)
            robot.retrocedeDirecaoTrocado = True
        
        direcao = robot.direcao_desejada

        if(pode_mover_direcao(robot, direcao)):
            print("MOVENDO NA DIREÇÃO DE RETROCEDE...", file=stderr)
            mover_direcao(robot, matriz, direcao)
        
        else:
            print("ACABOU DE MOVER NA DIREÇÃO DE RETROCEDE...", file=stderr)
            troca_sentido(robot)
            robot.retrocedeDirecaoTrocado = False

    # 6 - Células não visitadas acima
    if (dentro_de_limites(robot.x_pos, robot.y_pos + 1)) and (not rb_pos_acima.visitado):
        print("CÉLULAS NÃO VISITADAS ABAIXO...", file=stderr)
        if robot.pode_mover_acima:
            robot.move_acima(matriz)
            return 
    
    # 7 - Obstáculo ou limite
    
    if (not pode_mover_direcao(robot, robot.direcao_desejada)):
        if robot.y_pos != 5:
            print("OBSTACULO, MOVENDO ABAIXO...", file=stderr)
            robot.movendo_abaixo = True
        else if robot.y_pos != 0:
            print("OBSTACULO, MOVENDO ACIMA...", file=stderr)
            robot.movendo_acima = True
    
    # 8 - Limite
    if (not robot.prox_dentro_de_limites(robot.x_pos, robot.y_pos, robot.direcao_desejada)):
        print("NO LIMITE, INVERTENDO DIREÇÃO...", file=stderr)
        troca_sentido(robot)
    
    # 9 - Movendo acima
    if robot.movendo_acima:
        if robot.pode_mover_acima(matriz):
            print("MOVENDO ACIMA..", file=stderr)
            robot.move_acima(matriz)
            robot.movendo_acima = False
            return
    
    # 10 - Movendo abaixo
    if robot.movendo_abaixo:
        if robot.pode_mover_abaixo(matriz):
            print("MOVENDO ABAIXO..", file=stderr)
            robot.move_abaixo(matriz)
            robot.movendo_abaixo = False
            return
    
    # 11 - Não pode mover na direção desejada
    if not pode_mover_direcao(robot, robot.direcao_desejada):
        print("OBSTACULO, TROCANDO DIREÇÃO...", file=stderr)
        troca_sentido(robot)
    
    # 12 - Move numa direção desejada
    if pode_mover_direcao(robot, robot.direcao_desejada):
        print("MOVENDO NA DIREÇÃO DESEJADA...", file=stderr)
        mover_direcao(robot, matriz, robot.direcao_desejada)

    # if robot.pode_mover_acima(matriz):
    #     robot.move_acima(matriz)
    #     robot.movendo_acima = False
    #     robot.movendo_abaixo = False
    #     return
    
    # if robot.pode_mover_abaixo(matriz):
    #     robot.move_abaixo(matriz)
    #     robot.movendo_acima = False
    #     robot.movendo_abaixo = False
    #     return
    
    print("ERRO FATAL, TERMINANDO..", file=stderr)
    break

def modo_pastor(robot, matriz):
    print("MODO PASTOR..", file=stderr)

    # Esperando, acaba turno
    if robot.esperando:
        robot.esperando = False
    
    # Seguindo ovelhas

    if robot.direcao_seguir != None:
        celula_seguir = robot.busca_celula_direcao(matriz, robot.direcao_seguir)

        if celula_seguir:
            # Moveu a ovelha no turno anterior mas o mesmo não se moveu
            if celula_seguir and celula_seguir.conteudo == 0:
                robot.ultima_acao = None
                robot.esperando = True

                if(robot.pode_mover_esq(matriz)):
                    print("OVELHA PRESA, MOVENDO PARA A ESQUERDA..", file=stderr)
                    robot.move_esquerda(matriz)
                    return
                
                if(robot.pode_mover_abaixo(matriz)):
                    print("OVELHA PRESA, MOVENDO ABAIXO..", file=stderr)
                    robot.move_abaixo(matriz)
                    return
                
                if(robot.pode_mover_direita(matriz)):
                    print("OVELHA PRESA, MOVENDO PARA A DIREITA..", file=stderr)
                    robot.move_direita(matriz)
                    return
                
                print("ERRO FATAL, NÃO CONSEGUE MOVER..", file=stderr)
                return

        # Movemos a ação no último turno, seguindo
        robot.ultima_acao = None  

        if pode_mover_direcao(robot, robot.direcao_seguir):
            mover_direcao(robot, matriz, robot.direcao_seguir)

            if pode_mover_direcao(robot, robot.direcao_seguir):
                mover_direcao(robot, matriz, robot.direcao_seguir)
        
        robot.direcao_Seguir = None

    rb_pos_acima = matriz[robot.y_pos + 1][robot.x_pos]
    rb_pos_direita = matriz[robot.y_pos][robot.x_pos + 1]

    if(rb_pos_acima.conteudo == 0 and rb_pos_direita.conteudo == 0):
        rb_pos_abaixo = matriz[robot.y_pos - 1][robot.x_pos]
        rb_pos_esquerda = matriz[robot.y_pos][robot.x_pos - 1]

        if rb_pos_acima.conteudo == 0:
            # GRITO
        
        if rb_pos_direita.conteudo == 0:
            # GRITO
        
        if rb_pos_abaixo.conteudo == 0:
            # GRITO
        
        if rb_pos_esquerda.conteudo == 0:
            # GRITO

        return

    if rb_pos_acima and rb_pos_acima.conteudo == 0:
        print("OVELHA ACIMA, EMPURRANDO..", file=stderr)
        robot.ultima_acao = "Empurrar"
        robot.direcao_seguir = "Acima"

        # EMPURRA ACIMA

        return
    
    if rb_pos_direita and rb_pos_direita.conteudo == 0:
        print("OVELHA DIREITA, EMPURRANDO..", file=stderr)
        robot.ultima_acao = "Empurrar"
        robot.direcao_seguir = "Direita"

        # EMPURRA DIREITA

        return

    print("OVELHAS NÃO ENCONTRADAS, TROCANDO PARA SCAN..", file=stderr)

    robot.reset_visitado()
    robot.direcao_desejada = "Direita"
    robot.retrocede = False
    robot.movendo_acima = False
    robot.movendo_abaixo = False

    modo_scan(robot, jogo)
    return


# def pode_mover_desejado_esquerda(robot):
#     if robot.direcao_desejada == "Esquerda" and robot.pode_mover_esq(matriz):
#         return True

# def pode_mover_desejado_direita(robot):
#     if robot.direcao_desejada == "Direita" and robot.pode_mover_dir(matriz):
#         return True

# def pode_mover_desejado(robot):
#     if(pode_mover_desejado_esquerda(robot) or pode_mover_desejado_direita(robot)):
#         return True

def pode_mover_direcao(robot, direcao):
    if direcao == "Esquerda" and robot.pode_mover_esq(matriz):
        return True
    if direcao == "Direita" and robot.pode_mover_dir(matriz):
        return True
    if direcao == "Acima" and robot.pode_mover_acima(matriz):
        return True
    if direcao == "Abaixo" and robot.pode_mover_abaixo(matriz):
        return True

def mover_direcao(robot, matriz, direcao):
    if direcao == "Esquerda":
        robot.move_esq(matriz)
    else if direcao == "Direita":
        robot.move_dir(matriz)
    else if direcao == "Acima":
        robot.move_acima(matriz)
    else:
        robot.move_abaixo(matriz)

def troca_sentido(robot):
    robot.direcao_desejada = "Esquerda" if robot.direcao_desejada == "Direita" else "Esquerda"

def na_posicao(y,x):
    if robot.y_pos == y and robot.x_pos == x :
        return True

def linha_diferente(robot):
    if robot.pos_ant[1] != robot.y_pos :
        return True