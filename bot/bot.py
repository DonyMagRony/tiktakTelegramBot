import logging
import math
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor

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
        # Winning positions
        winning_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for positions in winning_positions:
            if self.board[positions[0]] == self.board[positions[1]] == self.board[positions[2]] != ' ':
                return True
        return False

    def get_best_move(self):
        # Check for winning move or blocking the opponent
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                if self.check_winner():
                    return (i // 3, i % 3)
                self.board[i] = ' '
                
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'X'
                if self.check_winner():
                    self.board[i] = 'O'
                    return (i // 3, i % 3)
                self.board[i] = ' '
        
        # If no immediate winning or blocking move, use minimax
        best_score = -math.inf
        best_move = None
        prioritized_moves = [4] + [0, 2, 6, 8] + [1, 3, 5, 7]
        for i in prioritized_moves:
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i // 3, i % 3)
        return best_move

    def minimax(self, is_maximizing, alpha=-math.inf, beta=math.inf):
        if self.check_winner():
            return 1 if is_maximizing else -1
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

# API token and bot setup
API_TOKEN = '7404123683:AAGegzbwo7ak_Yp73OpmqI-XZ_dITFndd1M'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Initialize game instance
game = TicTacToe()

# Button grid for Tic-Tac-Toe
def generate_board_markup(board):
    markup = InlineKeyboardMarkup(row_width=3)
    for i, cell in enumerate(board):
        row, col = divmod(i, 3)
        button_text = '❌' if cell == 'X' else '⭕' if cell == 'O' else f" "
        markup.insert(InlineKeyboardButton(button_text, callback_data=f"move_{i}"))
    return markup

# Status message for the game
async def send_game_status(message, status):
    await message.answer(status)

# Start a new game
@dp.message_handler(commands=['start', 'newgame'])
async def start_game(message: types.Message):
    game.reset_board()
    await message.answer("Game started! You are X. Make your move by tapping a cell.", reply_markup=generate_board_markup(game.board))

# Handle player move
@dp.callback_query_handler(lambda c: c.data.startswith('move_'))
async def handle_move(callback_query: types.CallbackQuery):
    move_index = int(callback_query.data.split('_')[1])
    player_row, player_col = divmod(move_index, 3)
    
    # Make player's move
    if game.make_move(player_row, player_col, 'X'):
        # Check for win or draw
        if game.check_winner():
            await bot.send_message(callback_query.from_user.id, "Congratulations! You won! 🎉", parse_mode="Markdown")
            game.reset_board()
            await bot.send_message(callback_query.from_user.id, "Start a new game by typing /newgame", reply_markup=generate_board_markup(game.board))
        elif game.is_board_full():
            await bot.send_message(callback_query.from_user.id, "It's a draw! 🤝")
            game.reset_board()
            await bot.send_message(callback_query.from_user.id, "Start a new game by typing /newgame", reply_markup=generate_board_markup(game.board))
        else:
            # Bot's turn
            await asyncio.sleep(1)  # Delay for bot to 'think'
            bot_move = game.get_best_move()
            game.make_move(bot_move[0], bot_move[1], 'O')
            if game.check_winner():
                await bot.send_message(callback_query.from_user.id, "You lost! The bot wins. 😢")
                game.reset_board()
                await bot.send_message(callback_query.from_user.id, "Start a new game by typing /newgame", reply_markup=generate_board_markup(game.board))
            elif game.is_board_full():
                await bot.send_message(callback_query.from_user.id, "It's a draw! 🤝")
                game.reset_board()
                await bot.send_message(callback_query.from_user.id, "Start a new game by typing /newgame", reply_markup=generate_board_markup(game.board))
        
        # Check if the new markup is different before sending
        new_markup = generate_board_markup(game.board)
        if new_markup != callback_query.message.reply_markup:
            await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=new_markup)

    await callback_query.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)