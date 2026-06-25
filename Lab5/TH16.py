# TH16.py - Minimax Tic-Tac-Toe 4x4 (Player vs Player GUI)
from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Game XO 4x4')

clicked = True
count = 0

def disableButtons():
    for btn in [button1, button2, button3, button4, button5, button6, button7, button8,
                button9, button10, button11, button12, button13, button14, button15, button16]:
        btn.config(state=DISABLED)

def checkWinner():
    global winner
    winner = False
    # Check rows, columns, diagonals for X and O (simplified example; full logic in PDF)
    win_conditions = [
        # rows, columns, diagonals for 4x4 - extend as needed
    ]
    # (Full implementation would check all 4-in-a-row combinations)
    if winner:
        disableButtons()
        messagebox.showinfo("XO Game", "Player 1 wins!" if clicked else "Player 2 wins!")

def b_click(b):
    global clicked, count
    if b["text"] == " " and clicked:
        b["text"] = "X"
        clicked = False
        count += 1
        checkWinner()
    elif b["text"] == " ":
        b["text"] = "O"
        clicked = True
        count += 1
        checkWinner()
    if count == 16:
        messagebox.showinfo("XO Game", "It's a Tie!")

# Create buttons (4x4 grid)
buttons = []
for i in range(16):
    btn = Button(root, text=" ", font=("Helvetica", 20), height=2, width=5)
    btn.grid(row=i//4, column=i%4)
    buttons.append(btn)

# Assign to variables as in lab
button1, button2, ..., button16 = buttons

root.mainloop()