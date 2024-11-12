import math

# Your TicTacToe class
class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9

    def reset_board(self):
        self.board = [' '] * 9

    def make_move(self, row, col, player):
        if self.board[row * 3 + col] == ' ':
            self.board[row * 3 + col] = player
            return True
        return False

    def is_board_full(self):
        return ' ' not in self.board

    def check_winner(self):
        # Define a function to check if all symbols in a line are the same and non-empty
        def is_winning_line(a, b, c):
            return self.board[a] == self.board[b] == self.board[c] != ' '
        
        # Check rows, columns, and diagonals for a winner
        for start in range(0, 9, 3):  # Rows
            if is_winning_line(start, start + 1, start + 2):
                return self.board[start]
        
        for start in range(3):  # Columns
            if is_winning_line(start, start + 3, start + 6):
                return self.board[start]
        
        # Diagonals
        if is_winning_line(0, 4, 8):
            return self.board[0]
        if is_winning_line(2, 4, 6):
            return self.board[2]
    
        return None
    def get_best_move(self):
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                if self.check_winner() == 'O':
                    return (i // 3, i % 3)
                self.board[i] = ' '
                
                self.board[i] = 'X'
                if self.check_winner() == 'X':
                    self.board[i] = 'O'
                    return (i // 3, i % 3)
                self.board[i] = ' '

        best_score = -math.inf
        best_move = None
        for i in [4, 0, 2, 6, 8, 1, 3, 5, 7]:  
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(False, -math.inf, math.inf)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i // 3, i % 3)
        return best_move

    def minimax(self, is_maximizing, alpha=-math.inf, beta=math.inf):
        winner = self.check_winner()
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'O'
                    score = self.minimax(False, alpha, beta)
                    self.board[i] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break 
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = 'X'
                    score = self.minimax(True, alpha, beta)
                    self.board[i] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break 
            return best_score