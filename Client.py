import socket
import json

HOST = 'localhost'
PORT = 65432

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        while True:
            data = s.recv(1024).decode('utf-8')
            if not data:
                break
            message = json.loads(data)

            if message['type'] == "init":
                player_id = message['player']
                print(f"Connected as Player {player_id}")
                place_characters(s, player_id)
            elif message['type'] == "update":
                print(f"Current Board (Turn: Player {message['turn']}):")
                for row in message['board']:
                    print(" ".join([cell if cell else "." for cell in row]))
                if message['turn'] == player_id:
                    make_move(s, player_id)
            elif message['type'] == "game_over":
                print(f"Game Over! Winner: Player {message['winner']}")
                break
            elif message['type'] == "fail":
                print(f"Move failed: {message['message']}")
                make_move(s, player_id)

def place_characters(sock, player_id):
    positions = input(f"Player {player_id}, enter your characters in format P1,H1,H2 (e.g., P1,P2,H1,H2,H3): ").split(",")
    sock.sendall(json.dumps({"type": "place", "positions": positions}).encode('utf-8'))

def make_move(sock, player_id):
    move = input(f"Player {player_id}, enter your move (e.g., P1:L, H2:FL): ")
    char, move = move.split(":")
    sock.sendall(json.dumps({"type": "move", "player": player_id, "char": char, "move": move}).encode('utf-8'))

if __name__ == "__main__":
    main()
