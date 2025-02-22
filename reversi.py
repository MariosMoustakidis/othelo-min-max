import math
import copy

# Constants representing the players and empty cells
EMPTY = '.'
PLAYER = 'X'  # Human player
AI = 'O'  # Computer player

# Directions to check for valid moves (8 surrounding directions)
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1), (0, 1),
              (1, -1), (1, 0), (1, 1)]


class Reversi:
    def __init__(self):
        # Initialize the game board with the starting position.
        self.board = self.initialize_board()

    def initialize_board(self):
        """
        Create an 8x8 board and set up the initial four pieces in the center.

        Returns:
            list: A 2D list representing the game board.
        """
        # Create an 8x8 board filled with EMPTY
        board = [[EMPTY for _ in range(8)] for _ in range(8)]

        # Set up the initial four pieces in the center
        board[3][3] = PLAYER
        board[4][4] = PLAYER
        board[3][4] = AI
        board[4][3] = AI
        return board

    # Count the number of pieces a player has on the board.
    def count(self, player):
        return sum(row.count(player) for row in self.board)

    # Check if the given coordinates are within the board boundaries.
    def is_on_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    # Determine all valid moves for a player.
    def valid_moves(self, player):
        valid = set()
        opponent = PLAYER if player == AI else AI

        # Iterate over every cell on the board
        for x in range(8):
            for y in range(8):
                if self.board[x][y] != EMPTY:
                    continue  # Skip occupied cells

                # Check all directions from the current cell
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if self.is_on_board(nx, ny) and self.board[nx][ny] == opponent:
                        # Move in the current direction
                        while self.is_on_board(nx, ny) and self.board[nx][ny] == opponent:
                            nx += dx
                            ny += dy
                        # Check if the chain ends with the current player's piece
                        if self.is_on_board(nx, ny) and self.board[nx][ny] == player:
                            valid.add((x, y))
                            break  # No need to check other directions for this cell
        return list(valid)
    # Place a piece for the player at the specified position and flip opponent's pieces.
    def make_move(self, player, x, y):
        if (x, y) not in self.valid_moves(player):
            return False  # Invalid move

        self.board[x][y] = player  # Place the player's piece
        opponent = PLAYER if player == AI else AI

        # Flip opponent's pieces in all valid directions
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            tiles_to_flip = []

            # Move in the current direction
            while self.is_on_board(nx, ny) and self.board[nx][ny] == opponent:
                tiles_to_flip.append((nx, ny))
                nx += dx
                ny += dy

            # If the chain ends with the player's piece, flip the tiles
            if self.is_on_board(nx, ny) and self.board[nx][ny] == player:
                for fx, fy in tiles_to_flip:
                    self.board[fx][fy] = player

        return True

    def is_game_over(self):
        return not self.valid_moves(PLAYER) and not self.valid_moves(AI)

    # Evaluate the board state from the AI's perspective.
    def evaluate(self):
        return self.count(AI) - self.count(PLAYER)

    def minimax(self, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.is_game_over():
            return self.evaluate(), None  # Return the evaluation score

        current_player = AI if maximizing_player else PLAYER
        moves = self.valid_moves(current_player)

        if not moves:
            # No valid moves, switch player
            return self.minimax(depth - 1, not maximizing_player, alpha, beta)[0], None

        best_move = None

        if maximizing_player:
            max_eval = -math.inf
            for move in moves:
                new_game = copy.deepcopy(self)  # Create a deep copy of the game state
                new_game.make_move(current_player, move[0], move[1])  # Simulate the move
                eval, _ = new_game.minimax(depth - 1, False, alpha, beta)  # Recurse
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)  # Update alpha
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval, best_move
        else:
            min_eval = math.inf
            for move in moves:
                new_game = copy.deepcopy(self)  # Create a deep copy of the game state
                new_game.make_move(current_player, move[0], move[1])  # Simulate the move
                eval, _ = new_game.minimax(depth - 1, True, alpha, beta)  # Recurse
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)  # Update beta
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval, best_move


def play_game():
    game = Reversi()
    current_player = PLAYER  # Player starts first

    while True:
        print_board(game.board)

        if current_player == PLAYER:
            moves = game.valid_moves(PLAYER)
            if not moves:
                print("You have no valid moves. Turn is passed to the AI.")
                # Check if AI also has no moves
                if not game.valid_moves(AI):
                    print("No valid moves left for both players. Game over.")
                    break
                current_player = AI
                continue  # Skip to AI's turn

            move = get_player_move(game)
            if move:
                game.make_move(PLAYER, move[0], move[1])
                current_player = AI
        else:
            print("AI is thinking...")
            moves = game.valid_moves(AI)
            if not moves:
                print("AI has no valid moves. Turn is passed to you.")
                # Check if Player also has no moves
                if not game.valid_moves(PLAYER):
                    print("No valid moves left for both players. Game over.")
                    break
                current_player = PLAYER
                continue  # Skip to Player's turn

            _, move = game.minimax(depth=4, maximizing_player=True, alpha=-math.inf, beta=math.inf)
            if move:
                game.make_move(AI, move[0], move[1])
                print(f"AI placed at position: {move}")
                current_player = PLAYER

        # Check if the game is over after each move
        if game.is_game_over():
            print("No valid moves left for both players. Game over.")
            break

    # Game over, display results
    print_board(game.board)
    player_score = game.count(PLAYER)
    ai_score = game.count(AI)
    print(f"Final Score - Player: {player_score}, AI: {ai_score}")
    if player_score > ai_score:
        print("Congratulations! You win!")
    elif player_score < ai_score:
        print("AI wins. Better luck next time!")
    else:
        print("It's a tie!")

#Helper function to print the game board.
def print_board(board):

    print("  " + " ".join(str(i) for i in range(8)))
    for idx, row in enumerate(board):
        print(f"{idx} " + " ".join(row))
    print()


def get_player_move(game):
    """
    Get a valid move from the player.
    This function includes input validation and returns the move as a tuple (x, y).
    """
    while True:
        try:
            move_input = input("Enter your move as 'row col' (e.g., '2 3'): ")
            if move_input.lower() in ['quit', 'exit']:
                print("Exiting the game.")
                exit()
            x, y = map(int, move_input.strip().split())
            if (x, y) in game.valid_moves(PLAYER):
                return (x, y)
            else:
                print("Invalid move. Please try again.")
        except ValueError:
            print("Invalid input format. Please enter two numbers separated by a space.")
