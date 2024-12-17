from MatrixProject import Matrix
if __name__ == "__main__":
    while True:
        while True:
            try:
                choice = int(input("Enter 1 to add two matricies\t\t\tEnter 2 to multiply two matricies\nEnter 3 to multiply a matrix by a scalar number\tEnter 4 to switch rows\nEnter 5 to do a linear combination of rows\tEnter 6 to find the reduced row echalont form of a matrix\nEnter 7 to find the inverse of a matrix\t\tEnter 8 to find the determinant of a matrix\nEnter 9 to end: "))
                if choice not in [1,2,3,4,5,6,7,8,9]:
                    raise ValueError 
                break
            except ValueError:
                print("x")
        if choice == 1:
            print('Enter Matrix 1:')
            m1 = Matrix.get_matrix_data()
            print('Enter Matrix 2:')
            m2 = Matrix.get_matrix_data()
            result = m1.matrix_plus(m2)
        elif choice == 2:
            print('Enter Matrix 1:')
            m1 = Matrix.get_matrix_data()
            print('Enter Matrix 2:')
            m2 = Matrix.get_matrix_data()
            result = m1.matrix_times(m2)
        elif choice == 3:
            print('Enter Matrix 1:')
            m1 = Matrix.get_matrix_data()
            while True:
                try:
                    scalar = float(input("Enter your scalar value: "))
                    row_num = int(input("Enter which row you would like to multiply: "))
                    break
                except ValueError:
                    print('please enter a number')
            result = m1.scalarTimesRow(scalar,row_num)
        elif choice == 4:
            print('Enter Matrix 1:')
            m1 = Matrix.get_matrix_data()
            while True:
                try:
                    firstRow = int(input("Enter the index of the first row to switch: "))
                    if firstRow not in range(1,m1.cols):
                        raise ValueError
                    secondRow = int(input("Enter the index of the second row to switch: "))
                    if secondRow not in range(1,m1.cols+1):
                        raise ValueError
                    m1.switchRows(firstRow,secondRow)
                    break
                except ValueError:
                    print(f'please enter a number in the range of 1-{len(m1.data)-1}')
        elif choice == 5: 
            print('Enter Matrix:')
            m1 = Matrix.get_matrix_data()
            while True:
                try:
                    scalar = float(input("Enter your scalar value: "))
                    row_num = int(input("Enter which row you would like to multiply: "))
                    if row_num not in range(1,m1.rows+1):
                        raise NameError
                    break
                except ValueError:
                    print('please enter a number')
                except NameError:
                    print(f"please enter a number in the range of 1-{m1.rows+1}")
            while True:
                try:
                    second_Row = int(input("Enter the index of the row to switch: "))
                    if second_Row not in range(1,m1.rows+1):
                        raise ValueError
                    break
                except ValueError:
                    print(f'please enter a number in the range of 1-{m1.rows+1}')
            result = m1.linearCombRows(scalar, row_num, second_Row)
        elif choice == 6:
            print('Enter Matrix:')
            m1 = Matrix.get_matrix_data()
            result = m1.rowReduce()
        elif choice == 7:
            print('Enter Matrix:')
            m1 = Matrix.get_matrix_data()
            result = m1.invert()
        elif choice == 8:
            print('Enter Matrix:')
            m1 = Matrix.get_matrix_data()
            if m1.cols != m1.rows:
                print('matrix must be square to find determinate')
                result = False
            else:
                result = Matrix.recursiveDeterminateFinder(m1.data)
                print(result)
                result = False
        elif choice == 9:
            break
        if result != False:
            print('result:')
            result.print_matrix()

