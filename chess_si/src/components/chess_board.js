import React, { useEffect, useState, useCallback , useMemo } from 'react';
import { Chessboard } from 'react-chessboard';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import { ChessboardDnDProvider } from 'react-chessboard';
import { get_board, get_turn, reset_game, make_move, make_move_against, createGame,change_difficult } from '../api/api';

const mapCustomPieces = {
  "Pb": "wP", "Pn": "bP",
  "Cb": "wN", "Cn": "bN",
  "Ab": "wB", "An": "bB",
  "Tb": "wR", "Tn": "bR",
  "RNb": "wQ", "RNn": "bQ",
  "Rb": "wK", "Rn": "bK",
  "-": null
};

const convertGameStateToPosition = (gameState) => {
  const position = {};
  const rows = ['8', '7', '6', '5', '4', '3', '2', '1'];
  const cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

  gameState.forEach((row, rowIndex) => {
    row.forEach((piece, colIndex) => {
      const square = `${cols[colIndex]}${rows[rowIndex]}`;
      if (mapCustomPieces[piece]) {
        position[square] = mapCustomPieces[piece];
      }
    });
  });

  return position;
};

const colMap = {
  'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
};

const chessToVector = (notation) => {
  const col = colMap[notation[0]];
  const row = 8 - parseInt(notation[1]);
  return [row, col];
};

const convertMoveToIndices = (move) => {
  const fromIndex = chessToVector(move.from);
  const toIndex = chessToVector(move.to);
  return { move: { from: fromIndex, to: toIndex } };
};

const ChessGame = () => {
  const [board, setBoard] = useState({});
  const [turn, setTurn] = useState('Blancas');
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [difficulty, setDifficulty] = useState('Normal'); // Estado para la dificultad
  const boardWidth = useMemo(() => 650, []);

  const startCreateGame = useCallback(async () => {
    try {
      const response = await createGame();
      if (response.session_id) {
        setSessionId(response.session_id);
      }
    } catch (error) {
      console.error('Error creating game:', error);
    }
  }, []);

  useEffect(() => {
    startCreateGame();
  }, [startCreateGame]);

  useEffect(() => {
    const initializeGame = async () => {
      if (sessionId) {
        await fetchBoard(sessionId);
        await fetchTurn(sessionId);
        setLoading(false);
      }
    };

    initializeGame();
  }, [sessionId]);

  const fetchBoard = async (session_id, retryCount = 3) => {
    try {
      const response = await get_board(session_id);
      if (response.length !== 0) {
        setBoard(convertGameStateToPosition(response));
      } else if (retryCount > 0) {
        console.warn("Board data empty, retrying...");
        setTimeout(() => fetchBoard(session_id, retryCount - 1), 1000);
      } else {
        console.error("Failed to load board data after multiple attempts");
      }
    } catch (error) {
      console.error('Error fetching board:', error);
    }
  };

  const fetchTurn = async (session_id) => {
    try {
      const response = await get_turn(session_id);
      setTurn(response.turn ? 'Blancas' : 'Negras');
    } catch (error) {
      console.error('Error fetching turn:', error);
    }
  };

  const make_against_move_ = async () => {
    try {
      const response_ = await make_move_against(sessionId, difficulty); // Considera la dificultad
      if (response_.success) {
        const gameState = response_.board;
        setBoard(convertGameStateToPosition(gameState));
      }
    } catch (error) {
      console.error('Error making move against:', error);
    }
  };

  const handleMove = async (sourceSquare, targetSquare) => {
    try {
      const move = convertMoveToIndices({ from: sourceSquare, to: targetSquare });
      const response = await make_move(sessionId, move);
      if (response.success) {
        const gameState = response.board;
        setBoard(convertGameStateToPosition(gameState));
        fetchTurn(sessionId);
        await new Promise(resolve => setTimeout(resolve, 1500));
        make_against_move_();
      } else {
        alert(response.message);
      }
    } catch (error) {
      console.error('Error making move:', error);
    }
  };

  const resetGame = async () => {
    try {
      await reset_game(sessionId);
      fetchBoard(sessionId);
      fetchTurn(sessionId);
    } catch (error) {
      console.error('Error resetting game:', error);
    }
  };

  const changeDifficulty = async () => {
    try {
      const difficulties = ['Facil', 'Normal', 'Dificil'];
      const currentIndex = difficulties.indexOf(difficulty);
      const nextIndex = (currentIndex + 1) % difficulties.length;
      setDifficulty(difficulties[nextIndex]);
      const response = await change_difficult(sessionId,difficulties[nextIndex])
      if (response.success){
        console.log("Dificultad cambiada")
      }
    } catch (error) {
      console.error('Error set difficult', error);
    }
 
  };

  async function onDrop(sourceSquare, targetSquare) {
    handleMove(sourceSquare, targetSquare);
    return true;
  }

  if (loading) {
    return <div>Cargando el juego de ajedrez...</div>;
  }

  return (

    <div style={{ marginBottom: '120px' }}>
      <div style={{ marginBottom: '10px' }}>
      
        <button  type="button" class="btn btn-warning me-5" onClick={changeDifficulty}>Cambiar Dificultad: {difficulty}</button>
        <button type="button" class="btn btn-success" onClick={resetGame}>Reiniciar Juego</button>
      </div>
      <ChessboardDnDProvider>
      <Chessboard
 
        position={board}
        onPieceDrop={onDrop}
        //clearPremovesOnRightClick	={false}
        boardWidth={boardWidth}
        customArrowColor='rgb(112,110,53)'
        customLightSquareStyle={{ backgroundColor: "#f2f8fc" }}
        customDarkSquareStyle={{ backgroundColor: '#0b6fe0' }}
      />
      </ChessboardDnDProvider>
    </div>

  );
};

export default ChessGame;