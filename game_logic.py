class Game:
    def __init__(self):
        self.grid = [['' for _ in range(5)] for _ in range(5)]
        self.current_turn = 'A'  # Player A starts the game
        self.players = {'A': [], 'B': []}
        self.character_positions = {'A': {}, 'B': {}}

    def place_characters(self, player, characters):
        if player == 'A':
            self.players['A'] = characters
            for i, char in enumerate(characters):
                self.grid[0][i] = f'A-{char}'
                self.character_positions['A'][char] = (0, i)
        elif player == 'B':
            self.players['B'] = characters
            for i, char in enumerate(characters):
                self.grid[4][i] = f'B-{char}'
                self.character_positions['B'][char] = (4, i)

    def make_move(self, player, character, move):
        if character not in self.character_positions[player]:
            return False, "Invalid character."

        row, col = self.character_positions[player][character]
        direction = move

        # Calculate new position based on character type and movement direction
        if character.startswith('P'):
            new_row, new_col = self._move_pawn(row, col, direction, player)
        elif character.startswith('H1'):
            new_row, new_col = self._move_hero1(row, col, direction, player)
        elif character.startswith('H2'):
            new_row, new_col = self._move_hero2(row, col, direction, player)
        else:
            return False, "Unknown character type."

        if not self._is_valid_move(new_row, new_col, player):
            return False, "Invalid move."

        # Update grid and character position
        self.grid[row][col] = ''
        self.grid[new_row][new_col] = f'{player}-{character}'
        self.character_positions[player][character] = (new_row, new_col)

        return True, "Move successful."

    def _move_pawn(self, row, col, direction, player):
        if direction == 'L':
            return row, col - 1
        elif direction == 'R':
            return row, col + 1
        elif direction == 'F':
            return (row + 1) if player == 'A' else (row - 1), col
        elif direction == 'B':
            return (row - 1) if player == 'A' else (row + 1), col
        return row, col

    def _move_hero1(self, row, col, direction, player):
        if direction == 'L':
            return row, col - 2
        elif direction == 'R':
            return row, col + 2
        elif direction == 'F':
            return (row + 2) if player == 'A' else (row - 2), col
        elif direction == 'B':
            return (row - 2) if player == 'A' else (row + 2), col
        return row, col

    def _move_hero2(self, row, col, direction, player):
        if direction == 'FL':
            return (row + 2) if player == 'A' else (row - 2), col - 2
        elif direction == 'FR':
            return (row + 2) if player == 'A' else (row - 2), col + 2
        elif direction == 'BL':
            return (row - 2) if player == 'A' else (row + 2), col - 2
        elif direction == 'BR':
            return (row - 2) if player == 'A' else (row + 2), col + 2
        return row, col

    def _is_valid_move(self, new_row, new_col, player):
        if new_row < 0 or new_row >= 5 or new_col < 0 or new_col >= 5:
            return False
        if self.grid[new_row][new_col].startswith(player):
            return False
        return True

    def switch_turn(self):
        self.current_turn = 'B' if self.current_turn == 'A' else 'A'

    def check_winner(self):
        opponent = 'B' if self.current_turn == 'A' else 'A'
        return not any(self.grid[row][col].startswith(opponent) for row in range(5) for col in range(5))
