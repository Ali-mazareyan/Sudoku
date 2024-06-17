import tkinter as tk
from tkinter import messagebox

class Item:
    def __init__(self, value: int, domain: list = []) -> None:
        self.v = value
        self.d = domain
        self.neighbor = 0

    def range(self, n: int, m: list = []) -> None:
        self.d = [i for i in range(1, n + 1) if i not in m]

class Table:
    def __init__(self, table: list, n: int) -> None:
        self.t = table
        self.n = n
        self.counter = 0

    def MRV(self) -> tuple:
        queue = self.addQueue()
        queue.sort(key=lambda x: len(x[0].d), reverse=True)
        return queue.pop()

    def addQueue(self) -> list:
        table = self.t
        queue = [(table[i][j], i, j) for i in range(self.n) for j in range(self.n) if table[i][j].v == 0]
        return queue

    def degree(self) -> tuple:
        queue = self.addQueue()
        queue.sort(key=lambda x: x[0].neighbor)
        return queue.pop()

    def printTables(self) -> None:
        for row in self.t:
            for column in row:
                print(column.v, end=' ')
            print()

    def safe(self, row: int, column: int, choice: int) -> bool:
        table = self.t
        for i in range(self.n):
            if table[i][column].v == choice or table[row][i].v == choice:
                return False
        return True

    def domains(self, row: int, column: int) -> None:
        table = self.t
        tb = []
        for i in range(self.n):
            if table[i][column].v != 0:
                tb.append(table[i][column].v)
            elif table[row][i].v != 0:
                tb.append(table[row][i].v)
        table[row][column].range(self.n, tb)

    def freeItem(self) -> tuple:
        for i in range(self.n):
            for j in range(self.n):
                if self.t[i][j].v == 0:
                    return (i, j)
        return (self.n + 1, self.n + 1)

    def neighbor_Update(self, row: int, column: int) -> None:
        table = self.t
        counter = 0
        if row == 0:
            if table[row + 1][column].v == 0:
                counter += 1
            if column == 0:
                if table[row][column + 1].v == 0:
                    counter += 1
                if table[row + 1][column + 1].v == 0:
                    counter += 1
            elif column == self.n - 1:
                if table[row][column - 1].v == 0:
                    counter += 1
                if table[row + 1][column - 1].v == 0:
                    counter += 1
            else:
                if table[row + 1][column - 1].v == 0:
                    counter += 1
                if table[row + 1][column + 1].v == 0:
                    counter += 1
                if table[row][column - 1].v == 0:
                    counter += 1
                if table[row][column + 1].v == 0:
                    counter += 1
        elif row == self.n - 1:
            if table[row - 1][column].v == 0:
                counter += 1
            if column == self.n - 1:
                if table[row][column - 1].v == 0:
                    counter += 1
                if table[row - 1][column - 1].v == 0:
                    counter += 1
            elif column == 0:
                if table[row][column + 1].v == 0:
                    counter += 1
                if table[row - 1][column + 1].v == 0:
                    counter += 1
            else:
                if table[row - 1][column - 1].v == 0:
                    counter += 1
                if table[row - 1][column + 1].v == 0:
                    counter += 1
                if table[row][column - 1].v == 0:
                    counter += 1
                if table[row][column + 1].v == 0:
                    counter += 1
        elif column == 0:
            if table[row - 1][column].v == 0:
                counter += 1
            if table[row + 1][column].v == 0:
                counter += 1
            if table[row][column + 1].v == 0:
                counter += 1
            if table[row + 1][column + 1].v == 0:
                counter += 1
            if table[row - 1][column + 1].v == 0:
                counter += 1
        elif column == self.n - 1:
            if table[row - 1][column].v == 0:
                counter += 1
            if table[row + 1][column].v == 0:
                counter += 1
            if table[row][column - 1].v == 0:
                counter += 1
            if table[row + 1][column - 1].v == 0:
                counter += 1
            if table[row - 1][column - 1].v == 0:
                counter += 1
        else:
            if table[row - 1][column - 1].v == 0:
                counter += 1
            if table[row - 1][column].v == 0:
                counter += 1
            if table[row - 1][column + 1].v == 0:
                counter += 1
            if table[row][column - 1].v == 0:
                counter += 1
            if table[row][column + 1].v == 0:
                counter += 1
            if table[row + 1][column - 1].v == 0:
                counter += 1
            if table[row + 1][column].v == 0:
                counter += 1
            if table[row + 1][column + 1].v == 0:
                counter += 1

        table[row][column].neighbor = counter

    def updateAll(self) -> None:
        for row in range(self.n):
            for column in range(self.n):
                self.domains(row, column)
                self.neighbor_Update(row, column)

    def isSolved(self, Heuristic) -> bool:
        table = self.t
        self.counter += 1

        if self.freeItem() == (self.n + 1, self.n + 1):
            return True

        item = Heuristic()
        locat = (item[1], item[2])

        for i in item[0].d:
            if self.safe(locat[0], locat[1], i):
                table[locat[0]][locat[1]].v = i
                self.updateAll()
                if self.isSolved(Heuristic=self.MRV):
                    return True
                else:
                    table[locat[0]][locat[1]].v = 0
                    self.updateAll()

        return False

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")

        self.size_label = tk.Label(self.master, text="Enter the size of Sudoku:")
        self.size_label.pack(padx=10, pady=5)

        self.size_entry = tk.Entry(self.master, width=5, font=('Arial', 12))
        self.size_entry.pack(padx=10, pady=5)

        self.solve_button = tk.Button(self.master, text="Solve", command=self.create_grid)
        self.solve_button.pack(pady=10)

    def create_grid(self):
        size = self.size_entry.get().strip()  # Strip whitespace from the size input
        if size.isdigit() and int(size) > 0:
            size = int(size)
            self.size_label.pack_forget()  # Hide the size label and entry
            self.size_entry.pack_forget()
            self.solve_button.pack_forget()  # Hide the solve button

            entries_frame = tk.Frame(self.master)
            entries_frame.pack(padx=10, pady=5)

            entries = [[None for _ in range(size)] for _ in range(size)]
            for i in range(size):
                for j in range(size):
                    entry = tk.Entry(entries_frame, width=4, font=('Arial', 12))
                    entry.grid(row=i, column=j, padx=2, pady=2)
                    entries[i][j] = entry

            solve_button = tk.Button(self.master, text="Solve", command=lambda: self.solve_sudoku(entries, size))
            solve_button.pack(pady=10)
        else:
            print("Invalid size!")

    def solve_sudoku(self, entries, size):
        # Extract the values from the entries and create the Sudoku table
        table = [[Item(int(entries[i][j].get())) for j in range(size)] for i in range(size)]
        sudoku_table = Table(table, size)
        sudoku_table.updateAll()

        # Solve the Sudoku puzzle
        if sudoku_table.isSolved(sudoku_table.degree):
            messagebox.showinfo("Sudoku Solver", "Sudoku puzzle solved!")
            for i in range(size):
                for j in range(size):
                    entries[i][j].delete(0, tk.END)  # Clear the entry widget
                    entries[i][j].insert(0, sudoku_table.t[i][j].v)  # Insert the solved value
        else:
            messagebox.showinfo("Sudoku Solver", "Sudoku puzzle not solved!")

def main():
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()