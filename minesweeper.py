import random

def gen_minesweeper(w, h, num_mines):
    '''
    Generate a Minesweeper board of dimensions wxh, with num_mines mines
    '''
    mine_locations = set()
    while len(mine_locations)<num_mines:
        mine_w = random.randint(0, w-1)
        mine_h = random.randint(0, h-1)
        mine = (mine_w, mine_h)
        if mine not in mine_locations:
            mine_locations.add(mine)
    return Minesweeper(w, h, mine_locations)

class Minesweeper:

    def __init__(self, w, h, mines):
        '''
        Iniitialize board
        '''
        self.w = w
        self.h = h
        self.board = [[0 for _ in range(h)] for _ in range(w)]
        self.mask = [[False for _ in range(h)] for _ in range(w)]
        self.state = "ongoing"
        self.mines = mines.copy()
        for r,c in mines:
            self.board[r][c] = "."
            self.__increment_neighbors(r,c)

    def valid_dims(self, r, c):
        return 0<=r<self.w and 0<=c<self.h

    def get_neighbors(self, r, c):
        neighbors = set()
        for i in range(r-1, r+2):
            for j in range(c-1, c+2):
                if self.valid_dims(i, j):
                    neighbors.add((i,j))
        return neighbors

    def __increment_neighbors(self, r, c):
        '''
        Helper function to calculate the numerical value of each square
        Used in __init__
        '''
        neighbors = self.get_neighbors(r, c)
        for neighbor in neighbors:
            nr, nc = neighbor
            if isinstance(self.board[nr][nc], int):
                self.board[nr][nc] += 1

    def __reveal_squares(self, r, c):
        '''
        Helper function for uncover
        Recursively reveals squares as needed
        '''
        if self.board[r][c] != 0:
            self.mask[r][c] = True
            return

        revealed = set()
        for rr in range(r - 1, r + 2):
            for rc in range(c - 1, c + 2):
                if self.valid_dims(rr, rc):
                    if self.board[rr][rc] != '.' and self.mask[rr][rc] == False:
                        self.mask[rr][rc] = True
                        revealed.add((rr, rc))
        for rr,rc in revealed:
            if self.board[rr][rc] != "." :
                self.__reveal_squares(rr, rc)
        return


    def uncover(self, r, c):
        '''
        Equivalent to clicking on a square in real Minesweeper
        '''
        if self.state == "victory" or self.state == "defeat":
            return

        if self.board[r][c]=='.':
            self.mask[r][c] = True
            self.state  == "defeat"
            return

        if self.mask[r][c] == 'f':
            return

        self.__reveal_squares(r, c)
        bad_squares = 0
        for r in range(self.w):
            for c in range(self.h):
                if self.board[r][c] == ".":
                    if  self.mask[r][c] == True:
                        bad_squares += 1
                elif self.mask[r][c] == False:
                    bad_squares += 1
        
        if bad_squares == 0:
            self.state = "victory"

    def flag(self, r, c):
        '''
        Flag a square
        '''
        if self.state == "ongoing":
            self.mask[r][c] = "f"

    def covered(self, r, c):
        '''
        Check if a square is covered
        '''
        return not self.mask[r][c]

    def flagged(self, r, c):
        '''
        Check if a square is flagged
        '''
        return self.mask[r][c] == 'f'

    def __get_uncovered(self, r, c):
        '''
        Get the uncovered square at a certain point
        '''
        return self.board[r][c]

    def get(self, r, c):
        '''
        Get the value of a square, as a player would see it
        '''
        if self.mask[r][c] == False:
            return "*"
        elif self.mask[r][c] == "f":
            return "f"
        else:
            return self.board[r][c]

    def get_first(self):
        '''
        Pick a random square to start at, that has 0 mines around it
        Provides a reasonable starting ground for the puzzle
        '''
        while True:
            r = random.randint(0, self.w-1)
            c = random.randint(0, self.h-1)
            if self.__get_uncovered(r, c) == 0:
                return r,c

    def print(self):
        '''
        Print out all relevant information about the board status.
        '''
        print(repr(self))

    def view(self, xray=False):
        '''
        View the board as the player would see it
        '''
        print(self.state)
        nrows, ncols = self.w, self.h
        arr = [['_' if (not xray) and (self.mask[r][c]==False) 
                 else 'X' if (self.mask[r][c]=='f')
                 else ' ' if self.board[r][c] == 0 
                 else str(self.board[r][c])
                 for c in range(ncols)] for r in range(nrows)]
        print("\n".join((("%s"*len(r)) % tuple(r)) for r in arr))

    def __repr__(self):
        '''
        Show all relevant information about the board status.
        '''
        return "board: %s" % ("\n       ".join(map(str, self.board)), ) \
              +"\nmask:  %s" % ("\n       ".join(map(str, self.mask)), ) \
              +"\nstate: " + self.state