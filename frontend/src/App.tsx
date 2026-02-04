import { useState, useEffect, useCallback } from "react";
import { Chess } from "chess.js";
import { Chessboard } from "react-chessboard";
import axios from 'axios';
import type { GameData } from './types';
import './App.css';

function App() {

  // Estado do jogo (inicia o tabuleiro sem lances executados)
  const [game, setGame] = useState(new Chess());

  // Lista de lances da partida escolhida
  const [moveHistory, setMoveHistory] = useState<string[]>([]);

  // Em qual lance estamos
  const [currentPly, setCurrentPly] = useState(0);

  const [gamesList, setGamesList] = useState<GameData[]>([]);
  const [selectedGame, setSelectedGame] = useState<GameData | null>(null);
  const [currentExplanation, setCurrentExplanation] = useState<string>("Selecione uma variante para começar!");

  // Busca de dados do backend
  useEffect(() => {
    axios.get('http://localhost:8000/api/games/')
      .then(response => {
        setGamesList(response.data);
        if (response.data.length > 0) {
          loadGame(response.data[0]);
        }
      })
      .catch(error => console.error("Erro ao buscar as partidas:", error));
  }, []);

  // Carregar a partida e preparar o histórico de movimentos
  function loadGame(gameData: GameData) {
    setSelectedGame(gameData);

    // Cria uma partida invisível com os lances para poder extrair o histórico de movimentos
    const masterGame = new Chess();
    try {
      // Carrega o PGN da partida na partida invisível
      masterGame.loadPgn(gameData.pgn);

      // Salva a sequência de lances corretos na memória
      setMoveHistory(masterGame.history());

      // Reseta o tabuleiro visual para a posição inicial
      setGame(new Chess());
      setCurrentPly(0);
      updateExplanation(0, gameData);

    } catch (e) {
      console.error("Erro ao carregar o histórico de movimentos da partida:", e);
      setCurrentExplanation("Erro: O histórico de movimentos desta partida é inválido ou não pode ser carregado.");
    }
  }

  // Atualizar a explicação conforme o lance equivalente
  function updateExplanation(ply: number, activeGame: GameData | null) {
    if (!activeGame) return;

    const explanation = activeGame.explanations.find(exp => exp.ply === ply);

    if (explanation) {
      setCurrentExplanation(explanation.content);
    } else {
      if (ply === 0) {
        setCurrentExplanation("Você escolheu a variante: " + activeGame.variant_name + ". Estamos na posição inicial. Avance e retroceda os lances para verificar as explicações.")
      } else {
        // Deixa vazio o campo da explicação
        setCurrentExplanation("...");
      }
    }
  }

  // Função da navegação entre os lances

  // Avançar para o próximo lance
  const stepForward = useCallback(() => {

    // Chegou no final do histórico de lances
    if (currentPly >= moveHistory.length) return;

    // Avança para o próximo lance
    const nextPly = currentPly + 1;
    setCurrentPly(nextPly);

    // Reconstrói o tabuleiro do zero até o índice atual do lance
    setGame(() => {
      // Cria uma nova instância do tabuleiro
      const newGame = new Chess();

      // Executa todos os lances sequencialmente até o novo índice
      for (let i = 0; i < nextPly; i++) {
        newGame.move(moveHistory[i])
      }
      return newGame;
    });

  }, [currentPly, moveHistory]);

  // Retroceder para o lance anterior
  const stepBackward = useCallback(() => {

    // Já está na posição inicial
    if (currentPly <= 0) return;

    // Retrocede para o lance anterior
    const previousPly = currentPly - 1;
    setCurrentPly(previousPly);

    // Reconstrói o tabuleiro do zero até o índice atual do lance
    setGame(() => {
      // Cria uma nova instância do tabuleiro
      const newGame = new Chess();

      // Executa todos os lances sequencialmente até o novo índice
      for (let i = 0; i < previousPly; i++) {
        newGame.move(moveHistory[i])
      }
      return newGame;
    });

  }, [currentPly, moveHistory]);

  // Atualiza a explicação sempre que o índice do lance mudar
  useEffect(() => {
    updateExplanation(currentPly, selectedGame);
  }, [currentPly, selectedGame])

  // Controle pelo teclado
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "ArrowRight") {
        stepForward();
      } else if (e.key === "ArrowLeft") {
        stepBackward();
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [stepForward, stepBackward]);

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'row', alignItems: 'center' }}>

      {/* Coluna esquerda: Lista e tabuleiro */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>

        {/* Seletor de variantes */}
        <select
          onChange={(e) => {
            const gameId = parseInt(e.target.value);
            const g = gamesList.find(x => x.id === gameId);
            if (g) loadGame(g);
          }}
          style={{ marginBottom: '10px', padding: '5px', fontSize: '16px' }}
          value={selectedGame?.id || ""}
        >
          {gamesList.map(g => (
            <option key={g.id} value={g.id}>{g.variant_name}</option>
          ))}
        </select>

        {/* Tabuleiro */}
        <Chessboard
          options={{
            position: game.fen(),
          }}
        />


        {/* Botões de controle*/}


        <button onClick={stepBackward} style={btnStyle}>
          ◀ Voltar
        </button>
        <span style={{ fontSize: '20px', fontWeight: 'bold', alignSelf: 'center' }}>
          {Math.ceil(currentPly / 2)}.{currentPly % 2 === 1 ? '...' : ''}
        </span>
        <button onClick={stepForward} style={btnStyle}>
          Avançar ▶
        </button>

        <p style={{ marginTop: '10px', color: '#333', fontSize: '14px' }}>
          Dica: Utilize as setas ⬅ ➡ do teclado para avançar e retroceder os lances.
        </p>
      </div>

      {/* Coluna direita: explicações */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <h2 style={{ color: '#333', borderBottom: '2px solid #4CAF50', paddingBottom: '10px' }}>
          {selectedGame ? selectedGame.variant_name : "Estudo"}
        </h2>
        {currentExplanation.split('\n').map((line, i) => (
          <p key={i}>{line}</p>
        ))}
      </div>

    </div >
  );
}

// Estilo dos botões
// Estilo simples para os botões
const btnStyle = {
  padding: '10px 20px',
  fontSize: '16px',
  cursor: 'pointer',
  backgroundColor: '#2196F3',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  minWidth: '100px'
};


export default App;