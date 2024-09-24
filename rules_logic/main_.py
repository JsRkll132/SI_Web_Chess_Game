import pygame
import sys
import ChessStates
import ChessItems
import ChessEngine
import time
import tkinter as tk
from tkinter import messagebox
# Definir algunos colores
BLANCO = (255, 255, 255)
NEGRO = (0, 99, 147)
GRIS = (100, 100, 100)
# Tamaño de la pantalla y tamaño del tablero
ANCHO = 720
ALTO = 720
TAM_CUADRO = ANCHO // 8
IMAGES = {}
TURNO = True
# Inicializar Pygame
pygame.init()
#CurrentChessGame = ChessStates.ChessStates()
#board =  CurrentChessGame.getBoard()
# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez 960")

def loadImages() : 
    blackPieces = sorted(ChessItems.Chessitems().getBlackItems())
    whitePieces = sorted(ChessItems.Chessitems().getWhiteItems())
    for i in blackPieces : 
        IMAGES[i] = pygame.transform.scale(pygame.image.load('GameView\Images\\blackpieces\\'+i+'.png'),(TAM_CUADRO, TAM_CUADRO))
    for i in whitePieces : 
        IMAGES[i] = pygame.transform.scale(pygame.image.load('GameView\Images\\whitepieces\\'+i+'.png'),(TAM_CUADRO, TAM_CUADRO))    


def draw_board( board) :
    for fila in range(8):
        for columna in range(8):
            x = columna * TAM_CUADRO
            y = fila * TAM_CUADRO
            # Dibujar el tablero
            color = BLANCO if (fila + columna) % 2 == 0 else NEGRO
            pygame.draw.rect(pantalla, color, (x, y, TAM_CUADRO, TAM_CUADRO))
            # Dibujar las piezas
            piece = board[fila][columna]
            if piece != '-' :
                try : 
                    pantalla.blit(IMAGES[piece], (x, y))
                except : 
                    pass

def gameLoop(piece = "",curr_pos = None,new_pos = None) : 
    pass
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, font, color, surface, x, y, width, height, hover_color, mouse_pos):
    button_rect = pygame.Rect(x, y, width, height)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, button_rect)
    else:
        pygame.draw.rect(surface, color, button_rect)
    draw_text(text, font, BLANCO, surface, x + 20, y + 10)
    return button_rect

def menu():
    while True:
        pantalla.fill(BLANCO)
        draw_text('Ajedrez 960', pygame.font.Font(None, 74), NEGRO, pantalla, ANCHO // 2 - 150, ALTO // 4)

        mouse_pos = pygame.mouse.get_pos()
        start_button = draw_button('Iniciar Juego', pygame.font.Font(None, 50), GRIS, pantalla, ANCHO // 2 - 150, ALTO // 2, 300, 50, NEGRO, mouse_pos)
        exit_button = draw_button('Salir', pygame.font.Font(None, 50), GRIS, pantalla, ANCHO // 2 - 150, ALTO // 2 + 100, 300, 50, NEGRO, mouse_pos)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(evento.pos):
                    return
                elif exit_button.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

def select_difficulty():
    while True:
        pantalla.fill(BLANCO)
        draw_text('Seleccionar Dificultad', pygame.font.Font(None, 74), NEGRO, pantalla, ANCHO // 2 - 250, ALTO // 4)

        mouse_pos = pygame.mouse.get_pos()
        easy_button = draw_button('Facil', pygame.font.Font(None, 50), GRIS, pantalla, ANCHO // 2 - 100, ALTO // 2, 200, 50, NEGRO, mouse_pos)
        intermediate_button = draw_button('Intermedio', pygame.font.Font(None, 50), GRIS, pantalla, ANCHO // 2 - 100, ALTO // 2 + 100, 200, 50, NEGRO, mouse_pos)
        hard_button = draw_button('Dificil', pygame.font.Font(None, 50), GRIS, pantalla, ANCHO // 2 - 100, ALTO // 2 + 200, 200, 50, NEGRO, mouse_pos)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(evento.pos):
                    return 'facil'
                elif intermediate_button.collidepoint(evento.pos):
                    return 'intermedio'
                elif hard_button.collidepoint(evento.pos):
                    return 'dificil'

def show_endgame_dialog(played):
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    if played == 'n':
        message = '¡Jugador Negro pierde! ¿Desea continuar(Si) o regresar al menú(No)?'
    else:
        message = '¡Jugador Blanco pierde! ¿Desea continuar(Si) o regresar al menú(No)'

    result = messagebox.askyesno("Fin del juego", message)
    root.destroy()

    if result:
        return 'continue'
    else:
        return 'menu'
def main():
    CurrentChessGame = None
    CurrentChessGame = ChessStates.ChessStates()
    global TURNO
   # global CurrentChessGame
    loadImages()
    menu()
    difficulty = select_difficulty()
    curr_pos=None
    new_pos= None
    piece = ""
    best = None
    ActiveGame = True
    flag_dialog = False
    while True:
        #board_aux = CurrentChessGame.getBoard()
        #next_data = ChessEngine.ChessEngine().minmax(board_aux,1,True,'b')
        #print(next_data)
        played = 'b' if CurrentChessGame.getTurno() else 'n'
        eval_cmw = ChessEngine.ChessEngine().is_checkmate([row[:] for row in CurrentChessGame.getBoard()],'b')
        eval_cmb = ChessEngine.ChessEngine().is_checkmate([row[:] for row in CurrentChessGame.getBoard()],'n')
        if (eval_cmw) : 
            print("Pierden blancas")
        elif(eval_cmb) :
            print("Pierden negras")

      #  print(eval_cm)
        if (CurrentChessGame.king_die([row[:] for row in CurrentChessGame.getBoard()],played) or eval_cmw or eval_cmb and not flag_dialog) :
            result = show_endgame_dialog(played)
            #
            if result == 'menu':

                main()
                
                ActiveGame = False
                break
            else:
                flag_dialog = True
                #ActiveGame = True  # Continúa la partida actual
                #continue
            a ="""
            mouse_pos = pygame.mouse.get_pos()
            restart_button = draw_button('Reiniciar Juego', pygame.font.Font(None, 50), GRIS, pantalla, ANCHO // 2 - 150, ALTO // 2, 300, 50, NEGRO, mouse_pos)
            exit_button = draw_button('Salir', pygame.font.Font(None, 50), GRIS, pantalla, ANCHO // 2 - 150, ALTO // 2 + 100, 300, 50, NEGRO, mouse_pos)

            pygame.display.flip()
            ActiveGame = False
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(evento.pos):
                        CurrentChessGame = ChessStates.ChessStates()
                        main()
                        break
                        
                    elif exit_button.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()"""
        if ActiveGame :
            if not CurrentChessGame.getTurno() :
                    board_aux = [row[:] for row in CurrentChessGame.getBoard()]
                    if difficulty == 'facil' :
                        best  = ChessEngine.ChessEngine().random_move(board_aux,'n')
                    elif difficulty == 'intermedio' : 
                        best = ChessEngine.ChessEngine().best_first_search(board_aux,'n',2)
                    elif difficulty == 'dificil' : 
                        best = ChessEngine.ChessEngine().minmax(board_aux,4,False,'b')

                    print(f'This is the best move : {best[0]}')
            if (CurrentChessGame.getTurno() ==False and best != None) : 
                CurrentChessGame.changePieces(best[0][1],best[0][0])
                CurrentChessGame.changeTurno()
                time.sleep(0.5)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN : 
                    x, y = pygame.mouse.get_pos()
                    position = CurrentChessGame.move_piece(x,y,TAM_CUADRO,TAM_CUADRO)  # Llamar a la función para mover la pieza
                    print("posicion")
                    print(position)
                    print((x//TAM_CUADRO,y//TAM_CUADRO))
                    print(CurrentChessGame.getBoard())
                    legal_moves = CurrentChessGame.generate_legal_moves_for_piece(CurrentChessGame.getBoard(),(y//TAM_CUADRO,x//TAM_CUADRO))
                    print("--------------------")
                # print(f"legal moves whites : {CurrentChessGame.count_legal_moves(CurrentChessGame.getBoard(),'b')}")
                #  print(f"legal moves whites : {CurrentChessGame.count_legal_moves(CurrentChessGame.getBoard(),'n')}")
                    lg_whites = CurrentChessGame.generate_legal_moves(CurrentChessGame.getBoard(),'b')
                    print(f'lfwhites : {lg_whites}')
                    CurrentChessGame.generate_legal_moves(CurrentChessGame.getBoard(),'n')
                # board_aux = []


                    
                    #print("nex data :")
                # print(next_data)
                    print(CurrentChessGame.evaluate_board(CurrentChessGame.getBoard()))
                    print("LEGAL MOVES")
                    print(legal_moves)
                    if CurrentChessGame.getBoard()[position[0]][position[1]] == '-' or CurrentChessGame.isKilled(position,curr_pos) : 
                        new_pos = position
                    elif   CurrentChessGame.getBoard()[position[0]][position[1]] != '-': 
                        piece = CurrentChessGame.getBoard()[position[0]][position[1]]
                        curr_pos = position
                    print(piece)
                    print(curr_pos)
                    print(new_pos)
                    print(f'turno actual {CurrentChessGame.getTurno()}')
                    if new_pos!= None and curr_pos!=None and CurrentChessGame.verifiedPiece(piece,new_pos,curr_pos,board =  CurrentChessGame.getBoard()) :
                        if CurrentChessGame.getTurno() :
                            time.sleep(0.2)
                        CurrentChessGame.changePieces(new_pos,curr_pos)
                        curr_pos = None 
                        new_pos =None
                        CurrentChessGame.changeTurno()
                    elif new_pos!= None and curr_pos!=None and not CurrentChessGame.verifiedPiece(piece,new_pos,curr_pos,board =  CurrentChessGame.getBoard()) :
                        curr_pos = None 
                        new_pos =None
        
                    
                    
                    
            # Dibujar el tablero
            draw_board(CurrentChessGame.getBoard())

            # Actualizar la pantalla
            pygame.display.flip()
        else :
            break

if __name__ == "__main__":
    main()
