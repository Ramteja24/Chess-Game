var socket = io();

var currentPlayer = null;

socket.on('game_state', function(data) {
    const board = document.getElementById('board');
    board.innerHTML = ''; // Clear the board
    currentPlayer = data.current_turn;

    data.grid.forEach((row, rowIndex) => {
        row.forEach((cell, cellIndex) => {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'cell';
            cellDiv.textContent = cell;
            
            if (cell.startsWith('A-')) {
                cellDiv.classList.add('playerA');
            } else if (cell.startsWith('B-')) {
                cellDiv.classList.add('playerB');
            }

            cellDiv.addEventListener('click', function() {
                if (cell.startsWith(currentPlayer)) {
                    handleCellClick(rowIndex, cellIndex);
                } else {
                    console.log("Not your turn!");
                }
            });

            board.appendChild(cellDiv);
        });
    });

    document.getElementById('status').innerText = "Current turn: " + data.current_turn;
});

socket.on('error', function(data) {
    document.getElementById('error').innerText = data.error;
});

socket.on('game_over', function(data) {
    alert("Game over! Winner: " + data.winner);
});

function handleCellClick(row, col) {
    console.log(`Cell clicked at row ${row}, col ${col}`);
    // Ask player which move to make (e.g., L, R, F, B, etc.)
    const character = prompt("Enter the character you want to move (e.g., P1, H1, H2):");
    const move = prompt("Enter the move direction (L, R, F, B, FL, FR, BL, BR):");
    makeMove(currentPlayer, character, move);
}

function placeCharacters(player, characters) {
    socket.emit('place_characters', {
        player: player,
        characters: characters
    });
}

function makeMove(player, character, move) {
    if (player !== currentPlayer) {
        alert("It's not your turn!");
        return;
    }
    
    socket.emit('make_move', {
        player: player,
        character: character,
        move: move
    });
}
