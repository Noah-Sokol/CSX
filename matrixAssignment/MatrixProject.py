'''
@author: NSokol25
Created on Nov 15, 2024
desc: Matrix class that has capabilities to add, multiply, find inverse of, 
find determinant of and put in reduced row echalont form
last edited: 12/2/24
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
            
        Prints matrix
    Output: 
        prints each point in matrix
        '''
        for i in self.data:
            for j in i:
                print(round(j,5), end=" ")
            print()

    @staticmethod
    def get_matrix_data():
        '''
        Gets rows, collumns and data for matrix
    Returns: 
        result - matrix - Matrix object with rows, cols and data filled out
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
        Adds two matricies

    Args:
        m2 - matrix - matrix object being added
    Returns:
        result - matrix - matrix after addition
        '''
        if self.cols != m2.cols or self.rows != m2.rows:
            print(f'Both matricies must have the same amount of rows and columns')
            return False
        result = Matrix(self.rows,self.cols, [[0 for _ in range(self.cols)] for _ in range(self.rows)])
        for i in range(self.rows):
            for j in range(self.cols):
                #resulting matrix at point is self matrix + m2 matrix
                result.data[i][j] = self.data[i][j] + m2.data[i][j]

        return result


    def matrix_times(self, m2):
        '''
        Multiplies matricies
    Args:
        m2 - matrix - second matrix being multiplied
    Returns: 
        result - matrix - output of multiplied matrix
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
        Multiplies row with a scalar value
    Args:
        Scalar - int - value row is being multiplied by
        Rownum - int - row being multiplies (input actual row not row-1)
    Returns: 
        Result - matrix - output of matrix after being multiplied
        '''
        if rownum-1 >= self.rows:
            print(f"row {rownum} is out of range in the matrix, please enter a number less than {self.rows}")
        result = Matrix(self.rows,self.cols, deepcopy(self.data))
        for i in range(self.cols):
            result.data[rownum-1][i] *= scalar
        return result
    
    def switchRows(self, first_row, second_row):
        '''
        Switches rows
    Args:
        First_row - int - first row being switched
        Second_row - int - second row being switched
    Returns: 
        self - Matrix with rows switched
        '''
        temp = self.data[first_row-1]
        self.data[first_row-1] = self.data[second_row-1]
        self.data[second_row-1] = temp
        return self

    def linearCombRows(self, scalar, row_num, second_row):
        '''
        Multiplies a row by scalar value then adds that result to another row
    Args:
        Scalar - int - value row is being multiplied by
        First_row - int - row getting changed
        Second_row - int - row being multipies then added
    Returns: 
        result - Matrix - resulting matrix after being combined
        '''
        temp_data = []
        for i in range(self.rows):
            #creates matrix with all rows empty but row being added
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
        Uses recoursive algorithm to find a point that is not zero
    Args:
        rowNum - int - row of starting point
        colNum - int - collumn of starting point
    Returns: 
        rownum - int - returns the row with 0 at point
        False - bool - if there is no point with 0 return False
        '''
        try:
            return rowNum+1 if round(self.data[rowNum+1][colNum],3) != 0 else self.recursiveNonZeroFinder(rowNum+1, colNum)
        except IndexError:
                return False

    def rowReduce(self):
        '''
        Uses Jordan-Gauss method to find row reduced form of matrix
    Returns: 
        result - Matrix - Row reduced echalont form of Matrix
        '''
        if round(self.data[0][0],3) == 0:
            nonZeroRow = self.recursiveNonZeroFinder(1, 0)
            if nonZeroRow is not False:
                self = self.switchRows(1,nonZeroRow + 1)
        if round(self.data[0][0],3) != 1 and round(self.data[0][0],3) != 0:
            scalar = 1/self.data[0][0]
            self = self.scalarTimesRow(scalar,1)
        for i in range(self.cols-1 if self.cols == self.rows +1 else self.cols):
            #starts at pivot every times
            for j in list(range(i,self.rows))+list(range(0,i)):
                if i == j:
                    #creates pivot but if point is 0 switch rows with a nonzero row
                    if round(self.data[i][i],3) == 0:
                        nonZeroRow = self.recursiveNonZeroFinder(j, i)
                        if nonZeroRow is not False:
                            self = self.switchRows(j+1,nonZeroRow+1)
                    if round(self.data[i][i],3) not in [0,1]:
                        self = self.scalarTimesRow(1/self.data[i][i],i+1)
                elif j > i:
                    #makes 0 in point under pivot
                    if round(self.data[j][i],3) != 0 and round(self.data[i][i],3) != 0:
                        self = self.linearCombRows(-self.data[j][i]/self.data[i][i],i+1,j+1)
                else:
                    #makes 0 in point over pivot
                    if round(self.data[j][i],3) != 0 and round(self.data[i][i],3) != 0:
                        self = self.linearCombRows(-self.data[j][i]/self.data[i][i],i+1,j+1)        
      
        return self

    def invert(self):
        '''
        Finds invert of matrix
    Args:
        Scalar - int - value row is being multiplied by
        First_row - int - row getting changed
        Second_row - int - row being multipies then added
    Returns: 
        result - Matrix - resulting matrix after being combined
        '''
        if self.cols != self.rows:
            print("Matrix must be square to invert")
            return False
        elif self.cols == 1:
            return Matrix(1,1,[1/self.data[0][0]])
        if round(Matrix.recursiveDeterminateFinder(self.data), 3) == 0:
            print("Inverse does not exist, determinate = 0")
            return False
        #augmented matrix with identity matrix as data
        augmentedMatrix = Matrix(self.rows,self.cols,[[1 if i == j else 0 for j in range(self.rows)] for i in range(self.cols)])
        #creates pivot in first point
        if round(self.data[0][0],3) != 1 and round(self.data[0][0],3) != 0:
            scalar = 1/self.data[0][0]
            self = self.scalarTimesRow(scalar,1)
            augmentedMatrix = augmentedMatrix.scalarTimesRow(scalar,1)
        elif round(self.data[0][0],3) == 0:
            scalarValue = self.recursiveNonZeroFinder(1, 0) + 1
            self = self.linearCombRows(1,scalarValue,1)
            augmentedMatrix = augmentedMatrix.linearCombRows(1,scalarValue,1)
        for i in range(self.cols):
            #starts at pivot every times
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
                #makes 0 in point under pivot
                elif j > i:
                    if round(self.data[j][i],3) != 0:
                        scalar = (-self.data[j][i])
                        self = self.linearCombRows(scalar,i+1,j+1)
                        augmentedMatrix = augmentedMatrix.linearCombRows(scalar,i+1,j+1)
                #makes 0 in point over pivot
                else:
                    if round(self.data[j][i],3) != 0:
                        scalar = (-self.data[j][i])
                        self = self.linearCombRows(scalar,i+1,j+1)
                        augmentedMatrix = augmentedMatrix.linearCombRows(scalar,i+1,j+1)

        return augmentedMatrix


    @staticmethod
    def twoByTwoDeterminate(matrix: list):
        '''
        Static method that returns determinant of 2x2 matrix
    Args:
        matrix - list - data of matrix
    Returns
        list - determinant of 2x2 matrix
        '''
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0]) if len(matrix) == len(matrix[0]) and len(matrix) == 2 else False

    @staticmethod
    def reducedDeterminateList(matrix: list, curRow, curCol):
        '''
        Static method that returns list of matrix without all points in chosen row and col
    Args:
        matrix - list - data of matrix
        curRow - Row to remove points from
        curCol - Col to remove points from
    Returns
        list - matrix without points in chosen row and col
        '''
        return [[matrix[j][i] for i in range(len(matrix)) if i != curCol]for j in range(len(matrix)) if j != curRow]
    
    @staticmethod
    def recursiveDeterminateFinder(matrix: list):
        '''
        Static recursive method that returns determinant of a square matrix
    Args:
        matrix - list - data of matrix
    Returns
        sum(result) - result contains all 2x2 determinantes then sum adds all of them
        '''
        if len(matrix) != 2:
            result = []
            for i in range(len(matrix)):
                #list to find determinante of
                nextList = Matrix.reducedDeterminateList(matrix, 0, i)
                #add determinant of matrix to result recoursively and flips between positive and negitive with power of -1^1
                result.append(pow(-1, i) * matrix[0][i] * Matrix.recursiveDeterminateFinder(nextList))
            return sum(result)
        else:
            #base case 2x2 matrix
            return Matrix.twoByTwoDeterminate(matrix)
        
matrix = Matrix(3,3,[[0,0,1],[1,2,3],[4,5,8]])
print(Matrix.recursiveDeterminateFinder(matrix.data))