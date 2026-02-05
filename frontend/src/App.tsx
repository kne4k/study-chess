import { useChessGame } from "./hooks/useChessGame";
import './App.css';
import VariantSelector from "./components/VariantSelector";
import ChessboardDisplay from "./components/ChessboardDisplay";
import NavigationControls from "./components/NavigationControls";
import ExplanationPanel from "./components/ExplanationPanel";

function App() {

  //Importa os estados e funções do hook useChessGame
  const {
    game,
    currentPly,
    gamesList,
    selectedGame,
    currentExplanation,
    loadGame,
    stepForward,
    stepBackward
  } = useChessGame();

  return (
    <div className="app-container">

      {/* Coluna esquerda: Lista, tabuleiro e botões de controle */}
      <div className="left-column">

        {/* Seletor de variantes */}
        <VariantSelector
          gamesList={gamesList}
          selectedGame={selectedGame}
          onGameSelect={loadGame}
        />

        {/* Tabuleiro */}
        <ChessboardDisplay position={game.fen()} />

        {/* Botões de controle*/}
        <NavigationControls
          currentPly={currentPly}
          onStepForward={stepForward}
          onStepBackward={stepBackward}
        />
      </div>

      {/* Coluna direita: explicações */}
      <ExplanationPanel
        title={selectedGame ? selectedGame.variant_name : "Selecione uma variante para começar!"}
        white_player={selectedGame ? selectedGame.white_player : ""}
        black_player={selectedGame ? selectedGame.black_player : ""}
        event={selectedGame ? selectedGame.event : ""}
        explanation={currentExplanation}
      />
    </div >
  );
}

export default App;