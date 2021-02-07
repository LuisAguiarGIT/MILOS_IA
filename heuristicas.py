def modo_scan(robot, jogo):
    matriz = jogo.matriz

    # SCANNING #
    while(1):
        if(position_at(5,5)):
            backtrack_mode(robot,jogo)

        else if(position_at(0,0)):
            robot.verifica_periferia(matriz)

        # Falta ver se foi visitado anteriormente
        if(robot.pode_mover_dir(matriz) ):
            robot.move_dir(matriz)

        # Falta ver se foi visitado anteriormente
        else if(robot.pode_mover_esq(matriz)):
            robot.move_esq(matriz)
        
        # Falta ver se foi visitado anteriormente
        else if(robot.pode_mover_acima(matriz) ):
            robot.move_acima(matriz)
        
        else if(robot.pode_mover_dir(matriz)
        and not robot.pode_mover_esq(matriz)
        and not robot.pode_mover_acima(matriz)):
            robot.move_l_acima(matriz)
            
        else if(robot.pode_mover_esq(matriz)):
            robot.move_esq(matriz)
        
        else if(robot.pode_mover_abaixo(matriz)):
            robot.move_abaix(matriz)
        
        else:
            print("Impossível!", file=stderr)
            break


def position_at(y,x):
    return (if robot.y_pos == y and robot.x_pos == x)

def backtrack_mode(robot, jogo):