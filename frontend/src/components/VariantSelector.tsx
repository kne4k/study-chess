//Importando tipos do arquivo types.ts
import { useRef } from 'react';
import type { GameData } from '../types'

//Interface do componente
interface VariantSelectorProps {

    //Array de partidas
    gamesList: GameData[];

    //Partida selecionada
    selectedGame: GameData | null;

    //Função chamada ao selecionar uma partida
    onGameSelect: (gameData: GameData) => void;
}

//Componente
function VariantSelector({ gamesList, selectedGame, onGameSelect }: VariantSelectorProps) {
    const variantSelectorRef = useRef<HTMLSelectElement>(null);
    return (
        <select
            onChange={(e) => {
                const gameId = parseInt(e.target.value);
                const g = gamesList.find(x => x.id === gameId);
                if (g) onGameSelect(g);
                variantSelectorRef.current?.blur();
            }}
            className="variant-selector"
            value={selectedGame?.id || ""}
            required={true}


            ref={variantSelectorRef}
            onKeyDown={(e) => {
                e.stopPropagation();
            }}
        >
            {/* Placeholder */}
            <option value="" disabled hidden>
                Variantes
            </option>

            {/* Lista de partidas */}
            {gamesList.map(g => (
                <option key={g.id} value={g.id}>
                    {g.variant_name}
                </option>
            ))}
        </select >
    );
}

//Exportando o componente
export default VariantSelector;