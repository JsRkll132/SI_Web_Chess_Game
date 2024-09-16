from flask import Flask, jsonify, request
import uuid_utils as uuid
from datetime import datetime, timedelta
from flask_cors import CORS
from ChessStates import ChessStates  # Asegurando que ChessStates maneja el estado del juego
import ChessEngine

app = Flask(__name__)
CORS(app, origins="*")

# Almacenamiento de sesiones en memoria
sessions = {}

# Función para crear una nueva sesión con un UUID y un estado de juego
def create_new_session():
    session_id = uuid.uuid4().hex
    sessions[session_id] = {
        'game': ChessStates(),  # Estado inicial del juego
        'last_activity': datetime.now() , # Marca de tiempo de la última actividad
        'difficult' : 'Normal'
    }
    return session_id

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

@app.route('/chessgame/create', methods=['POST'])
def create_game():
    session_id = create_new_session()
    return jsonify({'session_id': session_id})
uuid.uuid4().hex
@app.route('/chessgame/board', methods=['GET'])
def get_board():
    session_id = request.args.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403
    return jsonify(sessions[session_id]['game'].getBoard())

@app.route('/chessgame/changeDifficult', methods=['POST'])
def changeDifficult():
    session_id = request.json.get('session_id')
    difficult = request.json.get('difficult')
    print(session_id)
    if not session_id or is_session_expired(session_id):
        return jsonify({'success': False, 'error': 'Session expired or not found'}), 403
    if difficult in ['Facil','Normal','Dificil'] :
        sessions[session_id]['difficult'] = difficult 
        return jsonify({'success': True ,'difficult':difficult }) 

    return jsonify({'success': False, 'message': 'Movimiento ilegal'})

@app.route('/chessgame/move', methods=['POST'])
def make_move():
    session_id = request.json.get('session_id')
    print(session_id)
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403

    move = request.json.get('move')['move']
    print(move)
    current_game = sessions[session_id]['game']
    
    piece = current_game.getBoard()[move['from'][0]][move['from'][1]]
    if current_game.verifiedPiece(piece, new_pos=tuple(move['to']), curr_pos=tuple(move['from']), board=current_game.getBoard()):
        current_game.changePieces(currpos=tuple(move['from']), newpos=tuple(move['to']))
        current_game.changeTurno()
        return jsonify({'success': True, 'board': current_game.getBoard(), 'turn': current_game.getTurno()})
    
    return jsonify({'success': False, 'message': 'Movimiento ilegal'})

@app.route('/chessgame/move_against', methods=['GET'])
def make_move_against():
    session_id = request.args.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403
    
    current_game = sessions[session_id]['game']
    board_aux = [row[:] for row in current_game.getBoard()]
    if sessions[session_id]['difficult'] == 'Facil' :
        best  = ChessEngine.ChessEngine().random_move(board_aux,'n')
    if sessions[session_id]['difficult'] ==  'Normal':
        best = ChessEngine.ChessEngine().best_first_search(board_aux,'n',2)
    if sessions[session_id]['difficult'] == 'Dificil' :
        best = ChessEngine.ChessEngine().minmax(board_aux, 4, False, 'b')
    if best:
        current_game.changePieces(best[0][1], best[0][0])
        current_game.changeTurno()
        return jsonify({'success': True, 'board': current_game.getBoard(), 'turn': current_game.getTurno()})
    return jsonify({'success': False, 'message': 'Movimiento ilegal'})

@app.route('/chessgame/turn', methods=['GET'])
def get_turn():
    session_id = request.args.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403
    return jsonify({'turn': sessions[session_id]['game'].getTurno()})

@app.route('/chessgame/reset', methods=['POST'])
def reset_game():
    session_id = request.json.get('session_id')
    if not session_id or is_session_expired(session_id):
        return jsonify({'error': 'Session expired or not found'}), 403
    
    sessions[session_id]['game'] = ChessStates()
    return jsonify({'success': True, 'board': sessions[session_id]['game'].getBoard()})

if __name__ == '__main__':
    app.run(debug=True)
