# Programing Task 1 Solution by B23-DSAI-03 students
# Kirill Greshnov
# Danil Valiev
# Ostap Mamykin
# Nikita Solomennikov

class Simplexer:
    def __init__(self, n: int, row_count: int, col_count: int, type: str, eps: int = 3):
        self.n = n
        self.row_count = row_count
        self.col_count = col_count
        self.obj = list()
        self.data = list()
        self.b = list()
        self.type = type
        self.in_var = [i + n for i in range(self.row_count)]
        self.eps = eps
    
    def runInputData(self):

        print("Enter coefficients of objective function (one line with single space as a separator): ", end='')
        self.obj = list(map(float, input().split()))
        if len(self.obj) != n:
            print("Error: incorrect number of coefficients in the objective function!")
            exit()

        print("Enter the matrix of coefficients of constraint functions (line by line with single space as separator):")
        for i in range(self.row_count):
            temp_arr = list(map(float, input().split()))
            if len(temp_arr) != self.col_count:
                print("Error: incorrect number of elements in a row")
                exit()
            extra_arr = [0] * self.row_count
            extra_arr[i] = 1
            temp_arr += extra_arr
            self.data.append(temp_arr.copy())
            temp_arr.clear()

        print("Enter right-hand side values for the constraint functions (one line with space as separator): ", end='')
        self.b = list(map(float, input().split()))
        if len(self.b) != self.row_count:
            print(self.row_count, len(self.b))
            print("Error: incorrect number of values!")
            exit()

        print("Enter the approximation accuracy or -1 to use default eps=3: ", end='')
        new_eps = int(input())
        if new_eps == -1:
            pass
        elif new_eps < 0:
            print("Error: incorrect value of approximation accuracy!")
            exit()
        else:
            self.eps = new_eps


    def runIteration(self):
        self.display()
        
        k = self.data[0].index(min(self.data[0]))
        
        ratio_arr = list()
        for i in range(1, row_count + 1):
            try:
                ratio_arr.append(self.data[i][-1] / self.data[i][k])
                if ratio_arr[-1] <= 0:
                    ratio_arr[-1] = 1e9
            except ZeroDivisionError:
                ratio_arr.append(1e9)

        if min(ratio_arr) == 1e9:
            print("Unbounded (optimal solution cannot be found)")
            exit()

        g = ratio_arr.index(min(ratio_arr)) + 1

        self.in_var[g - 1] = k

        inter = self.data[g][k]

        for i in range(self.n + self.row_count + 1):
            self.data[g][i] /= inter
        
        # print(self.data[g])
        

        for i in range(self.row_count + 1):
            if i == g:
                continue
            pivot = self.data[i][k]
            for j in range(self.n + self.row_count + 1):
                self.data[i][j] -= pivot * self.data[g][j]

    def checkSolved(self):
        val = min(self.data[0][0:-1])
        if val >= 0:
            return True
        return False


    def solve(self):
        if self.type == 'max':
            for i in range(len(self.obj)):
                self.obj[i] *= -1

        for _ in range(self.row_count):
            self.obj.append(0)
        
        self.data.insert(0, self.obj)

        self.data[0].append(0)
        for i in range(1, self.row_count + 1):
            self.data[i].append(self.b[i - 1])

        print("\nBasic solution: ", end='')
        temp_arr = list()
        for _ in range(self.n):
            temp_arr.append(0)
        temp_arr += self.b

        basic_sol = 'F('

        for i in range(self.n):
            basic_sol += f"x{i + 1}, "

        for i in range(self.row_count):
            basic_sol += f"s{i + 1}, "
        
        basic_sol = basic_sol[:-2] + ") = "

        basic_sol += 'F(' + ', '.join(map(str, temp_arr)) + ') = 0'
        print(basic_sol)
        self.runIteration()
        
        while not self.checkSolved():
            self.runIteration()

        print("Final table:")
        self.display()

        print("Optimal solution found:")
        
        result = 'F('
        for i in range(self.n):
            result += f"x{i + 1}, "
        
        result = result[:-2] + ") = F("

        res_values = ['0'] * (self.n)
        line = 0
        for el in self.in_var:
            line += 1
            if el >= self.n:
                continue
            res_values[el] = f"{round(self.data[line][-1], self.eps)}"

        for el in res_values:
            result += f"{el}, "
        
        result = result[:-2] + ") = "
        
        sol = self.data[0][-1]
        
        if self.type == 'min':
            sol *= -1

        result += f"{round(sol, self.eps)}"
        
        # print("Solution:")
        print(result)
        exit()        

    def display(self):
        print(f"\n{self.row_count}x{self.col_count}\n----------------------")
        for i in range(n):
            print(f"x{i + 1}\t", end='')
        for i in range(self.row_count):
            print(f"s{i + 1}\t", end='')
        print("Sol.")
        for row in self.data:
            for el in row:
                print(round(el, self.eps), end='\t')
            print('')
        print('')

if __name__ == "__main__":
    print("Specify the type of LPP ('min' or 'max'): ", end='')
    type = input().lower()

    if type not in ['min', 'max']:
        print("Error: incorrect type!")

    print("Enter number of variables, rows and columns: ", end='')
    n, row_count, col_count = list(map(int, input().split()))

    if n != col_count:
        print("Error: incorrect number of variables or columns!")

    si = Simplexer(n, row_count, col_count, type)
    si.runInputData()
    si.solve()
