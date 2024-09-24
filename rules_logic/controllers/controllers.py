from quart import Blueprint, jsonify, request  # Cambiar flask por quart
import uuid_utils as uuid
from datetime import datetime, timedelta
from ChessStates import ChessStates  # Asegurando que ChessStates maneja el estado del juego
import ChessEngine
from services.services import make_move_Service, start_game, change_difficult,set_winner

sessions = {}
controllers_ = Blueprint('controllers_', __name__)

# Función para crear una nueva sesión con un UUID y un estado de juego
def create_new_session():
    session_id = uuid.uuid4().hex
    sessions[session_id] = {
        'game': ChessStates(),  # Estado inicial del juego
        'last_activity': datetime.now(),  # Marca de tiempo de la última actividad
        'difficult': 'Normal'
    }
    return session_id

def verifief_game(chessgame):
    #print('wda'*30)
    return chessgame.king_die(chessgame.getBoard(), 'b' if chessgame.getTurno() else 'n')

# Verificar si la sesión ha expirado (ej. 30 minutos de inactividad)
def is_session_expired(session_id, timeout=30):
    session = sessions.get(session_id)
    if session:
        if datetime.now() - session['last_activity'] > timedelta(minutes=timeout):
            del sessions[session_id]  # Eliminar la sesión si ha expirado
            return True
        # Actualizar la última actividad
        session['last_activity'] = datetime.now()
        return False
    return True

@controllers_.route('/chessgame/create', methods=['POST'])
async def create_game():
    session_id = create_new_session()
    await start_game(session_id=session_id, difficult='Normal')  # Usar await en lugar de asyncio.run
    return jsonify({'session_id': session_id})

@controllers_.route('/chessgame/board', methods=['GET'])
async def get_board():
    session_id = request.args.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403
    return jsonify(sessions[session_id]['game'].getBoard())

@controllers_.route('/chessgame/changeDifficult', methods=['POST'])
async def changeDifficult():
    json_data = await request.get_json()  # Obtener el JSON completo
    session_id = json_data.get('session_id')
    difficult = json_data.get('difficult')
    print(session_id)
    if not session_id or is_session_expired(session_id):
        return jsonify({'success': False, 'error': 'Session expired or not found'}), 403
    if difficult in ['Facil', 'Normal', 'Dificil']:
        sessions[session_id]['difficult'] = difficult
        await change_difficult(session_id=session_id, new_difficult=difficult)  # Usar await en lugar de asyncio.run
        return jsonify({'success': True, 'difficult': difficult})

    return jsonify({'success': False, 'message': 'Movimiento ilegal'})

@controllers_.route('/chessgame/move', methods=['POST'])
async def make_move():
    json_data = await request.get_json()  # Obtener el JSON completo
    session_id = json_data.get('session_id')
    print(session_id)
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403

    move = json_data.get('move')['move']
    print(move)
    current_game = sessions[session_id]['game']
    print(verifief_game(current_game))
    if verifief_game(current_game):
        message = 'Partida terminada, jaque mate o rey muerto'
        winner = current_game.king_die_(current_game.getBoard(),'b' if current_game.getTurno() else 'n')
        await set_winner(session_id=session_id,winner=winner )
        return jsonify({'success': True, 'board': current_game.getBoard(), 'turn': current_game.getTurno(), 'endgame': True, 'message': message,'winner':winner})
    
    piece = current_game.getBoard()[move['from'][0]][move['from'][1]]
    if current_game.verifiedPiece(piece, new_pos=tuple(move['to']), curr_pos=tuple(move['from']), board=current_game.getBoard()):
        current_game.changePieces(currpos=tuple(move['from']), newpos=tuple(move['to']))
        player_type = "Blancas" if current_game.getTurno() else 'Negras'
        await make_move_Service(session_id, piece, str(tuple(move['from'])), str(tuple(move['to'])), current_game.getTurno(), player_type)  # Usar await
        current_game.changeTurno()
        return jsonify({'success': True, 'board': current_game.getBoard(), 'turn': current_game.getTurno()})

    return jsonify({'success': False, 'message': 'Movimiento ilegal'})

@controllers_.route('/chessgame/move_against', methods=['GET'])
async def make_move_against():
    session_id = request.args.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403

    current_game = sessions[session_id]['game']
    if verifief_game(current_game):
        message = 'Partida terminada, jaque mate o rey muerto'
        winner = current_game.king_die_(current_game.getBoard(),'b' if current_game.getTurno() else 'n')
        await set_winner(session_id=session_id,winner=winner )
        return jsonify({'success': True, 'board': current_game.getBoard(), 'turn': current_game.getTurno(), 'endgame': True, 'message': message ,'winner':winner})
    
    board_aux = [row[:] for row in current_game.getBoard()]
    if sessions[session_id]['difficult'] == 'Facil':
        best = ChessEngine.ChessEngine().random_move(board_aux, 'n')
    elif sessions[session_id]['difficult'] == 'Normal':
        best = ChessEngine.ChessEngine().best_first_search(board_aux, 'n', 2)
    elif sessions[session_id]['difficult'] == 'Dificil':
        best = ChessEngine.ChessEngine().minmax(board_aux, 4, False, 'b')
    
    if best:
        current_game.changePieces(best[0][1], best[0][0])
        piece_select = list(best[0][0])
        print(piece_select)
        piece = board_aux[piece_select[0]][piece_select[1]]
        print(piece)
        player_type = "Blancas" if current_game.getTurno() else 'Negras'
        await make_move_Service(session_id, piece, str(best[0][0]), str(best[0][1]), current_game.getTurno(), player_type)  # Usar await
        current_game.changeTurno()
        return jsonify({'success': True, 'board': current_game.getBoard(), 'turn': current_game.getTurno()})

    return jsonify({'success': False, 'message': 'Movimiento ilegal'})

@controllers_.route('/chessgame/turn', methods=['GET'])
async def get_turn():
    session_id = request.args.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403
    return jsonify({'turn': sessions[session_id]['game'].getTurno()})

@controllers_.route('/chessgame/reset', methods=['POST'])
async def reset_game():
    json_data = await request.get_json()  # Obtener el JSON completo
    session_id = json_data.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403

    sessions[session_id]['game'] = ChessStates()
    return jsonify({'success': True, 'board': sessions[session_id]['game'].getBoard()})
