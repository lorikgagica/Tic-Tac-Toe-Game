import tkinter as tk
from tkinter import messagebox

# (Optional, but commented for portability)
# import winsound

BOARD_SIZE = 3

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0
        self.buttons = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.init_ui()

    def init_ui(self):
        self.root.title("Tic-Tac-Toe")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f8ff")

        # Scoreboard
        self.score_label = tk.Label(self.root, text=self.get_score_text(), font=("Arial", 13),
                                    bg="#e4f1fe", fg="#222")
        self.score_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 4))

        self.turn_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn",
                                   font=("Arial", 18), bg="#e4f1fe")
        self.turn_label.grid(row=1, column=0, columnspan=3, pady=6)

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = tk.Button(self.root, text="", font=("Arial", 28, "bold"),
                                width=5, height=2,
                                command=lambda row=r, col=c: self.onclick(row, col),
                                bg="#dff9fb", fg="#30336b")
                btn.grid(row=r+2, column=c, padx=6, pady=6)
                self.buttons[r][c] = btn

        self.reset_button = tk.Button(self.root, text="Reset", font=("Arial", 14),
                                      command=self.reset_game, bg="#f6e58d")
        self.reset_button.grid(row=6, column=0, columnspan=3, sticky="ew", pady=10)

    def get_score_text(self):
        return f"X Wins: {self.x_wins}   O Wins: {self.o_wins}   Draws: {self.draws}"

    def reset_game(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                btn = self.buttons[r][c]
                btn.config(text="", state="normal", bg="#dff9fb")
        # winsound.Beep(400, 140)  # optional sound on reset

    def onclick(self, row, col):
        btn = self.buttons[row][col]
        if btn['text'] == "":
            btn.config(text=self.current_player,
                       fg="#e17055" if self.current_player == 'X' else "#00b894")
            self.board[row][col] = self.current_player
            # winsound.Beep(700 if self.current_player=='X' else 400, 80)  # optional
            winner, win_coords = self.check_winner()
            if winner:
                self.score_update(winner)
                self.show_win(win_coords)
                self.turn_label.config(text=f"Player {winner} Wins!")
                self.score_label.config(text=self.get_score_text())
                self.disable_buttons()
                self.ask_restart(f"Player {winner} Wins! Play again?")
            elif self.is_draw():
                self.draws += 1
                self.turn_label.config(text="It's a Draw!")
                self.score_label.config(text=self.get_score_text())
                self.ask_restart("It's a Draw! Play again?")
                # winsound.Beep(300, 300)
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.turn_label.config(text=f"Player {self.current_player}'s Turn")

    def score_update(self, winner):
        if winner == 'X':
            self.x_wins += 1
        elif winner == 'O':
            self.o_wins += 1

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def show_win(self, win_coords):
        for r, c in win_coords:
            self.buttons[r][c].config(bg="#00b894" if self.board[r][c] == "O" else "#e17055")

    def ask_restart(self, msg):
        ans = messagebox.askyesno("Game Over", msg)
        if ans:
            self.reset_game()
        else:
            self.root.quit()

    def check_winner(self):
        # check rows/cols
        for r in range(BOARD_SIZE):
            if self.board[r][0] != "" and all(self.board[r][c] == self.board[r][0] for c in range(BOARD_SIZE)):
                return self.board[r][0], [(r, c) for c in range(BOARD_SIZE)]
        for c in range(BOARD_SIZE):
            if self.board[0][c] != "" and all(self.board[r][c] == self.board[0][c] for r in range(BOARD_SIZE)):
                return self.board[0][c], [(r, c) for r in range(BOARD_SIZE)]
        # diagonals
        if self.board[0][0] != "" and all(self.board[i][i] == self.board[0][0] for i in range(BOARD_SIZE)):
            return self.board[0][0], [(i, i) for i in range(BOARD_SIZE)]
        if self.board[0][BOARD_SIZE-1] != "" and all(self.board[i][BOARD_SIZE-1-i] == self.board[0][BOARD_SIZE-1] for i in range(BOARD_SIZE)):
            return self.board[0][BOARD_SIZE-1], [(i, BOARD_SIZE-1-i) for i in range(BOARD_SIZE)]
        return None, None

    def is_draw(self):
        return all(self.board[r][c] != "" for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)) and not self.check_winner()[0]

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()