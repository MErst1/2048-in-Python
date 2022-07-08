import tkinter as tk
from tkinter import ttk
from random import randrange

BOARDSIZE = 4

class GameBoard:
    def __init__(self, size: int):
        self.board = [[0 for x in range(size)] for y in range(size)]
        self.boardsize = size


    def rnd_element(self) -> int:
        return randrange(self.boardsize)

    def set_two(self):
        y,x = self.rnd_element(), self.rnd_element()
        if self.board[y][x]:
            self.set_two()
        else:
            self.board[y][x] = 2

    def rotate_board(self, count: int = 1):
        for _ in range(count):
            self.board = list(map(list,zip(*self.board[::-1])))
            
    def move_zero(self,row):
        move = True
        change = False
        while move:
            move = False
            for x in range(self.boardsize-1):
                if not row[x] and row[x+1]:
                    row[x] = row[x+1]
                    row[x+1] = 0
                    move = True
                    change = True  
        if change:       
            return change

    def move(self):
        change = False
        for row in self.board:
            for x in range(self.boardsize-1):
                if self.move_zero(row):
                    change = True
                if row[x] and row[x] == row[x+1]:
                    row[x] = 2*row[x+1]
                    row[x+1] = 0
                    change = True
        return change

                    

    def move_direction(self, direction: str):
        if direction == "l":
            change = self.move()
        elif direction == "d":
            self.rotate_board(count=1)
            change = self.move()
            self.rotate_board(count=3)
        elif direction == "r":
            self.rotate_board(count=2)
            change = self.move()
            self.rotate_board(count=2)
        elif direction == "u":
            self.rotate_board(count=3)
            change = self.move()
            self.rotate_board(count=1)
        return change

    def print_board(self):
        for i in self.board:
            print(i)


def update_win(obj):
    for y in range(BOARDSIZE):
        for x in range(BOARDSIZE):
            value = obj.board[y][x]
            labels[y][x]["textvar"].set(str(value))
            labels[y][x]["frame"]["style"] = "{}.TFrame".format(value)
            labels[y][x]["label"]["style"] = "{}.TLabel".format(value)
            if not value:
                labels[y][x]["label"].place_forget()
            else:
                labels[y][x]["label"].place(relx=.5, rely=.5, anchor="center")


def game_step(obj, direction: str):
    change = obj.move_direction(direction)
    if change:
        obj.set_two()
    update_win(obj)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("2048")
    root.geometry("400x400")
    root.resizable(width=False, height=False)
    win = ttk.Frame(root)

    style = ttk.Style()
    style_dict = {0: '#CDC0B4', 2: '#EEE4DA', 4: '#EDE0C8', 8: '#EDE0C8', 16: '#F59563',
          32: '#F67C60', 64: '#F65E3B', 128: '#EDCF73', 256: '#EDCC62',
          512: '#EDC850', 1024: '#EDC850', 2048: '#EDC22D', 4096: '#000000', 8192: '#000000'}
    for i in range(12):
        s = 2**i if i else 0
        style.configure("{}.TFrame".format(s),background=style_dict[s])
        style.configure("{}.TLabel".format(s), background = style_dict.get(s),forground="black",
            font="Arial 15 bold")


    board = GameBoard(BOARDSIZE)
    
    labels = []
    for y in range(BOARDSIZE):
        labels.append([])
        for x in range(BOARDSIZE):
            dic = dict()
            dic["frame"] = ttk.Frame(win, borderwidth=5, relief="solid", height=100, width=100)
            dic["frame"].grid_propagate(False)
            dic["frame"].grid(column=x, row=y)
            dic["textvar"] = tk.StringVar()
            dic["label"] = ttk.Label(dic["frame"], textvar = dic["textvar"])
            dic["label"].place(relx=.5, rely=.5, anchor="center")
            labels[y].append(dic)


    root.bind("<Right>", lambda x: game_step(board, direction="r"))
    root.bind("<Left>", lambda x: game_step(board, direction="l"))
    root.bind("<Up>", lambda x: game_step(board, direction="u"))
    root.bind("<Down>", lambda x: game_step(board, direction="d"))


    win.grid()
    board.set_two()
    update_win(board)
    tk.mainloop()
