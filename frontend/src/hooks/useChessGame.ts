//Imports
import { useState, useEffect, useCallback } from "react";
import { Chess } from "chess.js";
import axios from "axios";
import type { GameData } from "../types";

//Custom Hook
export function useChessGame() {

    //Estados utilizados
    // Estado do jogo (Armazena a posição atual do tabuleiro, inicia o tabuleiro sem lances executados)
    const [game, setGame] = useState(new Chess());

    // Lista de lances da partida escolhida (array com todos os movimentos)
    const [moveHistory, setMoveHistory] = useState<string[]>([]);

    // Índice do lance atual no histórico (0 = posição inicial)
    const [currentPly, setCurrentPly] = useState(0);

    // Lista de variantes disponíveis no backend
    const [gamesList, setGamesList] = useState<GameData[]>([]);

    // Variante selecionada, nulo se não foi selecionada nenhuma
    const [selectedGame, setSelectedGame] = useState<GameData | null>(null);

    // Explicação da variante (texto do painel direito)
    const [currentExplanation, setCurrentExplanation] = useState<string>("");


    //Funções
    // Carrega a partida selecionada pelo usuário
    function loadGame(gameData: GameData) {
        // Marca este jogo como o selecionado
        setSelectedGame(gameData);
        // Cria um tabuleiro temporário/invisível
        // POR QUE: Precisamos carregar o PGN para extrair os lances
        // mas sem afetar o tabuleiro visual ainda
        const masterGame = new Chess();

        try {
            // Carrega o PGN no tabuleiro temporário
            // PGN = "1. e4 e5 2. Nf3 Nc6" (notação completa da partida)
            masterGame.loadPgn(gameData.pgn);
            // Extrai os lances do PGN
            // masterGame.history() retorna: ["e4", "e5", "Nf3", "Nc6"]
            // Salva esse array no estado moveHistory
            setMoveHistory(masterGame.history());
            // Reseta o tabuleiro visual para a posição inicial
            // POR QUE: Queremos que o usuário veja a posição inicial primeiro
            setGame(new Chess());

            // Volta para o índice 0 (posição inicial)
            setCurrentPly(0);

            // Atualiza a explicação para a posição inicial
            updateExplanation(0, gameData);
        } catch (e) {
            // Se der erro ao carregar o PGN
            console.error("Erro ao carregar o histórico de movimentos da partida:", e);
            setCurrentExplanation("Erro: O histórico de movimentos desta partida é inválido ou não pode ser carregado.");
        }
    }

    // Atualiza a explicação baseada no lance atual
    function updateExplanation(ply: number, activeGame: GameData | null) {
        // Se não há jogo selecionado, não faz nada
        if (!activeGame) return;
        // Procura explicação para este ply no array de explicações
        // find() retorna o primeiro item que satisfaz a condição
        // ou undefined se não encontrar
        const explanation = activeGame.explanations.find(exp => exp.ply === ply);
        if (explanation) {
            // Se encontrou explicação, exibe o conteúdo dela
            setCurrentExplanation(explanation.content);
        } else {
            // Se não encontrou explicação

            if (ply === 0) {
                // Posição inicial tem mensagem especial
                setCurrentExplanation(
                    "Você escolheu: " + activeGame.variant_name + ".\n" +
                    "Estamos na posição inicial.\n" +
                    "Avance e retroceda os lances para verificar as explicações."
                );
            } else {
                // Outros lances sem explicação: mostra "..."
                setCurrentExplanation("...");

            }
        }
    }

    //Callbacks
    // Avança para o próximo lance
    const stepForward = useCallback(() => {
        // Verifica se chegou no final do histórico
        // Se currentPly já é igual ao número total de lances, não avança
        if (currentPly >= moveHistory.length) return;
        // Calcula o próximo índice
        const nextPly = currentPly + 1;

        // Atualiza o estado com o novo índice
        setCurrentPly(nextPly);
        // Reconstrói o tabuleiro do zero
        setGame(() => {
            // Cria um tabuleiro completamente novo (posição inicial)
            const newGame = new Chess();
            // Aplica todos os lances do início até o novo índice
            // Loop: i vai de 0 até nextPly-1
            // Exemplo: se nextPly = 3, aplica lances 0, 1, 2
            for (let i = 0; i < nextPly; i++) {
                newGame.move(moveHistory[i]);
            }

            // Retorna o novo tabuleiro com a posição correta
            return newGame;
        });
    }, [currentPly, moveHistory]);

    // Retrocede para o lance anterior
    const stepBackward = useCallback(() => {
        // Verifica se já está na posição inicial
        // Se currentPly é 0, não pode retroceder mais
        if (currentPly <= 0) return;
        // Calcula o índice anterior
        const previousPly = currentPly - 1;

        // Atualiza o estado
        setCurrentPly(previousPly);
        // Reconstrói o tabuleiro
        setGame(() => {
            const newGame = new Chess();
            // Aplica lances até o índice anterior
            // Exemplo: se previousPly = 2, aplica lances 0 e 1
            for (let i = 0; i < previousPly; i++) {
                newGame.move(moveHistory[i]);
            }

            return newGame;
        });
    }, [currentPly, moveHistory]);


    //Effects
    //Effect de buscar jogos do backend
    useEffect(() => {
        // Faz requisição GET para buscar todos os jogos
        axios.get('http://localhost:8000/api/games/')

            .then(response => {
                // Quando a resposta chegar com sucesso

                // Salva o array de jogos no estado
                setGamesList(response.data);

            })
            .catch(error => {
                // Se der erro na requisição (backend offline, erro de rede, etc)
                console.error("Erro ao buscar as partidas:", error);
            });
    }, []);

    //Effect de atualizar a explicação
    useEffect(() => {
        updateExplanation(currentPly, selectedGame);
    }, [currentPly, selectedGame]);

    //Effect de controle pelo teclado
    useEffect(() => {

        // Função que detecta qual tecla foi pressionada
        function handleKeyDown(e: KeyboardEvent) {
            // e = evento que contém informações sobre a tecla

            if (e.key === "ArrowRight") {
                // Se pressionou seta direita, avança
                stepForward();

            } else if (e.key === "ArrowLeft") {
                // Se pressionou seta esquerda, retrocede
                stepBackward();
            }
        }
        // Registra o listener: "escuta" todos os eventos de teclado
        // "keydown" = quando uma tecla é pressionada
        window.addEventListener("keydown", handleKeyDown);

        // Cleanup: função de limpeza
        // Executa quando o componente que usa o hook desmontar
        return () => {
            // Remove o listener para evitar memory leak
            window.removeEventListener("keydown", handleKeyDown);
        };

    }, [stepForward, stepBackward]);

    return {

        // ESTADOS (dados para mostrar na interface)

        game, // Tabuleiro atual (objeto Chess)
        currentPly, // Índice do lance atual (número)
        gamesList, // Lista de jogos disponíveis (array)
        selectedGame, // Jogo selecionado (objeto ou null)
        currentExplanation, // Texto da explicação (string)

        // FUNÇÕES (ações que o usuário pode fazer)
        loadGame, // Carregar uma partida
        stepForward, // Avançar lance
        stepBackward // Retroceder lance
    };
}
