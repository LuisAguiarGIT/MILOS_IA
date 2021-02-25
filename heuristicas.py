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

        return

    # 4 - Verificação retroceder
    if(linha_diferente(robot)):
        robot.retrocede = True
    
    # 5 - Retrocedendo
    if(robot.retrocede):
        troca_sentido(robot)
        direcao = robot.direcao_desejada

        if(direcao = "Esquerda" and pode_mover_desejado_esquerda(robot)):
            robot.move_esq(matriz)
            return
        
        else if(direcao = "Direita" and pode_mover_desejado_direita(robot)):
            robot.move_dir(matriz)
            return
        
        else 
            troca_sentido(robot)
            robot.retrocede = False
            return

    # 6 - Células não visitadas abaixo
    if (dentro_de_limites(robot.x_pos, robot.y_pos - 1)) and (not rb_pos_abaixo.visitado):
        if robot.pode_mover_abaixo:
            robot.move_abaixo(matriz)
            return 
    
    # 7 - Obstáculo ou limite
    if (robot.direcao_desejada == "Direita" and not pode_mover_desejado_direita(robot))
     or (robot.direcao_desejada == "Esquerda" and not pode_mover_desejado_esquerda(robot)):
        if robot.y_pos != 0:
            print("OBSTACULO, MOVENDO ACIMA...", file=stderr)
            robot.movendo_acima = True
        else if robot.y_pos != 5:
            print("OBSTACULO, MOVENDO ABAIXO...", file=stderr)
            robot.movendo_abaixo = False
    
    # 8 - Limite
    if ( robot.prox_dentro_de_limites(robot.x_pos, robot.y_pos, robot.direcao_desejada)):
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
    if not pode_mover_desejado(robot):
        print("OBSTACULO, TROCANDO DIREÇÃO...", file=stderr)
        troca_sentido(robot)
    
    # 12 - Move numa direção desejada
    if pode_mover_desejado(robot):
        print("MOVENDO NA DIREÇÃO DESEJADA...", file=stderr)
        if robot.direcao_desejada == "Direita" and pode_mover_desejado_direita(robot):
            robot.move_direita(matriz)
            return
        else if robot.direcao_desejada == "Esquerda" pode_mover_desejado_esquerda(robot):
            robot.move_esquerda(matriz)
            return
        else 
            return

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
    matriz = jogo.matriz
    rb_pos = matriz[robot.y_pos][robot.x_pos]
    rb_pos_acima = matriz[robot.y_pos + 1][robot.x_pos]

    if na_posicao(0,0):
        #Salta para conduzir as ovelhas

    if(linha_diferente(robot)):
        robot.retrocede = True
    
    if(robot.retrocede):
        troca_sentido(robot)
        
        if(pode_mover_desejado_esquerda(robot)):
            robot.move_esq(matriz)
            return
        
        else if(pode_mover_desejado_direita(robot)):
            robot.move_dir(matriz)
            return
        
        else 
            robot.retrocede = False

    if not rb_pos_acima.visitado:
        if robot.pode_mover_acima:
            robot.move_acima(matriz)
            return 
    
    if (robot.direcao_desejada == "Direita" and not pode_mover_desejado_direita(robot))
     or (robot.direcao_desejada == "Esquerda" and not pode_mover_desejado_esquerda(robot)):
        if robot.y_pos != 5:
            robot.movendo_acima = True
        if robot.y_pos == 5:
            robot.movendo_abaixo = False

        troca_sentido(robot)
    
    if robot.movendo_acima:
        if robot.pode_mover_acima(matriz):
            robot.move_acima(matriz)
            robot.movendo_acima = False
            return
    
    if robot.movendo_abaixo:
        if robot.pode_mover_abaixo(matriz):
            robot.move_abaixo(matriz)
            robot.movendo_abaixo = False
            return
    
    if not pode_mover_desejado(robot):
        if robot.pode_mover_acima(robot):
            robot.move_acima(matriz)
            return
        
        troca_sentido(robot)

        if robot.y_pos != 5 :
            robot.movendo_acima = True
        
        if pode_mover_desejado(robot):
            if pode_mover_desejado_direita(robot):
                robot.move_direita(matriz)
                return
            else if pode_mover_desejado_esquerda(robot):
                robot.move_esquerda(matriz)
                return
            else 
                pass
    
    if pode_mover_desejado(robot):
        if pode_mover_desejado_direita(robot):
            robot.move_direita(matriz)
            return
        else if pode_mover_desejado_esquerda(robot):
            robot.move_esquerda(matriz)
            return
        else 
            pass

def pode_mover_desejado_esquerda(robot):
    if robot.direcao_desejada == "Esquerda" and robot.pode_mover_esq(matriz):
        return True

def pode_mover_desejado_direita(robot):
    if robot.direcao_desejada == "Direita" and robot.pode_mover_dir(matriz):
        return True

def pode_mover_desejado(robot):
    if(pode_mover_desejado_esquerda(robot) or pode_mover_desejado_direita(robot)):
        return True

def troca_sentido(robot):
    robot.direcao_desejada = "Esquerda" if robot.direcao_desejada == "Direita" else "Esquerda"

def na_posicao(y,x):
    if robot.y_pos == y and robot.x_pos == x :
        return True

def linha_diferente(robot):
    if robot.pos_ant[0] != robot.y_pos :
        return True