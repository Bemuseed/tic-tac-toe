class Game:
    def __init__(self):
        self._grid = [[" "," "," "],[" "," "," "],[" "," "," "]]
        self._placed = 0
        self._turn = "O"
        self._state = "_"
        self.error_dict = {1:"Invalid coordinate/indexes",
                           3:"Invalid character argument (must be X or O)",
                           4:"Action attempted on wrong player turn",
                           5:"Game is over",
                           6:"Invalid argument type",
                           7:"Index is too low",
                           8:"Index is too high",
                           9:"Attempted move on occupied square"}

    def err_string(self, num, e=False):
        if e == False:
            return self.error_dict[num]
        else:
            return "Error: "+ self.error_dict[num]
                           

    # Prevent (as best we can) cheating!
    @property
    def grid(self):
        return self._grid
    @property
    def placed(self):
        return self._placed
    @property
    def turn(self):
        return self._turn
    @property
    def state(self):
        return self._state

    def coord_to_ind(self, coord:str):
        if len(coord) != 2:
            return [], 1
        coord = coord.upper()
        ind = []
        if coord[1] == "1":
            ind.append(0)
        elif coord[1] == "2":
            ind.append(1)
        elif coord[1] == "3":
            ind.append(2)
        else:
            return [], 1
        if coord[0] == "A":
            ind.append(0)
        elif coord[0] == "B":
            ind.append(1)
        elif coord[0] == "C":
            ind.append(2)
        else:
            return [], 1
        return ind

    def ind_to_coord(self, ind:list):
        if len(ind) != 2:
            return "_", 1
        coord = ""
        if ind[1] == 0:
            coord += "A"
        elif ind[1] == 1:
            coord += "B"
        elif ind[1] == 2:
            coord += "C"
        else:
            return "_", 1
        if ind[0] == 0:
            coord += "1"
        elif ind[0] == 1:
            coord += "2"
        elif ind[0] == 2:
            coord += "3"
        else:
            return "_", 1
        return coord

    def valid_coord(self, coord):
        if type(coord) != type(""):
            return False
        if len(coord) != 2:
            return False
        for i in "ABC":
            if coord[0] == i:
                for x in "123":
                    if coord[1] == x:
                        return True
        return False

    def valid_inds(self, inds):
        if type(inds) != type([]):
            return False
        if len(inds) != 2:
            return False
        for i in [0,1,2]:
            if inds[0] == i:
                for x in [0,1,2]:
                          if inds[1] == x:
                              return True
        return False
    
    def update_state(self):
        # Checks if it's already over
        if self._state != "_":
            pass
        else:
            # Checks if it's too early for a win
            if self._placed < 5:
                return "_"
            else:
                # Checks the rows of the grid
                for r in self.grid:
                    content = "";
                    for i in r:
                        content += i;
                    if content == "XXX":
                        self._state =  "X";
                        return "X"
                    elif content == "OOO":
                        self._state = "O"
                        return "O"

                # Checks the columns of the grid
                for i in range(0, 2):
                    content = "";
                    for r in self.grid:
                        content += r[i];
                    if content == "XXX":
                        self._state = "X"
                        return "X"
                    elif content == "OOO":
                        self._state = "O"
                        return "O"

                # Checks the diagonal of the grid
                content = ""
                content += self.grid[0][0] + self.grid[1][1] + self.grid[2][2]
                if content == "XXX":
                    self._state = "X"
                    return "X"
                elif content == "OOO":
                    self._state = "O"
                    return "O"
                content = "";
                content += self.grid[0][2] + self.grid[1][1] + self.grid[2][0]
                if content == "XXX":
                    self._state = "X"
                    return "X"
                elif content == "OOO":
                    self._state = "O"
                    return "O"

                else:
                    # If there are no three-in-a-rows anywhere
                    if self._placed == 9:
                        self._state = "XO"
                        return "XO"
                    else:
                        self._state = "_"

    def is_turn(self, char):
        if self._state != "_":
            return False, 5
        else:
            if char != "X" and char != "O":
                return False, 3
            else:
                if self._turn == char:
                    return True, ""
                else:
                    return False, 4

    def valid_pos(self, r, c):
        for i in r, c:
            if type(i) != type(1):
                return 6
            else:
                if i < 0:
                    return 7
                else:
                    if i > 2:
                        return 8
        return True
    
    def get_content(self, r, c):
        val = self.valid_pos(r, c)
        if val == True:
            return True, self.grid[r][c]
        else:
            return False, val

    """Function for determining legality.
    Input is two integers for position, and the character to be placed.
    Determines if it is [let]'s turn through is_turn, and if the position is valid through valid_pos.
    Returns a boolean and an error string"""
    def legal_move(self, r:int, c:int, let:str):
        tern, err = self.is_turn(let)
        if tern == False:
            return tern, err
        else:
            val, cont = self.get_content(r, c)
            if val:
                if cont == " ":
                    return True, ""
                else:
                    return False, 9
            else:
                return False, cont
    
    """Function for placing a character on the grid.
    Input is an integer for the first index (row), and an integer for the second (column)
    Determines legality through the legal_move function.
    Uses update_state to update the _state of play after a successful move,
    and if the game is not over, sets self._turn to the next player make a move.
    Returns a boolean, True or False for success or failure,
    and a string, either the player to go next/game state, or an error"""
    def place(self, move, char, coord = True):
        # Handles move variable
        if self.valid_coord(move) == True:
            move = self.coord_to_ind(move)
        if self.valid_inds(move) == False:
            return False, 1
        r = move[0]
        c = move[1]
        # Checks move legality
        is_leg, err = self.legal_move(r, c, char)
        if is_leg == True:
            self._grid[r][c] = char
            # Adds to the placed counter
            self._placed += 1
            # Updates the game _state
            self.update_state()
            if self._state == "_":
                # Changes the player to move next if the game is not done
                if self._turn == "X":
                    self._turn = "O"
                    return True, "It is O's turn"
                elif self._turn == "O":
                    self._turn = "X"
                    return True, "It is X's turn"
            else:
                # Re_turns True and the game _state
                if self._state == "XO":
                    return True, "It's a draw!"
                else:
                    return True, self._state + " has won!"
        else:
            return False, err
        
                
