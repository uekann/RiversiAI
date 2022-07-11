import tkinter as tk

from game import GameGUI
from riversi import Board

class RiversiGUI(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, width=800, height=800)
        self.master.title('Riversi')

        self.canvas = tk.Canvas(self, background="green")
        self.canvas.place(x=0, y=0, width=800, height=800)
        self.canvas.bind("<Button-1>", self.put)

        for x in range(100, 800, 100):
            self.canvas.create_line(x, 0, x, 800, fill="black")
        for y in range(100, 800, 100):
            self.canvas.create_line(0, y, 800, y, fill="black")
        
        self.game = GameGUI()

        self.update()
    
    def update(self) -> None:
        self.game.update()

        for i in range(8):
            for j in range(8):
                if not self.game.board.board[i, j] == Board.EMPTY:
                    x = i * 100 + 50
                    y = j * 100 + 50
                    self.canvas.create_oval(x-35, y-35, x+35, y+35, fill="black" if self.game.board.board[i, j] == Board.BLACK else "white")
        
        self.master.after(100, self.update)
    
    def put(self, event):
        x = event.x // 100
        y = event.y // 100
        self.game.put(x, y)



if __name__ == "__main__":
    app = RiversiGUI()
    app.pack()
    app.mainloop()