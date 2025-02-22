# gui.py

import tkinter as tk
from tkinter import messagebox
from reversi import Reversi, PLAYER, AI
from ai_player import AIPlayer


class ReversiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversi (Othello)")
        self.game = Reversi()
        self.ai_player = None
        self.current_player = None  # Ξεκινά ο χρήστης ή ο AI, ανάλογα με την επιλογή
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.setup_gui()
        self.start_game()

    def setup_gui(self):
        # Δημιουργία πλαισίου για τον πίνακα
        board_frame = tk.Frame(self.root)
        board_frame.pack()

        for x in range(8):
            for y in range(8):
                button = tk.Button(board_frame, text=' ', width=5, height=2,
                                   font=('Arial', 24, 'bold'),
                                   command=lambda x=x, y=y: self.on_cell_clicked(x, y))
                button.grid(row=x, column=y)
                self.buttons[x][y] = button

        # Πλαίσιο για τις ρυθμίσεις
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10)

        depth_label = tk.Label(settings_frame, text="Μέγιστο Βάθος Αναζήτησης:")
        depth_label.grid(row=0, column=0, padx=5)

        self.depth_var = tk.IntVar(value=3)
        depth_spinbox = tk.Spinbox(settings_frame, from_=1, to=6, textvariable=self.depth_var, width=5)
        depth_spinbox.grid(row=0, column=1, padx=5)

        first_label = tk.Label(settings_frame, text="Παίξε πρώτος:")
        first_label.grid(row=0, column=2, padx=5)

        self.first_var = tk.BooleanVar(value=True)
        first_check = tk.Checkbutton(settings_frame, variable=self.first_var, text="Ναι")
        first_check.grid(row=0, column=3, padx=5)

        start_button = tk.Button(settings_frame, text="Έναρξη Παιχνιδιού", command=self.start_game)
        start_button.grid(row=0, column=4, padx=5)

        # Πλαίσιο για το σκορ
        score_frame = tk.Frame(self.root)
        score_frame.pack(pady=10)

        self.score_label = tk.Label(score_frame, text="Score - X: 2  O: 2")
        self.score_label.pack()

    def start_game(self):
        # Ρύθμιση αρχικών παραμέτρων
        self.game = Reversi()
        self.ai_player = AIPlayer(depth=self.depth_var.get())
        self.current_player = PLAYER if self.first_var.get() else AI
        self.update_board()
        self.update_score()

        if self.current_player == AI:
            self.root.after(500, self.ai_move)  # Αναμονή πριν την κίνηση του AI

    def update_board(self):
        for x in range(8):
            for y in range(8):
                cell = self.game.board[x][y]
                if cell == PLAYER:
                    self.buttons[x][y].config(text='X', fg='black', bg='green')
                elif cell == AI:
                    self.buttons[x][y].config(text='O', fg='white', bg='green')
                else:
                    self.buttons[x][y].config(text=' ', bg='green')
        self.root.update_idletasks()

    def update_score(self):
        player_score = self.game.count(PLAYER)
        ai_score = self.game.count(AI)
        self.score_label.config(text=f"Score - X: {player_score}  O: {ai_score}")

    def on_cell_clicked(self, x, y):
        if self.current_player != PLAYER:
            return  # Δεν είναι η σειρά του χρήστη
        if (x, y) not in self.game.valid_moves(PLAYER):
            messagebox.showwarning("Μη Έγκυρη Κίνηση", "Αυτή η κίνηση δεν είναι έγκυρη.")
            return
        self.game.make_move(PLAYER, x, y)
        self.update_board()
        self.update_score()
        if self.game.is_game_over():
            self.end_game()
            return
        self.current_player = AI
        self.root.after(500, self.ai_move)  # Αναμονή πριν την κίνηση του AI

    def ai_move(self):
        if self.current_player != AI:
            return
        moves = self.game.valid_moves(AI)
        if moves:
            move = self.ai_player.get_move(self.game)
            if move:
                self.game.make_move(AI, move[0], move[1])
                self.update_board()
                self.update_score()
        else:
            messagebox.showinfo("Κίνηση AI", "Ο υπολογιστής δεν έχει διαθέσιμες κινήσεις.")
        if self.game.is_game_over():
            self.end_game()
            return
        self.current_player = PLAYER

    def end_game(self):
        player_score = self.game.count(PLAYER)
        ai_score = self.game.count(AI)
        if player_score > ai_score:
            result = "Συγχαρητήρια! Κερδίσατε!"
        elif player_score < ai_score:
            result = "Ο υπολογιστής κέρδισε."
        else:
            result = "Ισοπαλία!"
        messagebox.showinfo("Τερματισμός Παιχνιδιού",
                            f"Το παιχνίδι τελείωσε!\nΤελικό σκορ - X: {player_score}  O: {ai_score}\n{result}")
        self.start_game()  # Επανεκκίνηση παιχνιδιού
