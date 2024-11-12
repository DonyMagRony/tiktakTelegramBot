import logging
import math
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from game import TicTacToe
import os
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)

API_TOKEN=str(os.getenv("API_TOKEN"))
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