from tkinter import *
from tkinter import messagebox


class TicTacToe:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tic Tac Toe vs AI")

        self.buttons = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]]
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.game_over = False

        # Creating main frame
        self.main_frame = Frame(self.root)
        self.main_frame.pack(pady=10)

        # Creating the game board GUI
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = Button(
                    self.main_frame,
                    font=('Verdana', 56),
                    width=3,
                    bg='gray',
                    command=lambda r=i, c=j: self.human_move(r, c)
                )
                self.buttons[i][j].grid(row=i, column=j)

        # Control frame for buttons
        self.control_frame = Frame(self.root)
        self.control_frame.pack(pady=10)

        # Reset button
        self.reset_button = Button(
            self.control_frame,
            text="Reset Game",
            font=('Verdana', 12),
            command=self.reset_game
        )
        self.reset_button.pack(side=LEFT, padx=5)

        # Quit button
        self.quit_button = Button(
            self.control_frame,
            text="Quit Game",
            font=('Verdana', 12),
            command=self.quit_game
        )
        self.quit_button.pack(side=LEFT, padx=5)

        # Bind 'q' key and Return key to quit_game
        self.root.bind('q', lambda event: self.quit_game())
        self.root.bind('<Return>', lambda event: self.quit_game())

    def human_move(self, row, col):
        if self.board[row][col] == 0 and not self.game_over:
            self.make_move(row, col, 'X')
            if not self.check_game_status():
                self.ai_move()
                self.check_game_status()

    def ai_move(self):
        best_score = -float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = 'O'
                    score = self.minimax(self.board, 0, False, -float('inf'), float('inf'))
                    self.board[i][j] = 0

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.make_move(best_move[0], best_move[1], 'O')

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_winner(board, 'O'):
            return 1
        if self.check_winner(board, 'X'):
            return -1
        if self.is_board_full(board):
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 'O'
                        eval = self.minimax(board, depth + 1, False, alpha, beta)
                        board[i][j] = 0
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 'X'
                        eval = self.minimax(board, depth + 1, True, alpha, beta)
                        board[i][j] = 0
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].configure(
            text=player,
            fg='blue' if player == 'X' else 'orange',
            bg='white' if player == 'X' else 'black'
        )

    def check_winner(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
                    all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)) or \
                all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_board_full(self, board):
        return all(all(cell != 0 for cell in row) for row in board)

    def check_game_status(self):
        if self.check_winner(self.board, 'X'):
            self.highlight_winner()
            self.game_over = True
            messagebox.showinfo("Game Over", "You Won!")
            return True
        elif self.check_winner(self.board, 'O'):
            self.highlight_winner()
            self.game_over = True
            messagebox.showinfo("Game Over", "AI Wins!")
            return True
        elif self.is_board_full(self.board):
            self.game_over = True
            messagebox.showinfo("Game Over", "Draw!")
            return True
        return False

    def highlight_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                for j in range(3):
                    self.buttons[i][j].configure(bg='grey')
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                for j in range(3):
                    self.buttons[j][i].configure(bg='grey')

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            for i in range(3):
                self.buttons[i][i].configure(bg='grey')
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            for i in range(3):
                self.buttons[i][2 - i].configure(bg='grey')

    def reset_game(self):
        self.board = [[0, 0, 0] for _ in range(3)]
        self.game_over = False
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text='', bg='gray')

    def quit_game(self):
        if messagebox.askokcancel("Quit Game", "Are you sure you want to quit?"):
            self.root.quit()
            self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = TicTacToe()
    game.run()