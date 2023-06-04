import tkinter as tk


class GameBoard(tk.Frame):
    def __init__(self):
        title = tk.Label(text="Hello World")
        title.place(x=0, y=0)


if (__name__ == "__main__"):
    root = tk.Tk()
    root.title("안녕")
    root.geometry("400x400+0+0")

    frame = GameBoard()
    root.mainloop()
