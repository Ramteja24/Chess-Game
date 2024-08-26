from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from game_logic import Game

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('game_state', {
        'grid': game.grid,
        'current_turn': game.current_turn
    })

@socketio.on('place_characters')
def handle_place_characters(data):
    player = data['player']
    characters = data['characters']
    game.place_characters(player, characters)
    emit('game_state', {
        'grid': game.grid,
        'current_turn': game.current_turn
    }, broadcast=True)

@socketio.on('make_move')
def handle_make_move(data):
    player = data['player']
    character = data['character']
    move = data['move']
    
    if game.current_turn != player:
        emit('error', {'error': 'Not your turn!'})
        return

    success, message = game.make_move(player, character, move)
    if not success:
        emit('error', {'error': message})
    else:
        # Switch turn after a successful move
        game.switch_turn()

        emit('game_state', {
            'grid': game.grid,
            'current_turn': game.current_turn
        }, broadcast=True)
        
        if game.check_winner():
            emit('game_over', {'winner': player}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
