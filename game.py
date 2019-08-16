import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self._grid = self.createGrid(row, col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells

        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):

        """
        Create the grid here using the arguments row and col
        as the number of rows and columns of the grid to be made.

        The function should return the grid to be used in __init__()
        """
        grid = []
        for index in range(row):
            column_grid = []
            for item in range(col):
                column_grid.append(0)
            grid.append(column_grid)
        return grid        


    def setCell(self, cell, val):

        """
        This function should take two arguments cell and val and assign
        the cell of the grid numbered 'cell' the value in val.

        This function does not need to return anything.

        Use this function to change values of the grid.
        """

        row_number = cell // self.col
        col_number = cell % self.col
        self._grid[row_number][col_number] = val


    def getCell(self, cell):

        """"
        This function should return the value in cell number 'cell'
        of the grid.

        Use this function to access values of the grid
        """

        row_number = cell // self.col
        col_number = cell % self.col        
        return self._grid[row_number][col_number]


    def assignRandCell(self, init=False):

        """
        This function assigns a random empty cell of the grid
        a value of 2 or 4.

        In __init__() it only assigns cells the value of 2.

        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned
        a value of 4
        """

        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):

        """
        This function draws the grid representing the state of the game
        grid
        """

        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)
        print()


    def updateEmptiesSet(self):

        """
        This function should update the list of empty cells of the grid.
        """
        self.emptiesSet = []
        for cell in range(self.row * self.col):
            if self.getCell(cell) == 0:
                self.emptiesSet.append(cell)

    def collapsible(self):

        """
        This function should test if the grid of the game is collapsible
        in any direction (left, right, up or down.)

        It should return True if the grid is collapsible.
        It should return False otherwise.
        """

        is_collapsible = False
        
        if len(self.emptiesSet):
            is_collapsible = True
            
        elif not len(self.emptiesSet):
            
            # checks horizontally
            
            for index in range(self.row):
                if is_collapsible == True:  # stops loop if we already know the grid is collapsible
                    break
                for item in range(self.col - 1):
                    cell_number = item + (index * self.row)
                    cell_1 = self.getCell(cell_number)
                    cell_2 = self.getCell(cell_number + 1)
                    if cell_1 == cell_2:
                        is_collapsible = True
                        break
                    
            # checks vertically
            
            for index in range(self.row - 1):
                if is_collapsible == True:  # stops loop if we already know the grid is collapsible
                    break                
                for item in range(self.col):
                    cell_number = item + (index * self.row)
                    cell_1 = self.getCell(cell_number)
                    cell_2 = self.getCell(cell_number + self.row)
                    if cell_1 == cell_2:
                        is_collapsible = True
                        break
        return is_collapsible


    def collapseRow(self, lst):

        """
        This function takes a list lst and collapses it to the LEFT.

        This function should return two values:
        1. the collapsed list and
        2. True if the list is collapsed and False otherwise.
        """
        the_list = list(lst)
        
        previous_item = None    
        has_collapsed = False   
        
        # collapses the list if possible
        for item in the_list:
            if item == 0:
                the_list.remove(item)
                the_list.append(item)
        
        # checks to see if the list has collapsed
        if the_list != lst:
            has_collapsed = True
            
        # reduces the list if possible
        for index in range(len(the_list)):
            if the_list[index] == previous_item and the_list[index] != 0:
                the_list[index-1] = previous_item + the_list.pop(index)
                the_list.append(0)      # this part is necessary so the list length doesn't change
                self.score += the_list[index-1] # this part is for implementing the score system
                has_collapsed = True
            previous_item = the_list[index]      
            
        return the_list, has_collapsed
        
        

    def collapseLeft(self):

        """
        This function should use collapseRow() to collapse all the rows
        in the grid to the LEFT.

        This function should return True if any row of the grid is collapsed
        and False otherwise.
        """
        for row in range(self.row):
            counter = 0
            cell_list = []
            for item in range(self.col):
                cell = self.getCell(item + row * self.row)
                cell_list.append(cell)
            cell_list, has_collapsed = self.collapseRow(cell_list)
            for value in cell_list:
                self.setCell(counter + row * self.row, value)
                counter += 1
            if has_collapsed:
                will_collapse = True
        
        
        return will_collapse


    def collapseRight(self):

        """
        This function should use collapseRow() to collapse all the rows
        in the grid to the RIGHT.

        This function should return True if any row of the grid is collapsed
        and False otherwise.
        """

        will_collapse = False
        
        for row in range(self.row):
            counter = 0
            cell_list = []
            for item in range(self.col):
                cell = self.getCell(item + row * self.row)
                cell_list.append(cell)
            cell_list.reverse()
            cell_list, has_collapsed = self.collapseRow(cell_list)
            cell_list.reverse()
            for value in cell_list:
                self.setCell(counter + row * self.row, value)
                counter += 1
            if has_collapsed:
                will_collapse = True

        
        return will_collapse



    def collapseUp(self):

        """
        This function should use collapseRow() to collapse all the columns
        in the grid to UPWARD.

        This function should return True if any column of the grid is
        collapsed and False otherwise.
        """

        will_collapse = False
        
        for row in range(self.row):
            counter = 0
            cell_list = []
            for col in range(self.col):
                cell = self.getCell(row + col * self.row)
                cell_list.append(cell)
            cell_list, has_collapsed = self.collapseRow(cell_list)
            for value in cell_list:
                self.setCell(row + counter * self.row, value)
                counter += 1
            if has_collapsed:
                will_collapse = True        
        
        return will_collapse



    def collapseDown(self):

        """
        This function should use collapseRow() to collapse all the columns
        in the grid to DOWNWARD.

        This function should return True if any column of the grid is
        collapsed and False otherwise.
        """

        will_collapse = False
        
        for row in range(self.row):
            counter = 0
            cell_list = []
            for col in range(self.col):
                cell = self.getCell(row + col * self.row)
                cell_list.append(cell)
            cell_list.reverse()    
            cell_list, has_collapsed = self.collapseRow(cell_list)
            cell_list.reverse()  
            for value in cell_list:
                self.setCell(row + counter * self.row, value)
                counter += 1
            if has_collapsed:
                will_collapse = True                
        
        
        return will_collapse




class Game():
    def __init__(self, row=4, col=4, initial=2):

        """
        Creates a game grid and begins the game
        """

        self.game = Grid(row, col, initial)
        self.play()


    def printPrompt(self):

        """
        Prints the instructions and the game grid with a move prompt
        """

        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")

        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')


def main():
    game = Game()

main()