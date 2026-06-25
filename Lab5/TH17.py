from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('Game XO 5x5')

clicked = True
count = 0
board = [[' ' for _ in range(5)] for _ in range(5)]  # Bảng 5x5

def disableButtons():
    for btn in buttons:
        btn.config(state=DISABLED)

def checkWinner(player):
    # Kiểm tra hàng, cột, đường chéo
    for i in range(5):
        # Hàng
        if all(board[i][j] == player for j in range(5)):
            return True
        # Cột
        if all(board[j][i] == player for j in range(5)):
            return True
    # Đường chéo chính
    if all(board[i][i] == player for i in range(5)):
        return True
    # Đường chéo phụ
    if all(board[i][4-i] == player for i in range(5)):
        return True
    return False

def checkDraw():
    return count == 25

def buttonClicked(btn, row, col):
    global clicked, count
    if board[row][col] == ' ':
        if clicked:
            btn["text"] = "X"
            board[row][col] = "X"
            player = "X"
        else:
            btn["text"] = "O"
            board[row][col] = "O"
            player = "O"
        
        clicked = not clicked
        count += 1
        
        if checkWinner(player):
            disableButtons()
            messagebox.showinfo("OX Game", f"Player {'1 (X)' if player=='X' else '2 (O)'} WINNER!!")
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
    board = [[' ' for _ in range(5)] for _ in range(5)]
    for btn in buttons:
        btn.config(text=" ", state=NORMAL, bg="SystemButtonFace")

# Tạo 25 button
buttons = []
for i in range(5):
    for j in range(5):
        btn = Button(root, text=" ", font=("Helvetica", 16), height=2, width=5,
                     command=lambda r=i, c=j: buttonClicked(buttons[r*5 + c], r, c))
        btn.grid(row=i, column=j)
        buttons.append(btn)

# Menu
menubar = Menu(root)
root.config(menu=menubar)
options = Menu(menubar, tearoff=False)
menubar.add_cascade(label="Options", menu=options)
options.add_command(label="New Game", command=start)

start()
root.mainloop()