import tkinter as tk
from tkinter import messagebox
import ChessStates
import ChessEngine

# Inicializar el estado del juego
CurrentChessGame = ChessStates.ChessStates()

# Definir algunos colores
BLANCO = '#ffffff'
NEGRO = '#006393'
GRIS = '#646464'
VERDE = '#00ff00'
RED =  '#de3535'
CELESTE_OSCURO = '#007ACC'
BLANCO_TEXTO = '#ffffff'
# Tamaño del tablero
ANCHO_ = 720
ALTO_ = 720
ANCHO = 920
ALTO = 720
TAM_CUADRO = ANCHO_ // 8
IMAGES = {}

# Inicializar Tkinter
root = tk.Tk()
root.title("Ajedrez 960")

# Variables de control de juego
curr_pos = None
new_pos = None
piece = None
highlighted_squares = []
legal_moves = []
difficulty = tk.StringVar(value='facil')  # Variable para la dificultad, con valor predeterminado 'facil'

# Crear el lienzo
canvas = tk.Canvas(root, width=ANCHO_, height=ALTO)
canvas.pack(side=tk.LEFT)

# Frame para información adicional y controles
info_frame = tk.Frame(root, width=200, height=ALTO)
info_frame.pack(side=tk.RIGHT, fill=tk.Y)
info_frame.pack_propagate(False)

# Label para mostrar el turno actual
turn_label = tk.Label(info_frame, text="Turno: Blancas", font=("Terminal", 16))
turn_label.pack(pady=20)

# Botón para salir al menú principal
exit_button = tk.Button(info_frame, text="Salir", command=root.quit, font=("Terminal", 11), bg=CELESTE_OSCURO, fg=BLANCO_TEXTO)
exit_button.pack(pady=15)

# Botón para reiniciar la partida
reset_button = tk.Button(info_frame, text="Reiniciar partida", command=lambda: reset_game(), font=("Terminal", 11), bg=CELESTE_OSCURO, fg=BLANCO_TEXTO)
reset_button.pack(pady=15)

# Frame para selección de dificultad
difficulty_frame = tk.Frame(info_frame)
difficulty_frame.pack(pady=40)

difficulty_label = tk.Label(difficulty_frame, text="Dificultad:", font=("Terminal", 14))
difficulty_label.pack(pady=5)

easy_radio = tk.Radiobutton(difficulty_frame, text="Fácil", variable=difficulty, value='facil', font=("Terminal", 12), command=lambda: set_difficulty('facil'))
easy_radio.pack(pady=10)

intermediate_radio = tk.Radiobutton(difficulty_frame, text="Intermedio", variable=difficulty, value='intermedio', font=("Terminal", 12), command=lambda: set_difficulty('intermedio'))
intermediate_radio.pack(pady=10)

hard_radio = tk.Radiobutton(difficulty_frame, text="Difícil", variable=difficulty, value='dificil', font=("Terminal", 12), command=lambda: set_difficulty('dificil'))
hard_radio.pack(pady=10)
terminate = False
# Cargar imágenes de piezas
def load_images():
    pieces = {
        'Tn': 'Tn.png',
        'Cn': 'Cn.png',
        'An': 'An.png',
        'Rn': 'Rn.png',
        'RNn': 'RNn.png',
        'Pn': 'Pn.png',
        'Tb': 'Tb.png',
        'Cb': 'Cb.png',
        'Ab': 'Ab.png',
        'Rb': 'Rb.png',
        'RNb': 'RNb.png',
        'Pb': 'Pb.png'
    }
    for piece, filename in pieces.items():
        if piece[-1] == 'n':
            IMAGES[piece] = tk.PhotoImage(file=f'GameView\\Images\\blackpieces\\{filename}')
        else:
            IMAGES[piece] = tk.PhotoImage(file=f'GameView\\Images\\whitepieces\\{filename}')

# Dibujar el tablero
def draw_board(highlighted_squares=None):
    if highlighted_squares is None:
        highlighted_squares = []
    for row in range(8):
        for col in range(8):
            color = BLANCO if (row + col) % 2 == 0 else NEGRO
            x1 = col * TAM_CUADRO
            y1 = row * TAM_CUADRO
            x2 = x1 + TAM_CUADRO
            y2 = y1 + TAM_CUADRO
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    # Resaltar las casillas legales
    for square in highlighted_squares:
        row, col = square
        x1 = col * TAM_CUADRO
        y1 = row * TAM_CUADRO
        x2 = x1 + TAM_CUADRO
        y2 = y1 + TAM_CUADRO
        canvas.create_rectangle(x1, y1, x2, y2, fill=VERDE, stipple="gray50") if CurrentChessGame.getBoard()[row][col][-1] == '-' else canvas.create_rectangle(x1, y1, x2, y2, fill=RED, stipple="gray50")

# Colocar las piezas en el tablero
def place_pieces(board):
    canvas.delete("pieces")
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "-":
                x = col * TAM_CUADRO + TAM_CUADRO // 2
                y = row * TAM_CUADRO + TAM_CUADRO // 2
                canvas.create_image(x, y, image=IMAGES[piece], tags="pieces")

def on_canvas_click(event):
    global curr_pos, new_pos, piece, highlighted_squares, legal_moves
    x, y = event.x, event.y
    col = x // TAM_CUADRO
    row = y // TAM_CUADRO
    position = (row, col)
    print(CurrentChessGame.tablero)
    if curr_pos is None and new_pos is None and CurrentChessGame.getTurno():
        legal_moves = CurrentChessGame.generate_legal_moves_for_piece(CurrentChessGame.getBoard(), position)
        piece = CurrentChessGame.getBoard()[row][col]
        if piece != "-":
            curr_pos = position
            draw_board(highlighted_squares=legal_moves)
            place_pieces(CurrentChessGame.getBoard())
    elif (curr_pos is not None and new_pos is None and CurrentChessGame.getTurno() or (position == '-' or  CurrentChessGame.isKilled(position,curr_pos))):
        new_pos = position
        if curr_pos != new_pos and (new_pos in legal_moves):
            move_piece(curr_pos, new_pos)
            curr_pos = None
            new_pos = None
            piece = None
            highlighted_squares = []
            draw_board()  # Redibujar el tablero sin resaltado
            place_pieces(CurrentChessGame.getBoard())
        else:
            curr_pos = None
            new_pos = None
            piece = None
            highlighted_squares = []
            draw_board()  # Redibujar el tablero sin resaltado
            place_pieces(CurrentChessGame.getBoard())

def move_piece(start, end):
    start_row, start_col = start
    end_row, end_col = end
    global CurrentChessGame
    if CurrentChessGame.verifiedPiece(piece, end, start, board=CurrentChessGame.getBoard()):
        CurrentChessGame.changePieces(end, start)
        CurrentChessGame.changeTurno()
        update_turn_label()
        draw_board()
        place_pieces(CurrentChessGame.getBoard())
        verified_end_game() 
        if not CurrentChessGame.getTurno():
            root.after(500, make_black_move)  # Espera 500ms antes de hacer el movimiento de las negras

def make_black_move():
    board_aux = [row[:] for row in CurrentChessGame.getBoard()]
   # depth = 2 if difficulty.get() == 'facil' else 4 if difficulty.get() == 'intermedio' else 6
    if difficulty.get() == 'facil' :
        best  = ChessEngine.ChessEngine().random_move(board_aux,'n')
    elif difficulty.get() == 'intermedio' : 
        best = ChessEngine.ChessEngine().best_first_search(board_aux,'n',2)
    elif difficulty.get() == 'dificil' : 
        best = ChessEngine.ChessEngine().minmax(board_aux,4,False,'b')

    if best:
        CurrentChessGame.changePieces(best[0][1], best[0][0])
        CurrentChessGame.changeTurno()
        update_turn_label()
        draw_board()
        place_pieces(CurrentChessGame.getBoard())
        verified_end_game() 

def verified_end_game():
    global terminate
    if (not terminate and CurrentChessGame.king_die(CurrentChessGame.getBoard(), 'b' if CurrentChessGame.getTurno() else 'n') or ChessEngine.ChessEngine().is_checkmate([row[:] for row in CurrentChessGame.getBoard()], 'b') or ChessEngine.ChessEngine().is_checkmate([row[:] for row in CurrentChessGame.getBoard()], 'n')):
        result = show_endgame_dialog('b' if CurrentChessGame.getTurno() else 'n')
        if result == 'menu' :
            reset_game()
        else:
            terminate = True
            main_menu()

def show_endgame_dialog(played):
    if played == 'n':
        message = '¡Jugador Negro pierde! ¿Desea continuar (Sí) o reiniciar la partida (No)?'
    else:
        message = '¡Jugador Blanco pierde! ¿Desea continuar (Sí) o reiniciar la partida (No)?'

    result = messagebox.askyesno("Fin del juego", message)
    if result:
        return 'continue'
    else:
        return 'menu'

def main_menu():
    pass

def reset_game():
    global CurrentChessGame
    global terminate
    terminate = False
    CurrentChessGame = ChessStates.ChessStates()
    update_turn_label()
    draw_board()
    place_pieces(CurrentChessGame.getBoard())

def update_turn_label():
    if CurrentChessGame.getTurno():
        turn_label.config(text="Turno: Blancas")
    else:
        turn_label.config(text="Turno: Negras")

def set_difficulty(selected_difficulty):
    global difficulty
    difficulty.set(selected_difficulty)


# Cargar imágenes y dibujar tablero
load_images()
draw_board()
place_pieces(CurrentChessGame.getBoard())
update_turn_label()

# Vincular clic del ratón al lienzo
canvas.bind("<Button-1>", on_canvas_click)

# Iniciar el bucle principal de Tkinter
root.mainloop()
