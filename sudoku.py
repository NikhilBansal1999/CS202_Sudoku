import os
import sys

def read_from_console(): #reads the input provided by user on the console
    data = list()
    for i in range(9):
        inp = input().split()
        data.append(list())
        for j in range(9):
            data[i].append(inp[j])

    return data

def get_ind(row_num,col_num,num):
    #given the row number, column number, number it outputs the corresponding boolean variable number
    #each of the arguments are between 1 and 9, both included
    index = 81*(row_num-1)+9*(col_num-1)+num
    return index

def get_cell(index):
    #given the index it outputs the row ,column and number in the cell
    num = index % 9
    if num == 0:
        num=9

    index=index-num
    row_num=(index//81)+1
    col_num=(index-(row_num-1)*81)//9
    col_num=col_num+1

    return [row_num, col_num,num]

def exactly_one(num_list):
    #given a list of boolean variables it outputs the set of conditions specifying that only one of those are true
    condition_list=list()
    condition_str=""
    for var in num_list:#Condition for at least one to be true
        condition_str=condition_str+str(var)+" "
    condition_str=condition_str+"0"
    condition_list.append(condition_str)
    for i in range(len(num_list)):
        for j in range(i+1,len(num_list)):
            condition_str="-"+str(num_list[i])+" -"+str(num_list[j])+" 0"
            condition_list.append(condition_str)
    return condition_list

def encode_sudoku(sudoku_data):
    conditions=list()
    #A number must appear in each row exactly once
    for row in range(1,10):
        for num in range(1,10):
            var_list=list()

            for col in range(1,10):
                var_list.append(get_ind(row,col,num))

            con=exactly_one(var_list)
            for c in con:
                conditions.append(c)

    #A number must appear in each column exactly once
    for col in range(1,10):
        for num in range(1,10):
            var_list=list()

            for row in range(1,10):
                var_list.append(get_ind(row,col,num))

            con=exactly_one(var_list)
            for c in con:
                conditions.append(c)

    #Every box has at exactly  one number
    for row in range(1,10):
        for col in range(1,10):
            var_list=list()

            for num in range(1,10):
                var_list.append(get_ind(row,col,num))

            con=exactly_one(var_list)
            for c in con:
                conditions.append(c)

    #A number must appear in each 3x3 box exactly once
    for box_row in range(1,4):
        for box_col in range(1,4):
            for num in range(1,10):
                var_list=list()
                for row in range(3*box_row-2,3*box_row+1):
                    for col in range(3*box_col-2,3*box_col+1):
                        var_list.append(get_ind(row,col,num))
                con=exactly_one(var_list)
                for c in con:
                    conditions.append(c)

    #every number present in main diagonal only once
    for num in range(1,10):
        var_list=list()
        for rowcol in range(1,10);
            var_list.append(get_ind(rowcol,rowcol,num))
        con=exactly_one()
        for c in con:
            conditions.append(c)

    #every number present in other diagonal only once
    for num in range(1,10):
        var_list=list()
        for rowcol in range(1,10);
            var_list.append(get_ind(rowcol,10-rowcol,num))
        con=exactly_one()
        for c in con:
            conditions.append(c)    

    #Given input sudoku data
    for row in range(9):
        for col in range(9):
            if sudoku_data[row][col] == '*':
                continue
            else:
                boolean_ind=get_ind(row+1,col+1,int(sudoku_data[row][col]))
                con=str(boolean_ind)+" 0"
                conditions.append(con)

    #write to the file
    fhand=open("Sudoku_data","w")
    fhand.write("p cnf 729 "+str(len(conditions))+"\n")
    for c in conditions:
        fhand.write(c+"\n")
    fhand.close()

def solve_sudoku():
    os.system("minisat Sudoku_data Sudoku_solution")
    fhand=open("Sudoku_solution","r")
    solution=list()
    for i in range(9):
        solution.append(list())
        for j in range(9):
            solution[i].append("*")

    sol=""
    for line in fhand:
        if line.strip() == "UNSAT":
            print("SUDOKU NOT SOLVABLE")
        elif line.strip() == "SAT":
            print("SUDOKU SOLVED")
        else:
            sol=line.strip()

    for val in sol.split():
        output=int(val.strip())
        if output>0:
            cell=get_cell(output)
            solution[cell[0]-1][cell[1]-1]=cell[2]

    return solution

data=read_from_console()
encode_sudoku(data)
solution_gen=solve_sudoku()
for i in range(9):
    for j in range(9):
        print(solution_gen[i][j],end=" ")
    print()
