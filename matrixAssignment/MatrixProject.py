'''
Author: Noah Sokol

'''
from copy import deepcopy


class Matrix:
    def __init__(self, rows, cols, data = None):
        self.rows = rows
        self.cols = cols
        if data == None:
            self.data = Matrix.get_matrix_data(self)
        else:
            self.data = data

    def print_matrix(self):
        '''
        
        '''
        for i in self.data:
            for j in i:
                print(round(j,5), end=" ")
            print()

    @staticmethod
    def get_matrix_data():
        '''
        
        '''
        while True:
            try:
                rows = int(input("please inupt how many rows you want: "))
                cols = int(input("please inupt how many colums you want: "))
                if rows < 0 or cols < 0:
                    raise NameError
                break
            except ValueError:
                print("Please input integers only")
            except NameError:
                print('Please enter a positive number')
        result_data = [[0 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            while True:
                try:
                    temp_input = input(f"please input row {i+1} sperated by commas: ").split(',')
                    if len(temp_input) != cols:
                        raise ValueError
                    for j in range(len(temp_input)):                 #will raise value error if
                        temp_input[j-1] = int(temp_input[j-1])       #not int and converts to int
                    result_data[i] = temp_input
                    break
                except ValueError:
                    print(f"please enter {cols} values in the form 1,2,3")
        result = Matrix(rows, cols, result_data)
        result.print_matrix()



        return result

    def matrix_plus(self, m2):
        '''
        
        
        '''
        if self.cols != m2.cols or self.rows != m2.rows:
            print(f'Both matricies must have the same amount of rows and columns')
            return False
        result = Matrix(self.rows,self.cols, [[0 for _ in range(self.cols)] for _ in range(self.rows)])
        for i in range(self.rows):
            for j in range(self.cols):
                result.data[i][j] = self.data[i][j] + m2.data[i][j]

        return result


    def matrix_times(self, m2):
        '''
        
        
        '''
        if self.cols != m2.rows:
            print(f"the amount of collumns on matrix 1 must = the amount of rows on matrix 2")
            return False
        currData = 0
        result = Matrix(self.rows,m2.cols, [[0 for _ in range(m2.cols)] for _ in range(self.rows)])
        for i in range(result.rows):
            for j in range(result.cols):
                for h in range(self.cols):
                    currData += self.data[i][h] * m2.data[h][j]
                result.data[i][j] = currData
                currData = 0

        return result

    def scalarTimesRow(self, scalar, rownum):
        '''
        
        
        '''
        if rownum-1 >= self.rows:
            print(f"row {rownum} is out of range in the matrix, please enter a number less than {self.rows}")
        result = Matrix(self.rows,self.cols, deepcopy(self.data))
        for i in range(self.cols):
            result.data[rownum-1][i] *= scalar
        return result
    
    def switchRows(self, first_row, second_row):
        '''
        
        '''
        temp = self.data[first_row-1]
        self.data[first_row-1] = self.data[second_row-1]
        self.data[second_row-1] = temp
        return self

    def linearCombRows(self, scalar, row_num, second_row):
        '''
        
        '''
        temp_data = []
        for i in range(self.rows):
            if i != second_row-1:
                temp_data += [[0 for _ in range(self.cols)]]
            else:
                temp_data += [self.data[row_num-1].copy()]
        result = Matrix(self.rows,self.cols,temp_data)
        result = result.scalarTimesRow(scalar, second_row)
        result = result.matrix_plus(self)
        return result
    
    def recursiveNonZeroFinder(self, rowNum, colNum):
        '''
        
        '''
        try:
            return rowNum+1 if round(self.data[rowNum+1][colNum],3) != 0 else self.recursiveNonZeroFinder(rowNum+1, colNum)
        except IndexError:
                return False

    def rowReduce(self):
        '''
        
        
        '''
        if round(self.data[0][0],3) == 0:
            nonZeroRow = self.recursiveNonZeroFinder(1, 0)
            if nonZeroRow is not False:
                self = self.switchRows(1,nonZeroRow + 1)
        if round(self.data[0][0],3) != 1 and round(self.data[0][0],3) != 0:
            scalar = 1/self.data[0][0]
            self = self.scalarTimesRow(scalar,1)
        for i in range(self.cols-1 if self.cols == self.rows +1 else self.cols):
            for j in list(range(i,self.rows))+list(range(0,i)):
                if i == j:
                    if round(self.data[i][i],3) == 0:
                        nonZeroRow = self.recursiveNonZeroFinder(j, i)
                        if nonZeroRow is not False:
                            self = self.switchRows(j+1,nonZeroRow+1)
                    if round(self.data[i][i],3) not in [0,1]:
                        self = self.scalarTimesRow(1/self.data[i][i],i+1)
                elif j > i:
                    if round(self.data[j][i],3) != 0 and round(self.data[i][i],3) != 0:
                        self = self.linearCombRows(-self.data[j][i]/self.data[i][i],i+1,j+1)
                else:
                    if round(self.data[j][i],3) != 0 and round(self.data[i][i],3) != 0:
                        self = self.linearCombRows(-self.data[j][i]/self.data[i][i],i+1,j+1)        
      

        return self

    def invert(self):
        '''
        
        
        '''
        if self.cols != self.rows:
            print("Matrix must be square to invert")
            return False
        if round(Matrix.recursiveDeterminateFinder(self.data), 3) == 0:
            print("Inverse does not exist, determinate = 0")
            return False
        augmentedMatrix = Matrix(self.rows,self.cols,[[1 if i == j else 0 for j in range(self.rows)] for i in range(self.cols)])
        if round(self.data[0][0],3) != 1 and round(self.data[0][0],3) != 0:
            scalar = 1/self.data[0][0]
            self = self.scalarTimesRow(scalar,1)
            augmentedMatrix = augmentedMatrix.scalarTimesRow(scalar,1)
        elif round(self.data[0][0],3) == 0:
            scalarValue = self.recursiveNonZeroFinder(1, 0) + 1
            self = self.linearCombRows(1,scalarValue,1)
            augmentedMatrix = augmentedMatrix.linearCombRows(1,scalarValue,1)
        for i in range(self.cols):
            for j in list(range(i,self.rows))+list(range(0,i)):
                if i == j:
                    if round(self.data[i][i],3) == 0:
                        nonZeroRow = self.recursiveNonZeroFinder(j, i)
                        self = self.switchRows(j+1,nonZeroRow+1)
                        augmentedMatrix = augmentedMatrix.switchRows(j+1,nonZeroRow+1)
                    if round(self.data[i][i],3) not in [0,1]:
                        scalar = 1/self.data[i][i]
                        self = self.scalarTimesRow(scalar,i+1)
                        augmentedMatrix = augmentedMatrix.scalarTimesRow(scalar,i+1)
                elif j > i:
                    if round(self.data[j][i],3) != 0:
                        scalar = (-self.data[j][i])
                        self = self.linearCombRows(scalar,i+1,j+1)
                        augmentedMatrix = augmentedMatrix.linearCombRows(scalar,i+1,j+1)
                else:
                    if round(self.data[j][i],3) != 0:
                        scalar = (-self.data[j][i])
                        self = self.linearCombRows(scalar,i+1,j+1)
                        augmentedMatrix = augmentedMatrix.linearCombRows(scalar,i+1,j+1)

        return augmentedMatrix


    @staticmethod
    
    def twoByTwoDeterminate(matrix: list):
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0]) if len(matrix) == len(matrix[0]) and len(matrix) == 2 else False

    @staticmethod
    def reducedDeterminateList(matrix: list, curRow, curCol):
        return [[matrix[j][i] for i in range(len(matrix)) if i != curCol]for j in range(len(matrix)) if j != curRow]
    
    @staticmethod
    def recursiveDeterminateFinder(matrix: list):
        if len(matrix) != 2:
            result = []
            for i in range(len(matrix)):
                nextList = Matrix.reducedDeterminateList(matrix, 0, i)
                result.append(pow(-1, i) * matrix[0][i] * Matrix.recursiveDeterminateFinder(nextList))
            return sum(result)
        else:
            return Matrix.twoByTwoDeterminate(matrix)