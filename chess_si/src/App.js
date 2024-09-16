import logo from './logo.svg';
import './App.css';
import { Router, Route, RouterProvider } from 'react-router-dom';
import Chess_board from './components/chess_board';

function App() {
  return (
    <div className="App">
      <h1 style={{ marginBottom: '50px' }}>Chess 960</h1>
      <div 
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          width: '100%',   // Use 100% width for responsive layout
          height: '100vh', // Full viewport height
         
        }}
      >
        <Chess_board  /> {/* Passing desired board width as prop */}
      </div>
    </div>
  );
}

export default App;
