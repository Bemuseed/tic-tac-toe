import tic_model

class View:
    def print_grid(self, grid:list):
        gridstr = "   |   |   \n "+grid[0][0]+" | "+grid[0][1]+" | "+grid[0][2]+" \n___|___|___\n   |   |   \n "+grid[1][0]+" | "+grid[1][1]+" | "+grid[1][2]+" \n___|___|___\n   |   |   \n "+grid[2][0]+" | "+grid[2][1]+" | "+grid[2][2]+" \n   |   |   \n"
        print(gridstr)
    def inform_turn(self, pchar):
        print("It is "+pchar+"'s turn")
    def prompt_move(self):
        move = input("Enter move:  ")
        return move
    def open(self):
        print("Welcome to GrahmWare's Tic-Tac-Toe player!\n")
        print("   |   |   \n   |   |   \n___|___|___\n   |   |   \n   |   |   \n___|___|___\n   |   |   \n   |   |   \n")

class Controller:
    def __init__(self):
        self.model = tic_model.Game()
        self.view = View()
        self.over = False
    def to_ind(self, coord):
        return self.model.coord_to_ind(inp)
    def play(self):
        self.view.open()
        while self.over == False:
            got_move = False
            while got_move == False:
                inp = self.view.prompt_move()
                success, ret = self.model.place(inp, self.model.turn)
                if success:
                    got_move = True
                else:
                    print("Invalid move!")
                
            if self.model.state != "_":
                self.over = True
            self.view.print_grid(self.model.grid)
            print(ret)

def main():
    c = Controller()
    c.play()
    
main()
