# Tic-Tac-Toe Telegram Bot

This project is a Telegram bot that lets users play a game of Tic-Tac-Toe against an AI bot directly within a Telegram chat. The bot is built with Python, using the `aiogram` library for bot interactions and `python-dotenv` for environment variable management.

## Features

- Play Tic-Tac-Toe with an intelligent AI opponent.
- The AI uses the Minimax algorithm with alpha-beta pruning to make the best possible moves.
- Start a new game with `/start` or `/newgame`.
- Easy-to-use interface with inline keyboard buttons for each move.

## Requirements

- Python 3.7+
- Telegram Bot API token (from [BotFather](https://core.telegram.org/bots#botfather) on Telegram)

## Technologies Used

- **Python**: Core programming language.
- **aiogram**: Telegram bot framework for asynchronous interaction.
- **python-dotenv**: For managing environment variables.
- **TicTacToe Game Logic**: Custom implementation of Tic-Tac-Toe, including an AI using Minimax.

## Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/tic-tac-toe-bot.git
    cd tic-tac-toe-bot
    ```

2. **Install Dependencies**

    Make sure you have `pip` installed. Then, run:

    ```bash
    pip install -r requirements.txt
    ```

3. **Create `.env` File**

    In the root directory, create a `.env` file with your Telegram Bot API token:

    ```plaintext
    API_TOKEN=your_telegram_bot_token
    ```

4. **Run the Bot**

    Start the bot with the following command:

    ```bash
    python bot.py
    ```

## Usage

- **Start a Game**: Send `/start` or `/newgame` to the bot to begin a new game.
- **Make a Move**: Tap on an empty cell in the inline keyboard to make a move as "X". The bot will respond with its move as "O".
- **Win/Loss/Draw**: The bot will notify you if you've won, lost, or if the game ends in a draw.

## File Structure

- `bot.py`: Main bot code with the game logic and AI logic.
- `game.py`: Contains the `TicTacToe` class implementing the game logic and AI.
- `.env`: Contains your `API_TOKEN` for the bot.
- `requirements.txt`: Lists the Python dependencies.

## Tic-Tac-Toe Game Logic

The game is implemented in the `TicTacToe` class, with an AI that uses the Minimax algorithm to make optimal moves. The bot prioritizes moves in the center, corners, and sides to enhance its chances of winning.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for improvements or bug fixes.

## Credits

This bot was created using `aiogram` for asynchronous Telegram interactions and `python-dotenv` for secure API token management.
