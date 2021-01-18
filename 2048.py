import tkinter as tk
import colors as c
import random

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048py - Developed By Faria Karim Porna")
        #border pixel = 3, height and width of the main frame
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width = 600, height = 600)
        #padding on the top
        self.main_grid.grid(pady = (100, 0))
        self.make_GUI()
        self.start_game()

        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()


    def make_GUI(self):
        #there are 4 rows and 4 columns in this game so i and j range is 4
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                #color, height and width of each cell
                cell_frame = tk.Frame(self.main_grid, bg=c.EMPTY_CELL_COLOR, width = 150, height = 150)
                #position of each cell, top bottom padding is pady, left right padding is padx
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                #cell value
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        # score header
        score_frame = tk.Frame(self)
        # position of score frame . relx = 0.5 means middle position in x axis
        score_frame.place(relx=0.5, y=45, anchor="center")
        # "Score" text will appeare in the 0th row of the score frame
        tk.Label(score_frame, text="Score", font=c.SCORE_LABEL_FONT).grid(row=0)
        # actual score will appeare in the 1st row of the score frame
        self.score_label = tk.Label(score_frame, text = "0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        # matrix of zeros
        self.matrix = [[0]*4 for _ in range(4)]
        # randomly select a position in row wise
        row = random.randint(0, 3)
        # randomly select a position in column wise
        col = random.randint(0,3)
        # game will start with a cell value of 2 at random position
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")
        # random position for second the 2 at random position
        while(self.matrix[row][col] != 0):
            # randomly select a position in row wise
            row = random.randint(0, 3)
            # randomly select a position in column wise
            col = random.randint(0,3)
            # game will start with a cell value of 2 at random position
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")
        self.score = 0

    # slide all the non-empty cells to the left
    def stack(self):
        # create new matrix with zeros of four rows and four columns
        new_matrix = [[0]*4 for _ in range(4)]
        
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    # first non-empty cell will move to the the 
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position = fill_position + 1
        print("stack new_matrix", new_matrix)
        self.matrix = new_matrix

    # combine two consecutive cells
    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]:
                    # after combining, one value will be doubled and the other will be empty. so 0.
                    self.matrix[i][j] = self.matrix[i][j]*2
                    self.matrix[i][j+1] = 0
                    self.score = self.score + self.matrix[i][j]
    # new_matrix will be the reverse of the actual matrix
    # left most value will be the right most value in new_matrix
    def reverse(self):
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 -j])
        print("reverse new_matrix", new_matrix)
        self.matrix = new_matrix

    # new_matrix will be the trabspose of the actual matrix
    # row will become column and column will become row
    def transpose(self):
        new_matrix = [[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j]= self.matrix[j][i]
        print("transpose new_matrix", new_matrix)
        self.matrix = new_matrix

    def add_new_tile(self):
        # randomly select a position in row wise
        row = random.randint(0, 3)
        # randomly select a position in column wise
        col = random.randint(0,3)
        
        while(self.matrix[row][col] != 0):
            # randomly select a position in row wise
            row = random.randint(0, 3)
            # randomly select a position in column wise
            col = random.randint(0,3)
            # new tile will contain any of two values 2 or 4
        self.matrix[row][col] = random.choice([2, 4])

    # GUI will be updated on each move
    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                # GUI for empty cells
                if cell_value == 0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                # GUI for other cells
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value], fg=c.CELL_NUMBER_COLORS[cell_value], font=c.CELL_NUMBER_FONTS[cell_value], text=str(cell_value))

        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self, event):
        self.stack()
        self.combine()
        
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
      
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    # if row wise consecutive valus are same return True otherwise return False
    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False

    # if column wise consecutive valus are same return True otherwise return False
    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def game_over(self):
        # if win
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="Hurray!! You WIN!", bg=c.WINNER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT).pack()
        # if lose
        # if no empty cell and no consecutive has same value
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(game_over_frame, text="Game Over :( ", bg=c.LOSER_BG, fg=c.GAME_OVER_FONT_COLOR, font=c.GAME_OVER_FONT).pack()


def main():
    Game()

if __name__ == "__main__":
    main()