from tkinter import Frame, Label, CENTER
import tkinter as tk
import game_ai
import game_functions
import colors_for_the_game as c
from time import sleep
import sys

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY = "'d'"
AI_KEY = "'q'"
AI_PLAY_KEY = "'p'"


class Display(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.score = 0
        self.master.title('Game: 2048')
        self.master.bind("<Key>", self.key_press)

        self.commands = \
            {
                UP_KEY: game_functions.move_up,
                DOWN_KEY: game_functions.move_down,
                LEFT_KEY: game_functions.move_left,
                RIGHT_KEY: game_functions.move_right,
                AI_KEY: game_ai.ai_move,  # signal move BOT
            }

        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()
        self.mainloop()

    def build_grid(self):
        background = Frame(
            self, bg=c.GRID_COLOR, bd=3, width=600, height=600
        )
        background.grid(pady=(100, 0))
        for row in range(4):
            grid_row = []
            for col in range(4):
                cell_frame = Frame(
                    background,
                    bg=c.EMPTY_CELL_COLOR,
                    width=200,  # 150
                    height=200  # 150
                )
                cell_frame.grid(
                    row=row, column=col, padx=5, pady=5
                )
                tk_label = Label(
                    master=cell_frame,
                    text="",
                    bg=c.EMPTY_CELL_COLOR,
                    justify=CENTER,
                    font=c.SCORE_FONT,
                    width=4,
                    height=2
                )
                tk_label.grid()
                grid_row.append(tk_label)
            self.grid_cells.append(grid_row)

        # make score_header
        score_frame = Frame()
        score_frame.place(relx=0.5, y=45, anchor="center")
        Label(
            score_frame,
            text="Your Score:",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        score_label = Label(score_frame, text="0", font=c.SCORE_FONT)
        score_label.grid(row=1)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()  # starting the matrix

    def draw_grid_cells(self):  # draw the matrix
        for row in range(4):
            for col in range(4):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="",
                        bg=c.EMPTY_CELL_COLOR
                    )
                else:
                    self.grid_cells[row][col].configure(
                        text=str(tile_value),
                        bg=c.CELL_COLORS[tile_value],
                        # fg=c.CELL_NUMBER_COLORS[tile_value]
                    )
        self.update_idletasks()

    def update_score(self, score_from_move):
        self.score += score_from_move
        score_frame = Frame()
        score_frame.place(relx=0.5, y=45, anchor="center")
        Label(
            score_frame,
            text="Your Score:",
            font=c.SCORE_LABEL_FONT
        ).grid(row=0)
        score_label = Label(score_frame, text=str(self.score), font=c.SCORE_FONT)
        score_label.grid(row=1)
        self.update_idletasks()

    def check_game_over(self, matrix):
        flag_for_ending_the_game = False
        if any(2048 in row for row in matrix):
            game_over_frame = Frame(self, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            Label(
                game_over_frame,
                text="YOU WIN!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()
            self.update_idletasks()
            flag_for_ending_the_game = True
        elif not any(0 in row for row in matrix) and not game_functions.horizontal_move_exists(
                matrix) and not game_functions.vertical_move_exists(matrix):
            game_over_frame = Frame(self, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            Label(
                game_over_frame,
                text="YOU LOSE!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT
            ).pack()
            self.update_idletasks()
            flag_for_ending_the_game = True
        return flag_for_ending_the_game

    def key_press(self, event):
        valid_game = True
        end_game = False
        key = repr(event.char)
        if key == AI_PLAY_KEY:
            move_count = 0
            while valid_game:
                self.matrix, valid_game, score = game_ai.ai_move(self.matrix, 20, 10)  # 40 30 (100,100)
                if valid_game:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                    self.update_score(score)
                    end_game = self.check_game_over(self.matrix)
                    if end_game:
                        sleep(3)
                        self.master.destroy()
                move_count += 1
        if key == AI_KEY:
            self.matrix, move_made, score = game_ai.ai_move(self.matrix, 40, 30)  # 20 30
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()
                self.update_score(score)
                end_game = self.check_game_over(self.matrix)
                if end_game:
                    sleep(3)
                    self.master.destroy()
                move_made = False

        elif key in self.commands:
            self.matrix, move_made, score = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()
                self.update_score(score)
                # now we going to check if there are valid moves to make
                end_game = self.check_game_over(self.matrix)
                if end_game:
                    sleep(3)
                    self.master.destroy()
                move_made = False


def main():
    while True:
        set_up_game = tk.Tk()
        set_up_game.geometry("750x650")
        set_up_game.configure(bg='gray97')
        set_up_game.title("Instructions for 2048 by Idan Ezer")
        len_label = tk.Label(text="Welcome to 2048 game by Idan Ezer", background="gray97", foreground="sandy brown",
                             font=("Roboto Light", 26, 'bold', 'underline', 'italic'))
        len_label.place(relx=.5, rely=.2, anchor="center")
        len_label_2 = tk.Label(text="Controls: Use the keys: 'w' (up), 'd' (right), 'a'(left), 's' (down) to move \n"
                                    "use Q to make one single move as a BOT,"
                                    "\n use P to play as a BOT for the entire game,\n"
                                    "the tiles merge into one when they touch,\n"
                                    " Add them up to reach 2048! "
                                    "\n" "You will lose if 2048 not in board and no valid moves exists \n"
                                    "\n" "Valid Moves are moves that you can make when the board is full or not.\n"
                                    "\n" "If the board is full and you can't merge tiles you lose.\n"
                                    "\n" "Winning will be when the the tile of 2048 on board.\n",
                               font=("Roboto Light", 15, 'bold'), background="gray97", foreground="sandy brown")
        len_label_2.place(relx=.5, rely=.5, anchor="center")
        gen_button = tk.Button(text="Time to Start", font=("Roboto Light", 16), width=16, height=4,
                               command=set_up_game.destroy)
        gen_button.place(relx=0.5, rely=0.8, anchor="center")
        set_up_game.mainloop()
        game_grid = Display()
        play_again = tk.Tk()
        play_again.geometry("850x450")
        play_again.configure(bg='gray97')
        play_again.title("Remote Control")
        play_again_label = tk.Label(text="Would you like to play again?",
                                    font=("Roboto Light", 20, 'bold'), background="gray97", foreground="orange")
        play_again_label.place(relx=.5, rely=.2, anchor="center", )
        yes_button = tk.Button(text="YES", font=("Roboto Light", 16), width=16, height=4, command=play_again.destroy)
        yes_button.place(relx=.25, rely=.55, anchor="center")
        no_button = tk.Button(text="NO", font=("Roboto Light", 16), width=16, height=4, command=sys.exit)
        no_button.place(relx=.75, rely=.55, anchor="center")
        play_again.mainloop()


if __name__ == '__main__':
    main()
