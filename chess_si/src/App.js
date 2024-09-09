import logo from './logo.svg';
import './App.css';
import { Router,Route,RouterProvider } from 'react-router-dom';
import Chess_board from './components/chess_board';
function App() {
  return (
    <div className="App">
      <h1>Chess 960</h1>
      <div style={{display: 'flex',  justifyContent:'center', alignItems:'center',width:600,height:600,paddingLeft:"470px"}}>
      <Chess_board></Chess_board></div>
    </div>
  );
}

export default App;
