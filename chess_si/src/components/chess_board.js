import React, { useEffect, useState, useCallback , useMemo } from 'react';
import { Chessboard } from 'react-chessboard';

import { ChessboardDnDProvider } from 'react-chessboard';
import { get_board, get_turn, reset_game, make_move, make_move_against, createGame,change_difficult } from '../api/api';
import toast, { Toaster } from 'react-hot-toast';
import Card from 'react-bootstrap/Card';



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
  const boardWidth = useMemo(() => 600, []);

  const [messagealert,setMessage] = useState("");
  const startCreateGame = useCallback(async () => {
    if (sessionId!==null){
      console.log("Ya existe una session actual")
      return
    }
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
    if (sessionId==null){
      startCreateGame();
    }
    
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
      setTurn("Negras")
      const response_ = await make_move_against(sessionId, difficulty); // Considera la dificultad
      if (response_.success && response_.endgame==null ) {
        const gameState = response_.board;
        setBoard(convertGameStateToPosition(gameState));
        
      }else if (response_.endgame){
        //toast.error(response_.message,{duration:2100})
        toast((t) => (
          <span>
          {response_.message} {'\n Ganan : ' }
          <b>{response_.winner}</b>
            <hr></hr>
            <button class="btn btn-danger" onClick={resetGame}>
              Reiniciar
            </button>
          </span>
        ),{duration:3000});
        setMessage(response_.message)
        //alert(response.message)
      }else {
        //toast.error(response_.message ?? "Session inactiva o error del servidor",{duration:2100})
        toast((t) => (
          <span>
            {response_.message} 
            <br></br><br></br>
            <button class="btn btn-danger" onClick={resetGame}>
              Reiniciar
            </button>
          </span>
        ),{duration:3000});
        //return <Toaster></Toaster>
        //alert(response.message);
      }
    } catch (error) {
      console.error('Error making move against:', error);
    }
  };

  const handleMove = async (sourceSquare, targetSquare) => {
    try {
      const move = convertMoveToIndices({ from: sourceSquare, to: targetSquare });
      const response = await make_move(sessionId, move);
      if (response.success && response.endgame==null) {
        const gameState = response.board;
        setBoard(convertGameStateToPosition(gameState));
        fetchTurn(sessionId);
        await new Promise(resolve => setTimeout(resolve, 1500));
        make_against_move_();
        setTurn("Blancas")
      } else if (response.endgame){
        //toast.error(response.message,{duration:2100})
        toast((t) => (
          <span>
            {response.message} {'\n Ganan : ' }
            <b>{response.winner}</b>
            <hr></hr>
            <button class="btn btn-danger" onClick={resetGame}>
              Reiniciar
            </button>
          </span>
        ),{duration:3000});
        //return <Toaster></Toaster>
        setMessage(response.message)
        //alert(response.message)
      }else {
        toast.error(
          <b>{response.message ?? "Session inactiva o error del servidor"}
          </b>,
          {duration:2100})
     
        //return <Toaster></Toaster>
        //alert(response.message);
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
      window.location.reload()
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
    <><Toaster></Toaster><div style={{ marginBottom: '120px' }}>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' ,marginLeft:'280px'}}>
      <div>
        <ChessboardDnDProvider>
          <Chessboard
            position={board}
            onPieceDrop={onDrop}
            boardWidth={boardWidth}
            customArrowColor='rgb(112,110,53)'
            customLightSquareStyle={{ backgroundColor: "#f2f8fc" }}
            customDarkSquareStyle={{ backgroundColor: '#0b6fe0' }}
          />
        </ChessboardDnDProvider>
      </div>
    
      <div>
        <Card style={{ width: '18rem', marginLeft: '20px' }}>
          <Card.Body>
            <Card.Title>Turno Actual</Card.Title>
            
            <Card.Text>
            
                {"Fichas : "}<b>{turn}</b>
            </Card.Text>
            <hr></hr>
            <div style={{ marginBottom: '10px' }}>

            <button type="button" class="btn btn-warning mb-3" onClick={changeDifficulty}>Cambiar Dificultad: {difficulty}</button>
            <button type="button" class="btn btn-success" onClick={resetGame}>Reiniciar Juego</button>
          </div>
          </Card.Body>
        </Card>
      </div>
    </div>
    </div></>

  );
};

export default ChessGame;