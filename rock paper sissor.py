import tkinter as tk
import random

# Create main window
window = tk.Tk()
window.title("Rock Paper Scissors")
window.geometry("400x400")
window.config(bg="#1e1e1e")

# Game choices
choices = ["Rock", "Paper", "Scissors"]

# Function to play
def play(user_choice):
    comp_choice = random.choice(choices)
    if user_choice == comp_choice:
        result = "It's a tie!"
    elif (user_choice == "Rock" and comp_choice == "Scissors") or \
         (user_choice == "Paper" and comp_choice == "Rock") or \
         (user_choice == "Scissors" and comp_choice == "Paper"):
        result = "You win!"
    else:
        result = "Computer wins!"

    result_label.config(text=f"Computer chose: {comp_choice}\n{result}")

# Title
title_label = tk.Label(window, text="Rock Paper Scissors", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white")
title_label.pack(pady=20)

# Buttons for user choices
button_frame = tk.Frame(window, bg="#1e1e1e")
button_frame.pack(pady=20)

for choice in choices:
    btn = tk.Button(button_frame, text=choice, font=("Arial", 14), width=10,
                    command=lambda c=choice: play(c))
    btn.pack(pady=5)

# Result label
result_label = tk.Label(window, text="", font=("Arial", 14), bg="#1e1e1e", fg="lightgreen")
result_label.pack(pady=20)

# Run app
window.mainloop()
