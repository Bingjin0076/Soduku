import numpy as np
import itertools
import copy


## this function below checks whether two cells are in the same row or the same column
## or in the same square or none above
## notice that two cells can be at the same row and the same square the same time. 
## the function return a list of true or false, indicating in the same row or the same column or in the same square

def check_cells(cell1, cell2):
    r = [False]*3

    ##in the same row:
    if cell1[0] == cell2[0]:
        r[0] = True
    ## check in the same column   
    if cell1[1] == cell2[1]:
        r[1] = True
    ## check in the same square
    if (cell1[0]//3 == cell2[0]//3) and (cell1[1]//3 == cell2[1]//3):
        r[2] = True
    
    return r

## the input may not start with 0, thus shifting the index is necessary
## The second parameter "shifts" is a list of len 3, telling whether to shift the row index, column index or the number by subtracting the shift num

def shift_index(positions, shifts):
    new_positions = []
    for p in positions:
        new_positions.append((p[0] - shifts[0],p[1] - shifts[1],p[2] - shifts[2]))                
    return new_positions


class Soduku:

    ## size of the soduku
    s = 3

    ## possible fills for each cell. It is a matrix of size (s^2)^2 * s^2
    F = np.ones((s**2,s**2,s**2))
    ## the first 2 dimensionas are to record the position of each cell, the last dimention
    ## is to record all the possible numbers from 1 to s^2. This matrix F is a matrix consisting of 1 and 0s.

    ## positions is a list of tuples, a tuple is like (1,1,9), which means in the position (1,1) cell, 9 is filled in.
    ## s is the size of the soduku
    choice = []

    ## here we are adding a choice, which means this soduku will be updated under this choice
    def __init__(self,n,positions, choice = []):
        self.s = n
        self.choice = choice
        # print(self.F.shape)
        for position in positions:
            self.F[position[0],position[1],:] = 0 
            self.F[position] = 1
    
    def copy(self):
        S = Soduku(self.s,[],self.choice)
        S.F = copy.copy(self.F)
        return S


    
    ## this function is to obtain the positions where the fill-in is sure to be correct.
    ## the function returns a set consisting of all such positions
    def definite_positions(self):
        
        results = np.where((self.F.sum(axis = 2)) == 1)
        cells = list(zip(results[0],results[1]))
        pos = []
        for cell in cells:
            num = list(self.F[cell[0],cell[1],:]).index(1)
            pos.append((cell[0],cell[1],num))

        return pos

    ## This function is to decide whether there is some contradiction in the fillings
    ## if the there is a cell with all entries being 0, then there is something wrong, return True
    ## else return false, and in this case, we do not know whether there is contradiction or not
    def contradiction(self):
        if (self.F.sum(axis = 2) == 0).any():
            return True
        else:
            False
        
    
    ## This function is to check whether the soduku is fully filled. If it is, then true is returned.
    def done(self):
        pos = self.definite_positions()
        if len(pos) == (self.s)**4:
            return True
        else:
            return False


    ## this function is to update the soduku after filling in several positions
    def updateF(self,positions = []):

        ## this set means the positions that the number is sure to be correct
        def_pos = self.definite_positions()

        ## If the soduku is already fully filled, then no need to update.
        if len(def_pos) == self.s**2:
            return True   
        ## If there is contradiction,then no need to update
        if self.contradiction():
            return False 

        # for position in positions:
        #     if self.F[position] == 0:
        #         return False

        #     ## first update that cell
        #     self.F[position[0],position[1],:] = 0
        #     self.F[position] = 1
        #     if position not in def_pos:
        #         def_pos.append(position)
        if positions == []:
            positions = def_pos


        ##rule 1: For each cell (i,j), the possible numbers in this cell are those not
        ## appearing in the same row or column or the square box.
        for position in positions:
            if self.F[position] == 0:
                return False
            ## first update that cell
            self.F[position[0],position[1],:] = 0
            self.F[position] = 1
            if position not in def_pos:
                def_pos.append(position)

            ## only need to update cells which is not filled in and not in the positions
            cellx= [(position[0], j, position[2])  for j in range(self.s**2) ]
            celly = [(i, position[1], position[2]) for i in range(self.s**2) ]
            cells = [((position[0]//self.s)* self.s + i, (position[1]//self.s)* self.s+ j,position[2]) for (i,j) in itertools.product(range(self.s),range(self.s))]
            update_cells = set(cellx).union(set(celly).union(set(cells)))
            update_cells.remove(position)
            for cell in update_cells:
                self.F[cell] = 0
        # print(self.definite_positions())

        # print('After rule1:')
        # self.display()
        ## rule2: Fix a number 1 to s^2, if the possible cells for this number is unique
        ## in that row or column or in the square then that number must be filled in the unique cell

        ## notice that the number affected is not only the number filled in 
        for i in range(self.s**2):
            c = np.where(self.F[:,:,i] == 1)
            cells = list(zip(c[0],c[1]))
            cells = [p for p in cells if (p[0],p[1],i) not in def_pos]
            
            for k in range(len(cells)):
                r = [False]*3
                for j in range(len(cells)):
                    if j!=k:
                        a = check_cells(cells[j],cells[k])
                        r = [(r[n] | a[n]) for n in range(len(a))]
                ## if cells[i] is unique in either r or c or s

                if all(r) == False:
                    row = cells[k][0]
                    col = cells[k][1]

                    ## check whether there is contradiction
                    if self.F[row,col, i] == 0:
                        return False
                    self.F[row,col, :] = 0
                    self.F[row,col, i] = 1 
                    # print('The cell to fill in after rule2 is',(row,col,i))

        # print(self.definite_positions())
        # self.display()
        # print("after rule2")
        # self.display()

        ## rule3: If there are two cells whose possible fill-in numbers are the same and of size 2 in the 
        ## same row or the same column or the same squre. The other cells in the same row (reps. column, squre)
        ## can not be these two numbers
        ## notice that rule3 will not provide more cases for rule2
        
        c = np.where(self.F.sum(axis = 2) == 2)
        cells = list(zip(c[0],c[1]))
        pairs = []
        for cell in cells:
            nums = [i for i in range(self.s**2) if self.F[cell[0],cell[1],i] == 1]
            pairs.append(tuple(nums))
        dup_pairs = [pair for pair in set(pairs) if pairs.count(pair) == 2]

        for pair in dup_pairs:
            pair_cells = [cells[i] for i, p in enumerate(pairs) if p == pair]
            a = check_cells(pair_cells[0], pair_cells[1])

            ## check whether there is contradiction
            if ((self.F[pair_cells[0][0],pair_cells[0][1],pair] == 0 ).any()) | ((self.F[pair_cells[1][0],pair_cells[1][1],pair] == 0 ).any()):
                return False
            if a[0]:
                self.F[pair_cells[0][0],:,pair] = 0 
                # print('The pair is ', pair, 'the cells are', pair_cells)
                # self.F[pair_cells[0][0],:,pair[1]] = 0               
            if a[1]:    
                self.F[:,pair_cells[0][1],pair] = 0 
                # print('The pair is ', pair, 'the cells are', pair_cells)
                # self.F[:,pair_cells[0][1],pair[1]] = 0                   
            if a[2]:    
                for (i,j)  in itertools.product(range(self.s),range(self.s)):
                    self.F[(pair_cells[0][0]//self.s)*self.s + i, (pair_cells[0][1]//self.s)*self.s + j, pair] = 0
                    # print('The pair is ', pair, 'the cells are', pair_cells)

            self.F[pair_cells[0][0],pair_cells[0][1],pair] = 1
            self.F[pair_cells[1][0],pair_cells[1][1],pair] = 1
            
        # print(self.definite_positions())
        # print("after rule3")
        # self.display()


        ## once all the three rules are updated, then we may need to update our F again,
        ## because above process, F can be updated. 
        new_def_pos = self.definite_positions()
        new_def_pos = [p for p in new_def_pos if p not in def_pos]
        if new_def_pos == []:
            return True
        else:
            # print('The new positions to fill in are ', new_def_pos)
            self.updateF(new_def_pos)
            

    ## how to update the choice after we can not update F anymore?
    ## we choose the number and the rows where this number may appears which has median completetion degree 
    def make_choice(self):
        positions = self.definite_positions()
        sum = np.zeros(self.s**2)
        for p in positions:
            sum += self.F[p[0],p[1],:]
        ssum = [a for a in sum if a < self.s**2]
        ssum.sort()
        num = list(sum).index(ssum[len(ssum)//2])

        ## once the number is choosen, we will choos the row. Again we would like to choose
        ## the row which has highest completion rate
        rates = []
        for row in range(self.s**2):
            all_cols = np.where(self.F[row,:,num] == 1)
            def_cols = [p[1] for p in positions if( p[0] == row) & (p[2] == num)]
            unfinish_rate = (len(all_cols) -len(def_cols))/len(all_cols)
            rates.append(unfinish_rate)
        
        rates = [r if r > 0 else 2 for r in rates]
        row = np.argmin(rates)
        cols = np.where(self.F[row,:,num] == 1)[0]
        # print(cols)
        choices = [(row,col,num) for col in cols if (row,col,num) not in positions]

        # ## always make the left most choice, which means the col index is the smallest one
        # self.choice = [choices[0]]

        return choices
        
        
    ## display the soduku, only the cells filled in
    def display(self, positions = 'None'):
        if self.contradiction == True:
            print("There is some error in this soduku.")
            return False
        if positions == 'None':
            positions = shift_index(self.definite_positions(), [0,0,-1])

        cells = [(p[0],p[1]) for p in positions]     
        print_string = ''
        for (i,j) in itertools.product( range(self.s**2),range(self.s**2)):
            if (i,j) not in cells:
                print_string += '* '
            else:
                print_string += str(positions[cells.index((i,j))][2])+ ' '
            if j == (self.s**2 -1):
                print_string += '\n'
        print(print_string)   
        return True

            

            
        




# ## next we will use the tree structure to record the guess we make during the completion of the soduku

# ## how to update the choice after we can not update F anymore?
# ## we choose the number and the rows where this number may appears which has median completetion degree 
# def make_choice(soduku):
#     positions = soduku.definite_positions()
#     sum = np.zeros(soduku.s**2)
#     for p in positions:
#         sum += soduku.F[p[0],p[1],:]
#     ssum = [a for a in sum if a < soduku.s**2]
#     ssum.sort()
#     num = list(sum).index(ssum[len(ssum)//2])

#     ## once the number is choosen, we will choos the row. Again we would like to choose
#     ## the row which has highest completion rate
#     rates = []
#     for row in range(soduku.s**2):
#         all_cols = np.where(soduku.F[row,:,num] == 1)
#         def_cols = [p[1] for p in positions if( p[0] == row) & (p[2] == num)]
#         unfinish_rate = (len(all_cols) -len(def_cols))/len(all_cols)
#         rates.append(unfinish_rate)
    
#     rates = [r if r > 0 else 2 for r in rates]
#     row = np.argmin(rates)
#     cols = np.where(soduku.F[row,:,num] == 1)[0]
#     # print(cols)
#     return [(row,col,num) for col in cols if (row,col,num) not in positions]
    
        
    
    
# ## It seems that there is not need to have the node structure
# ## what is the node of this choice tree?
# ## the node consists of a fill-in choice and the soduku right before making the choice.
# class node:
#     children = {}
    
#     ## here the choice the fill-in choice and the state is the soduku state right before the choice
#     def __init__(self, choice, soduku) -> None:
#         self.choice = choice
#         self.soduku= soduku
    
#     def add_children(self,nodes):
        
#         self.children = self.children.union(set(nodes))



def soduku_solver(soduku):

    a = soduku.updateF(soduku.choice)
    # soduku.display()
    if a == False:
        print('No solution.')
        return False, soduku
    if soduku.done():
        return True, soduku

    choices = soduku.make_choice()
    print(choices)
    results = [True] * len(choices)
    for i, choice in enumerate(choices):
        print("The choice made here is", choice)
        print('The soduku before updating the choice:')
        
        n_soduku = soduku.copy()     
        n_soduku.choice = [choice]

        n_soduku.display()

        result, updated_soduku = soduku_solver(n_soduku)
        updated_soduku.display()
        if result == True:
            return True, updated_soduku
        else:
            print('wrong choices')
            results[i] = False
    if results == [False]*len(choices):
        return False, soduku
        
    
original_positions =[
(1,2,3),(1,7,8),(1,8,7),
(2,7,4),(2,9,2),
(3,2,1),(3,6,4),(3,8,5),
(4,3,8),(4,6,7),(4,8,4),
(5,5,6),
(6,2,9),(6,4,8),(6,7,3),
(7,2,8),(7,4,7),(7,8,1),
(8,1,4),(8,3,7),
(9,2,6),(9,3,1),(9,8,2)]
positions = shift_index(original_positions,[True,True,True])  
S = Soduku(3,positions)
S.display()
# T = S.copy()
# S.display()
# # # print(S.definite_positions())
# T.updateF()
# # # print(S.definite_positions())
# print("S")
# S.display()
# print('T')
# T.display()

print("Start to solve the soduku")
a, solved_S = soduku_solver(S)   
# print(a)
# solved_S.display()
# print(check_cells((0,6), (3,8)))
# print(make_choice(S))
    
    

    


                        
            


        

            

                


    


   






        