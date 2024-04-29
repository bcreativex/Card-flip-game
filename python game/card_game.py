import tkinter as tk
from tkinter import ttk
import random

# List of card images (replace with your image paths)
card_images = [
    "D:/python game/dazai.png", "D:/python game/anyaa.png", "D:/python game/eren.png", "D:/python game/naruto.png",
    "D:/python game/dazai.png", "D:/python game/anyaa.png", "D:/python game/eren.png", "D:/python game/naruto.png",
    "D:/python game/nezuko.png", "D:/python game/nezuko.png", "D:/python game/levi.png", "D:/python game/shinchan.png",
    "D:/python game/mikey.png", "D:/python game/mikey.png", "D:/python game/levi.png", "D:/python game/shinchan.png"
]

random.shuffle(card_images)

class StartPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Card Game")

        self.start_frame = tk.Frame(root)
        self.start_frame.pack(fill=tk.BOTH, expand=True)

        # Set background image for the start page
        self.background_image = tk.PhotoImage(file="D:/python game/gamecover2.png")

        # Create a Label widget for the background image
        self.background_label = tk.Label(self.start_frame, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.start_label = ttk.Label(self.background_label,)
        self.start_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        style = ttk.Style()
        style.configure("Start.TButton", font=("Heather", 12), padding=20, relief=tk.RAISED, borderwidth=5, borderradius=20)  # Adjust padding to increase button size

        self.start_button = ttk.Button(self.background_label, text="Start Game", style="Start.TButton", command=self.start_game)
        self.start_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def start_game(self):
        # Remove the background image of the start page
        self.background_label.destroy()
        game = CardGame(self.root)

class CardGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Flip Game")

        # Set background image for the game window
        self.background_image = tk.PhotoImage(file="D:/python game/gamecover3.png")

        # Create a Label widget for the background image
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.game_frame = tk.Frame(root, background="#8BF3FF")
        self.game_frame.pack(expand=True, padx=20, pady=20)

        self.cards = []
        self.selected_cards = []
        self.matched_pairs = 0
        self.moves = 0

        style = ttk.Style()
        style.configure("Card.TButton", padding=10, font=("Helvetica", 12))

        style.configure("Win.TLabel", font=("Helvetica", 32), foreground="black")

        self.moves_label = ttk.Label(self.game_frame, text=f"Moves: {self.moves}", font=("Helvetica", 16))
        self.moves_label.grid(row=0, column=0, columnspan=4, pady=10)

        self.card_images = [tk.PhotoImage(file=image) for image in card_images]

        self.win_label = ttk.Label(self.root, text="You won!", style="Win.TLabel")
        self.win_label.grid_remove()  # Initially hide the label

        # Restart button
        self.restart_button = ttk.Button(self.root, text="Restart", style="Start.TButton", command=self.restart_game)
        self.restart_button.place(relx=0.85, rely=0.5, anchor=tk.CENTER)

        self.first_card_index = None

        self.setup_game_board()

    def setup_game_board(self):
        for i in range(4):
            for j in range(4):
                card = ttk.Button(self.game_frame, style="Card.TButton", image=back_image, command=lambda i=i, j=j: self.flip_card(i, j))
                card.grid(row=i + 1, column=j, padx=5, pady=5)
                self.cards.append(card)

    def flip_card(self, i, j):
        index = i * 4 + j
        if index not in self.selected_cards and len(self.selected_cards) < 2:
            card = self.cards[index]
            card.config(image=self.card_images[index])
            self.selected_cards.append((index, card))

            if len(self.selected_cards) == 2:
                self.root.after(1000, self.check_match)
                self.moves += 1
                self.moves_label.config(text=f"Moves: {self.moves}")

    def check_match(self):
        idx1, idx2 = self.selected_cards[0][0], self.selected_cards[1][0]
        card1, card2 = self.selected_cards[0][1], self.selected_cards[1][1]

        if card_images[idx1] != card_images[idx2]:
            card1.config(image=back_image)
            card2.config(image=back_image)
        else:
            self.matched_pairs += 1
            card1.config(state=tk.DISABLED)
            card2.config(state=tk.DISABLED)

        self.selected_cards.clear()

        if self.matched_pairs == len(card_images) // 2:
            self.show_win_message()

    def show_win_message(self):
        if self.matched_pairs == len(card_images) // 2:
            # Place the label at the center of the game frame
            self.win_label.place(relx=0.5, rely=0.5, anchor="center")
    
    def restart_game(self):
        # Clear the game board and restart
        for card in self.cards:
            card.config(image=back_image, state=tk.NORMAL)
        self.moves = 0
        self.matched_pairs = 0
        self.moves_label.config(text=f"Moves: {self.moves}")

        # Hide the "You won!" label using grid_remove
        self.win_label.place_forget()

        # Shuffle card images again
        random.shuffle(card_images)
        self.card_images = [tk.PhotoImage(file=image) for image in card_images]

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")

    back_image = tk.PhotoImage(file="D:/python game/cover.png")
    start_page = StartPage(root)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 500
    window_height = 600
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.mainloop()
