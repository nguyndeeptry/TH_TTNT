from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Game XO 8x8')

clicked = True
count = 0
size = 8
board = [[' ' for _ in range(size)] for _ in range(size)]

def disableButtons():
    for btn in buttons:
        btn.config(state=DISABLED)

def checkWinner(player):
    for i in range(size):
        if all(board[i][j] == player for j in range(size)) or \
           all(board[j][i] == player for j in range(size)):
            return True
    if all(board[i][i] == player for i in range(size)) or \
       all(board[i][size-1-i] == player for i in range(size)):
        return True
    return False

def checkDraw():
    return count == size * size

def buttonClicked(btn, row, col):
    global clicked, count
    if board[row][col] == ' ':
        mark = "X" if clicked else "O"
        btn["text"] = mark
        board[row][col] = mark
        clicked = not clicked
        count += 1
        
        if checkWinner(mark):
            disableButtons()
            messagebox.showinfo("OX Game", f"Player {'1 (X)' if mark=='X' else '2 (O)'} WINNER!!")
            return
        if checkDraw():
            disableButtons()
            messagebox.showinfo("OX Game", "DRAW!!")
    else:
        messagebox.showerror("OX Game", "Ô này đã được chọn!")

def start():
    global clicked, count, board
    clicked = True
    count = 0
    board = [[' ' for _ in range(size)] for _ in range(size)]
    for btn in buttons:
        btn.config(text=" ", state=NORMAL, bg="SystemButtonFace")

buttons = []
for i in range(size):
    for j in range(size):
        btn = Button(root, text=" ", font=("Helvetica", 12), height=2, width=4,
                     command=lambda r=i, c=j: buttonClicked(buttons[r*size + c], r, c))
        btn.grid(row=i, column=j)
        buttons.append(btn)

menubar = Menu(root)
root.config(menu=menubar)
options = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Options", menu=options)
options.add_command(label="New Game", command=start)

start()
root.mainloop()