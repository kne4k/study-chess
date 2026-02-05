import { Chessboard } from 'react-chessboard';

interface ChessboardDisplayProps {
    position: string;
}

function ChessboardDisplay({ position }: ChessboardDisplayProps) {
    return (
        <div className="chessboard-container">
            <Chessboard
                options={{
                    position: position,
                }}
            />
        </div>
    );
}

export default ChessboardDisplay;
