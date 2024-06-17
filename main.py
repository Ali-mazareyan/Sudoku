class Item:
    def __init__(self, value: int, domain: list = []) -> None:
        self.v = value
        self.d = domain
        self.neighbor = 0

    def range(self, n: int, m: list = [0]) -> None:
        self.d = [i for i in range(1, n+1) if i not in m]


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
        queue = [(table[i][j], i, j) for i in range(self.n)
                 for j in range(self.n) if table[i][j].v == 0]
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
            if  table[i][column].v == choice or table[row][i].v == choice:
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
        return(self.n+1, self.n+1)

    def neighbor_Update(self, row: int, column: int) -> None:
        table = self.t
        counter = 0
        if row == 0:
            if table[row+1][column].v == 0:
                counter += 1
            if column == 0:
                if table[row][column+1].v == 0:
                    counter += 1
                if table[row+1][column+1].v == 0:
                    counter += 1
            elif column == self.n-1:
                if table[row][column-1].v == 0:
                    counter += 1
                if table[row+1][column-1].v == 0:
                    counter += 1
            else:
                if table[row+1][column-1].v == 0:
                    counter += 1
                if table[row+1][column+1].v == 0:
                    counter += 1
                if table[row][column-1].v == 0:
                    counter += 1
                if table[row][column+1].v == 0:
                    counter += 1
        elif row == self.n-1:
            if table[row-1][column].v == 0:
                counter += 1
            if column == self.n-1:
                if table[row][column-1].v == 0:
                    counter += 1
                if table[row-1][column-1].v == 0:
                    counter += 1
            elif column == 0:
                if table[row][column+1].v == 0:
                    counter += 1
                if table[row-1][column+1].v == 0:
                    counter += 1
            else:
                if table[row-1][column-1].v == 0:
                    counter += 1
                if table[row-1][column+1].v == 0:
                    counter += 1
                if table[row][column-1].v == 0:
                    counter += 1
                if table[row][column+1].v == 0:
                    counter += 1
        elif column == 0:
            if table[row-1][column].v == 0:
                counter += 1
            if table[row+1][column].v == 0:
                counter += 1
            if table[row][column+1].v == 0:
                counter += 1
            if table[row+1][column+1].v == 0:
                counter += 1
            if table[row-1][column+1].v == 0:
                counter += 1
        elif column == self.n-1:
            if table[row-1][column].v == 0:
                counter += 1
            if table[row+1][column].v == 0:
                counter += 1
            if table[row][column-1].v == 0:
                counter += 1
            if table[row+1][column-1].v == 0:
                counter += 1
            if table[row-1][column-1].v == 0:
                counter += 1
        else:
            if table[row-1][column-1].v == 0:
                counter += 1
            if table[row-1][column].v == 0:
                counter += 1
            if table[row-1][column+1].v == 0:
                counter += 1
            if table[row][column-1].v == 0:
                counter += 1
            if table[row][column+1].v == 0:
                counter += 1
            if table[row+1][column-1].v == 0:
                counter += 1
            if table[row+1][column].v == 0:
                counter += 1
            if table[row+1][column+1].v == 0:
                counter += 1

        table[row][column].neighbor = counter

    def updateAll(self) -> None:
        for row in range(self.n):
            for column in range(self.n):
                self.domains(row, column)
                self.neighbor_Update(row, column)


    def isSolved(self, Heurestic) -> bool:
        table = self.t
        self.counter = self.counter + 1

        if self.freeItem() == (self.n+1, self.n+1):
            return True

        item = Heurestic()
        locat = (item[1], item[2])

        for i in item[0].d: 
            if self.safe(locat[0], locat[1], i):
                table[locat[0]][locat[1]].v = i
                self.updateAll()
                if self.isSolved(Heurestic = self.MRV):
                    return True
                else:
                    table[locat[0]][locat[1]].v = 0
                    self.updateAll()

        return False


def main() -> None:
    number = int(input())
    array = [[0 for _ in range(number)]for _ in range(number)]
    for i in range(number):
        print("row " , i+1)
        inp = list(map(int, input().split()))
        for j in range(number):
            item = Item(inp[j])
            if inp[j] == 0:
                item.range(number)
            array[i][j] = item

    table = Table(array, number)
    table.updateAll()
    if table.isSolved(table.degree):
        print('_____________________')
        print('Solved')
        table.printTables()
        print(table.counter)
    else:
        print('_____________________')
        print('Not Solved!')
        table.printTables()
        print(table.counter)
        


if __name__ == '__main__':
    main()
