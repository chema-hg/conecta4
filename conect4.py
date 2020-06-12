#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''version del juego conecta 4'''
import numpy as np
import pygame
import sys
import math
import os # Para meter efectos de sonido al programa

ROW_COUNT=6
COLUMN_COUNT=7

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

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

def draw_board(board):
    ''' Dibuja el tablero del juego en pygame'''
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            # El algoritmo dibuja los cuadrados azules y circulos negros si el la matriz
            # del juego no hay fichas, es decir si el valor es cero.
        
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):      
                if board[r][c]==1:
                    # Si el valor de la matriz es 1, dibuja la ficha roja del jugador 1
                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif board[r][c]==2:
                    # # Si el valor de la matriz es 2, dibuja la ficha amarilla del jugador 2
                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    # Cada vez que se redibuje el tablero mandaremos actualizar la pantalla.
    pygame.display.update()
    

board=create_board() # Crea una matriz numpy de 6 por 7
print(board)
game_over=False
turn=0

# -------------------------------------------------------------------------------------
pygame.init() # Iniciamos la parte gráfica con la libreria pygame

SQUARESIZE = 100 # Tamaño de los cuadrados en pixeles

width = SQUARESIZE*COLUMN_COUNT
height = SQUARESIZE*(ROW_COUNT+1) # Anadimos una fila mas para poder mover la ficha por la parte superior.

# El radio de los circulos interiores tiene que ser un poco mas pequeño que los cuadrados en donde esta metido
RADIUS = int(SQUARESIZE/2-5)                    

screen = pygame.display.set_mode((width,height))
# Crea una pantalla de pygame con el tamaño que necesitamos
draw_board(board)
# Dibuja el tablero 
# Para el dibujo de las formas del juego podemos verlo en http://www.pygame.org/docs/ref/draw.html

# definimos la fuente para renderizar posteriormente texto en la pantalla
myfont=pygame.font.SysFont("monospace", 60)


while not game_over:
    # bucle donde se desarrollara el juego, mientras turn no se True el bucle
    # se ejecutará indefinidamente
    
    for event in pygame.event.get(): # Por cada evento (Pulsacion de teclado, raton etc)
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx=event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()        
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            # El juego comienza al pulsar el boton del mouse
            # print(event.pos) #lo podemos utilizar para ver las coordenadas (x,y) cuando
            # pulsamos el raton.
            
            # Preguntar al jugador 1 para que mueva
            if turn==0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                # math.floor redondea al entero más proximo menor o igual que x
                # Lo que hacemos es dividir la coordenada x en la pantalla cuando pulsamos
                # el boton del ratón y lo dividimos entre el tamaño de cada cuadrado. Luego con math.floor
                # lo redondeamos y asi conseguimos saber la columna donde tirar la ficha (0,1,2,3,4,5,6)
                # col-> nos da la columna donde caerá la ficha del jugador 1.
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    
                    if winning_move(board,1):
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        label = myfont.render("EL JUGADOR 1 GANÓ. YEAHH!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over=True
                
            # Preguntar al jugador 2 para que mueva
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                # col-> nos da la columna donde caerá la ficha del jugador 2.
                
                #Aqui empieza el motor del juego
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
                    
                    if winning_move(board,2):
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        label = myfont.render("EL JUGADOR 2 GANÓ. YEAHH!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over=True
                        
            draw_board(board)
            os.system("aplay click_sound.wav&")
            print_board(board)
            
            # A la variable que empieza el programa en cero le sumamos uno en cada bucle
            turn +=1
            # % obteniendo el resto de dividir la variable por si misma, siempre nos dara 0 o 1
            # lo que nos permitirá alternar entre los jugadores con el condicional.
            turn=turn%2
            
            if game_over:
                os.system("aplay tada.wav&")
                # Cuando el juego termine espera 3 segundos para que no salga inmediatamente
                # de la pantalla.
                pygame.time.wait(3000)

            
    
    
    
    
    
    
    

    
    
        
