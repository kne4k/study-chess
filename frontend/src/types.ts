// Define o formato da explicação do movimento
export interface MoveExplanation {
    ply: number;
    content: string;
    color: boolean;
}

// Define o formato dos dados da partida completa
export interface GameData {
    id: number;
    variant_name: string;
    pgn: string;
    explanations: MoveExplanation[];
    white_player: string;
    black_player: string;
    event: string;
}