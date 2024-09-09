import pygame
import sys
import ChessStates
import ChessItems
# Definir algunos colores
BLANCO = (255, 255, 255)
NEGRO = (0, 99, 147)

# Tamaño de la pantalla y tamaño del tablero
ANCHO = 720
ALTO = 720
TAM_CUADRO = ANCHO // 8
IMAGES = {}
# Inicializar Pygame
pygame.init()

board =  ChessStates.ChessStates().getBoard()
# Crear la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tablero de Ajedrez")

def loadImages() : 
    blackPieces = sorted(ChessItems.Chessitems().getBlackItems())
    whitePieces = sorted(ChessItems.Chessitems().getWhiteItems())
    for i in blackPieces : 
        IMAGES[i] = pygame.transform.scale(pygame.image.load('ChessGame\GameView\Images\\blackpieces\\'+i+'.png'),(TAM_CUADRO, TAM_CUADRO))
    for i in whitePieces : 
        IMAGES[i] = pygame.transform.scale(pygame.image.load('ChessGame\GameView\Images\\whitepieces\\'+i+'.png'),(TAM_CUADRO, TAM_CUADRO))    

def move_piece(x, y):
    fila = y // TAM_CUADRO
    columna = x // TAM_CUADRO

    print(f'Moviendo pieza en la fila {fila} y columna {columna}')
    return fila,columna
def changePieces (newpos,currpos) :
    
    board[newpos[0]][newpos[1]] = board[currpos[0]][currpos[1]]
    board[currpos[0]][currpos[1]] = "-"
    [ print(f'{k}\n') for k in board ]
    draw_board(board)
def main():
    loadImages()
    curr_pos=None
    new_pos= None
    while True:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN : 
                x, y = pygame.mouse.get_pos()
                position = move_piece(x, y)  # Llamar a la función para mover la pieza
                if board[position[0]][position[1]] == '-' : 
                    new_pos = position
                elif   board[position[0]][position[1]] != '-': 
                    curr_pos = position
                print(curr_pos)
                print(new_pos)
                
                if new_pos!= None and curr_pos!=None :
                    changePieces(new_pos,curr_pos)
                    curr_pos = None 
                    new_pos =None
                
                
        # Dibujar el tablero
        draw_board(board)

        # Actualizar la pantalla
        pygame.display.flip()
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
 
def draw_board_and_pieces(board, white_pieces, black_pieces):
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
                    image = pygame.transform.scale(pygame.image.load('ChessGame\GameView\Images\\blackpieces\\' + piece + '.png'), (TAM_CUADRO, TAM_CUADRO))
                    pantalla.blit(image, (x, y))
                except : 
                    image = pygame.transform.scale(pygame.image.load('ChessGame\GameView\Images\whitepieces\\' + piece + '.png'), (TAM_CUADRO, TAM_CUADRO))
                    pantalla.blit(image, (x, y))


if __name__ == "__main__":
    main()
