def modo_scan(robot, jogo):
    matriz = jogo.matriz
    rb_pos = matriz[robot.y_pos][robot.x_pos]
    rb_pos_abaixo = matriz[robot.y_pos - 1][robot.x_pos]

    if na_posicao(5,5):
        modo_volta_inicio(robot, jogo)
        return
    
    rb_pos.visitado = True

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

    if not rb_pos_abaixo.visitado:
        if robot.pode_mover_abaixo:
            robot.move_abaixo(matriz)
            return 
    
    if (robot.direcao_desejada == "Direita" and robot.x_pos == 5) or (robot.direcao_desejada == "Esquerda" and robot.x_pos == 0):
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

def pode_mover_desejado_esquerda(robot):
    if robot.direcao_desejada == "Direita" and robot.pode_mover_dir(matriz):
        return True

def pode_mover_desejado(robot):
    if(pode_mover_desejado_esquerda(robot) or pode_mover_desejado_esquerda(robot)):
        return True

def troca_sentido(robot):
    robot.direcao_desejada = "Esquerda" if robot.direcao_desejada == "Direita" else "Esquerda"

def na_posicao(y,x):
    if robot.y_pos == y and robot.x_pos == x :
        return True

def linha_diferente(robot):
    if robot.pos_ant[0] != robot.y_pos :
        return True

def modo_volta_inicio(robot, jogo):
    matriz = jogo.matriz


