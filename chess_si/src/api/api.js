import axios from 'axios';

// Crear instancia de axios con la URL base correcta
const api = axios.create({
    baseURL: 'http://127.0.0.1:5000/chessgame', // Asegúrate de que esta URL sea correcta
});

// Crear una nueva partida y obtener el session_id
export const createGame = async () => {
    try {
        const response = await api.post('/create');
        return response.data;
    } catch (error) {
        console.error('Error creating game:', error);
        return { error: 'Error creating game' };
    }
};

// Obtener el estado del tablero
export const get_board = async (session_id) => {
    try {
        const response = await api.get('/board', { params: { session_id } });
        return response.data;
    } catch (error) {
        console.error('Error fetching board:', error);
        return [];
    }
};

// Realizar un movimiento
export const make_move = async (session_id, move) => {
    try {
        const response = await api.post('/move', { session_id, move });
        return response.data;
    } catch (error) {
        console.error('Error making move:', error);
        return { error: 'Error making move' };
    }
};

// Reiniciar el juego
export const reset_game = async (session_id) => {
    try {
        const response = await api.post('/reset', { session_id });
        return response.data;
    } catch (error) {
        console.error('Error resetting game:', error);
        return { error: 'Error resetting game' };
    }
};

// Obtener el turno actual
export const get_turn = async (session_id) => {
    try {
        const response = await api.get('/turn', { params: { session_id } });
        return response.data;
    } catch (error) {
        console.error('Error fetching turn:', error);
        return { error: 'Error fetching turn' };
    }
};

// Realizar un movimiento contra la máquina
export const make_move_against = async (session_id) => {
    try {
        const response = await api.get('/move_against', { params: { session_id } });
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        return { error: 'Error making move' };
    }
};
