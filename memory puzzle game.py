import tkinter as tk
import random
import time

# Create a game window
root = tk.Tk()
root.title("Memory Puzzle Game")

# Setup game variables
rows, cols = 4, 4
time_limit = 60  # Time limit in seconds
cards = list(range(1, ((rows * cols) // 2) + 1)) * 2
random.shuffle(cards)
cards = [cards[i:i + cols] for i in range(0, len(cards), cols)]
hidden_cards = [["" for _ in range(cols)] for _ in range(rows)]

selected = []
matches = 0
start_time = time.time()

# Handle clicks
def handle_click(row, col):
    global selected, matches
    if hidden_cards[row][col] or len(selected) == 2:
        return

    hidden_cards[row][col] = cards[row][col]
    selected.append((row, col))
    update_display()

    if len(selected) == 2:
        root.after(1000, check_match)

# Check matches
def check_match():
    global selected, matches
    r1, c1 = selected[0]
    r2, c2 = selected[1]
    if cards[r1][c1] != cards[r2][c2]:
        hidden_cards[r1][c1] = ""
        hidden_cards[r2][c2] = ""
    else:
        matches += 1
    selected = []
    update_display()
    check_win()

# Update display
def update_display():
    for row in range(rows):
        for col in range(cols):
            button_text = hidden_cards[row][col] if hidden_cards[row][col] else ""
            buttons[row][col].config(text=button_text)

# Check win condition
def check_win():
    if matches == (rows * cols) // 2:
        elapsed_time = time.time() - start_time
        tk.Label(root, text=f"Congratulations! You won in {elapsed_time:.2f} seconds!").grid(row=rows, columnspan=cols)

# Create buttons
buttons = []
for r in range(rows):
    button_row = []
    for c in range(cols):
        button = tk.Button(root, text="", width=5, height=3, command=lambda row=r, col=c: handle_click(row, col))
        button.grid(row=r, column=c)
        button_row.append(button)
    buttons.append(button_row)

# Timer
def update_timer():
    elapsed_time = time.time() - start_time
    if elapsed_time >= time_limit:
        tk.Label(root, text="Time's up! You lost!").grid(row=rows, columnspan=cols)
        return
    timer_label.config(text=f"Time left: {time_limit - int(elapsed_time)}s")
    root.after(1000, update_timer)

timer_label = tk.Label(root, text=f"Time left: {time_limit}s")
timer_label.grid(row=rows, columnspan=cols)
update_timer()

# Start the game
root.mainloop()