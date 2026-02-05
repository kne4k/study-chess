interface NavigationControlsProps {
    currentPly: number;
    onStepForward: () => void;
    onStepBackward: () => void;
}

function NavigationControls({
    currentPly,
    onStepForward,
    onStepBackward
}: NavigationControlsProps) {
    return (
        <>
            <div className="controls-container">

                {/* Botão de retroceder */}
                <button className="control-button" onClick={onStepBackward}>
                    ◀ Voltar
                </button>

                {/* Contador de lances */}
                <span className="move-counter">
                    {currentPly === 0
                        ? "Posição inicial"
                        : `Lance ${Math.ceil(currentPly / 2)} - ${currentPly % 2 === 1 ? '⬜ Brancas' : '⬛ Pretas'}`
                    }
                </span>

                {/* Botão de avançar */}
                <button className="control-button" onClick={onStepForward}>
                    Avançar ▶
                </button>
            </div>
            <p className="keyboard-hint">
                Utilize as setas 🡄 🡆 do teclado para avançar e retroceder os lances.
            </p>
        </>
    );
}

export default NavigationControls;