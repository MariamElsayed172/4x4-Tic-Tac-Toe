import tkinter as tk
from tkinter import messagebox
import math
import time
import random


class Board:
    players = ['x', 'O', '']

    def __init__(self):
        self.board = [[['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']],
                      [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']],
                      [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']],
                      [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]]
        self.current_player = self.players[0]  # Set default player to 'x'
        self.AI_player = None

    def set_player(self, player):
        if player in self.players:
            self.current_player = player
        else:
            raise ValueError("Invalid player. Choose from:", self.players)

    def set_AI_player(self):
        if self.current_player == 'x':
            self.AI_player = 'O'
        elif self.current_player == 'O':
            self.AI_player = 'x'
        elif self.current_player == '':
            None
        else:
            raise ValueError("Invalid current player. Cannot determine AI player.")

    def set_value(self, layer, row, column):
        if self.board[layer][row][column] == '':
            self.board[layer][row][column] = self.current_player
        else:
            print("Cell already occupied.")

    def get_value(self, layer, row, column):
        return self.board[layer][row][column]

    def undo_move(self, layer, row, column):
        self.board[layer][row][column] = ''

    def turn(self):
        # Switch the current player after each turn
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def is_win(self, player):
        # Check rows
        for layer in self.board:
            for row in layer:
                if all(cell == player for cell in row):
                    return True

        # Check columns
        for col in range(4):
            for layer in self.board:
                if all(row[col] == player for row in layer):
                    return True

        # Check diagonals within layers
        for layer in self.board:
            if all(layer[i][i] == player for i in range(4)) or all(
                    layer[i][3 - i] == player for i in range(4)):
                return True

        # Check across layers
        for col in range(4):
            for row in range(4):
                if all(self.board[l][row][col] == player for l in range(4)):
                    return True
                
        # Check columns between layers
        for col in range(4):
                if all(self.board[i][i][col] == player for i in range(4)):
                    return True 
        
        # check rows between layers 
        for row in range(4):
                if all(self.board[i][row][i] == player for i in range(4)):
                    return True                    

        # Check diagonals between layers
        if all(self.board[i][i][i] == player for i in range(4)) or all(
                self.board[i][i][3 - i] == player for i in range(4)):
            return True

        if all(self.board[i][3 - i][i] == player for i in range(4)) or all(
                self.board[i][3 - i][3 - i] == player for i in range(4)):
            return True

        return False

    def is_empty(self):
        # Check if the entire board is empty
        return all(
            self.board[layer][row][column] == '' for layer in range(4) for row in range(4) for column in range(4))

    def is_full(self):
        # Check if the entire board is full
        return all(
            self.board[layer][row][column] != '' for layer in range(4) for row in range(4) for column in range(4))

    def get_invalid_spaces(self):
        invalid_spaces = []
        for layer in range(4):
            for row in range(4):
                for column in range(4):
                    if self.board[layer][row][column] not in self.players:
                        invalid_spaces.append((layer, row, column))
        return invalid_spaces

    def reset_board(self):
        for layer in range(4):
            for row in range(4):
                for column in range(4):
                    self.board[layer][row][column] = ''
                    
    def evaluate_line(line):
        # Evaluate a line (row, column, or depth) for the heuristic
        if line.count('X') == 4:
            return 100  # Maximizer (PLAYER_X) wins
        elif line.count('O') == 4:
            return -100  # Minimizer (PLAYER_O) wins
        elif line.count('X') == 3 and line.count('') == 1:
            return 10  # Maximizer has three in a row with one empty cell
        elif line.count('O') == 3 and line.count('') == 1:
            return -10  # Minimizer has three in a row with one empty cell
        elif line.count('X') == 2 and line.count('') == 2:
            return 5  # Maximizer has two in a row with two empty cells
        elif line.count('O') == 2 and line.count('') == 2:
            return -5  # Minimizer has two in a row with two empty cells
        else:
            return 0  # No winner in the line

    def heuristic_evaluation(self):
    # Symmetric heuristic evaluation function
        score = 0

        # Check rows, columns, and depth
        for i in range(4):
            for j in range(4):
                # Rows and columns
                score += Board.evaluate_line([self.board[i][j][k] for k in range(4)])

                # Depth
                score += Board.evaluate_line([self.board[i][k][j] for k in range(4)])

        # Check diagonals in each layer
        for i in range(4):
            # Main diagonals
            score += Board.evaluate_line([self.board[i][j][j] for j in range(4)])
            score += Board.evaluate_line([self.board[i][j][3 - j] for j in range(4)])

            # Side diagonals
            score += Board.evaluate_line([self.board[i][3 - j][j] for j in range(4)])
            score += Board.evaluate_line([self.board[i][3 - j][3 - j] for j in range(4)])

        # Check along the depth dimension
        for j in range(4):
            for k in range(4):
                # Diagonals in depth
                score += Board.evaluate_line([self.board[i][j][k] for i in range(4)])

                # Side diagonals in depth
                score += Board.evaluate_line([self.board[3 - i][j][k] for i in range(4)])

        return score
    
    


    def minimax_with_heuristic(self, depth, maximizing_player):
        if depth == 0 or self.is_win('x') or self.is_win('O') or self.is_full():
            return self.heuristic_evaluation()

        if maximizing_player:
            max_eval = -math.inf
            for layer in range(4):
                for row in range(4):
                    for col in range(4):
                        if self.board[layer][row][col] == '':
                            self.board[layer][row][col] = self.AI_player
                            eval = self.minimax_with_heuristic(depth - 1, False)
                            self.undo_move(layer, row, col)  # Undo the move
                            max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for layer in range(4):
                for row in range(4):
                    for col in range(4):
                        if self.board[layer][row][col] == '':
                            self.board[layer][row][col] = self.players[0]
                            eval = self.minimax_with_heuristic(depth - 1, True)
                            self.undo_move(layer, row, col)  # Undo the move
                            min_eval = min(min_eval, eval)
            return min_eval


class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("4x4x4 Tic Tac Toe")

        self.board = Board()
        self.create_widgets()
        self.set_players("x")
        self.update_status()

    def set_players(self, player):
        self.board.set_player(player)
        self.board.set_AI_player()

    def create_widgets(self):
        self.buttons = [
            [
                [
                    tk.Button(
                        self.master, text='', width=4, height=2,
                        command=lambda layer=l, row=r, col=c: self.make_move(layer, row, col),
                        bg='coral'  # Set the background color for buttons to coral
                    )
                    for c in range(4)
                ]
                for r in range(4)
            ]
            for l in range(4)
        ]

        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    self.buttons[layer][row][col].grid(row=row + layer * 4, column=col + layer * 4, padx=5, pady=0)

        self.status_label = tk.Label(self.master, text=f"Current Player: {self.board.current_player}", bg='misty rose')
        self.status_label.grid(row=16, columnspan=4)
        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, bg='light coral')
        self.reset_button.grid(row=17, columnspan=4)
        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, bg='light coral')
        self.start_button.grid(row=18, columnspan=4)
        self.exit_button = tk.Button(self.master, text="Exit Game", command=self.master.destroy, bg='light coral')
        self.exit_button.grid(row=19, columnspan=4)

    def reset_game(self):
        self.board.reset_board()
        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    self.buttons[layer][row][col].config(text='')
        self.update_status()

    def start_game(self):
        self.reset_game()
        self.set_players("x")
        self.update_status()

    def get_best_move(self, max_time=2):
        best_move = None
        best_eval = -math.inf
        max_depth = 2
        start_time = time.time()

        while time.time() - start_time < max_time:
            available_moves = [
                (layer, row, col)
                for layer in range(4)
                for row in range(4)
                for col in range(4)
                if self.board.get_value(layer, row, col) == ''
            ]

            random.shuffle(available_moves)

            for move in available_moves:
                layer, row, col = move
                self.board.set_value(layer, row, col)

                # Check if the opponent is about to win, and block that move
                if self.board.is_win('x'):
                    eval = -100  # Heavily penalize blocking the opponent's win
                else:
                    eval = -self.board.minimax_with_heuristic(max_depth-1, False)

                self.board.undo_move(layer, row, col)

                if eval > best_eval:
                    best_eval = eval
                    best_move = move

            #max_depth += 1

        return best_move


    def make_move(self, layer, row, col):
        if self.board.get_value(layer, row, col) == '':
            self.board.set_value(layer, row, col)
            self.buttons[layer][row][col].config(text=self.board.current_player)
            self.board.turn()
            self.update_status()

            # Check for a win or draw after the human player's move
            if self.check_game_over():
                return

            # If it's the AI player's turn, let it make a move
            if self.board.current_player == self.board.AI_player:
                best_move = self.get_best_move()
                if best_move:
                    layer, row, col = best_move
                    self.board.set_value(layer, row, col)
                    self.buttons[layer][row][col].config(text=self.board.AI_player)
                    self.board.turn()
                    self.update_status()

                    # Check for a win or draw after the AI player's move
                    self.check_game_over()

    def check_game_over(self):
        if self.board.is_win('x') or self.board.is_win('O'):
            winner = 'Player X' if self.board.is_win('x') else 'Player O'
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.start_game()
            self.update_status()
            return True

        if self.board.is_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.board.reset_board()
            self.update_status()
            return True

        return False

    def update_status(self):
        self.status_label.config(text=f"Current Player: {self.board.current_player}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
