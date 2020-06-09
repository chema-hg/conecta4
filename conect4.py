#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''version del juego conecta 4'''
import numpy as np

ROW_COUNT=6
COLUMN_COUNT=7

def create_board():
    '''diseñanos el tablero como una matriz de 6 filas y 7 columnas'''
    board=np.zeros((ROW_COUNT,COLUMN_COUNT)) #matriz de 6 filas y 7 columnas rellena con ceros
    return board

def drop_piece(board, row, col, piece):
    '''marca la casilla con la ficha del jugador que tenga el turno: 1 o 2'''
    board[row][col] = piece

def is_valid_location(board, col):
    '''Comprueba que la columna seleccionada es valida, sea todavia cero y no haya sido utilizada.

    IMPORTANTE: Estamos trabajando con un tablero al reves de lo que se verá en el juego. Es decir, interna-
    mente la ficha la primera vez cambiara una columna en la primera fila. Si luego, por ejemplo
    el jugador 2 pone en la misma columna se cambiara el valor en la segunda fila y asi sucesivamente.
    Se va llenando o, cambiando el valor de la primera fila hacia abajo. Se va lledando de
    arriba hacia abajo.Esto luego lo arreglaremos visualmente con la función print_board'''
    return board[ROW_COUNT-1][col]==0
    #devuelve siempre True salvo que algun jugador haya alcanzado ya un elemento de la ultima fila
    #, en nuestro caso la 5 (python empieza a contar desde el cero). Recordemos que internamente se va llenando
    # de arriba hacia abajo.
   
def get_next_open_row(board, col):
    '''Devuelve que fila no ha sido utilizada en funcion de la columna que haya escogido el jugador'''
    for r in range(ROW_COUNT):
        if board[r][col]==0:
            return r
    return None

def print_board(board):
    '''Redibuja el tablero girandolo en el eje x.

    Sin esta funcion al representar el tablero, este se va llenando primero la fila de arriba y
    sigue hacia abajo, justo al reves de como tendría que ser en el juego original'''
    print(np.flip(board, 0))
    
def winning_move(board, piece):
    '''rutinas para determinar el ganador del juego.

    Gana quien conecte cuatro fichas en horizontal, vertical o diagonal'''
    # Comprueba las posiciones horizontales. El algoritmo va mirando horizontalmente todas las casillas
    # que contengan 4 fichas juntas del mismo jugador y devuelve true si las encuentra.
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
            
    # Comprobamos las posiciones verticales.
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    

    # Comprobamos diagonal positivas (abajo-arriba)
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True
    
    # Comprobamos diagonal negativas (arriba-abajo)
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True
    
    return None

board=create_board() # Crea una matriz numpy de 6 por 7
print(board)
game_over=False
turn=0

while not game_over:
    # bucle donde se desarrollara el juego, mientras turn no se True el bucle
    # se ejecutará indefinidamente
    
    # Preguntar al jugador 1 para que mueva
    if turn==0:
        col = int(input("Jugador 1 mueve ficha (0-6) > "))
        # col-> nos da la columna donde caerá la ficha del jugador 1.
        
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)
            
            if winning_move(board,1):
                print("EL JUGADOR 1 GANO. YEAHH!!")
                game_over=True
        
    # Preguntar al jugador 2 para que mueva
    else:
        col = int(input("Jugador 2 mueve ficha (0-6) > "))
        # col-> nos da la columna donde caerá la ficha del jugador 2.
        
        #Aqui empieza el motor del juego
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            
            if winning_move(board,2):
                print("EL JUGADOR 2 GANO. YEAHH!!")
                game_over=True
    
    print_board(board)
    
    # A la variable que empieza el programa en cero le sumamos uno en cada bucle
    turn +=1
    # % obteniendo el resto de dividir la variable por si misma, siempre nos dara 0 o 1
    # lo que nos permitirá alternar entre los jugadores con el condicional.
    turn=turn%2


    
    
        
