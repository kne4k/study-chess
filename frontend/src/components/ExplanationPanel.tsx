interface ExplanationPanelProps {
    title: string;
    white_player: string;
    black_player: string;
    event: string;
    explanation: string;
}

function ExplanationPanel({ title, white_player, black_player, event, explanation }:
    ExplanationPanelProps) {
    return (
        <div className="right-column">
            <h2 className="title-variant">
                {title}
            </h2>
            <h3 className="title-players">
                Brancas: {white_player} vs Pretas: {black_player}
            </h3>
            <p className="title-event">
                {event}
            </p>
            {explanation.split('\n').map((line, i) => (
                <p key={i} className="explanation-text">
                    {line}
                </p>
            ))}
        </div>
    );
}

export default ExplanationPanel;
