using System;
using System.Collections.Generic;

namespace tic_tac_toe
{
    class Program
    {
        // Outputs to the console the given tic-tac-toe 'grid' string in a recognisable format.
        static string GridString(string[,] grid)
        {
            return "#############\n" +
                "#   |   |   #\n" +
                "# " + grid[0, 0] + " | " + grid[0, 1] + " | " + grid[0, 2] + " #\n" +
                "#___|___|___#\n" +
                "#   |   |   #\n" +
                "# " + grid[1, 0] + " | " + grid[1, 1] + " | " + grid[1, 2] + " #\n" +
                "#___|___|___#\n" +
                "#   |   |   #\n" +
                "# " + grid[2, 0] + " | " + grid[2, 1] + " | " + grid[2, 2] + " #\n" +
                "#   |   |   #\n" +
                "#############\n";
        }

        static string HelpGrid()
        {
            return "-----------" +
                "|   |   |   |\n" +
                "| 0 | 1 | 2 |\n" +
                "|___|___|___|\n" +
                "|   |   |   |\n" +
                "| 3 | 4 | 5 |\n" +
                "|___|___|___|\n" +
                "|   |   |   |\n" +
                "| 6 | 7 | 8 |\n" +
                "|   |   |   |\n" +
                "-----------\n";
        }

        // Gets valid input for move coordinates from user.
        // Returns them as two integers, x and y.
        static (int, int) PlayerMove(string[,] grid)
        {
            bool val = false;
            int square_num = 0;
            int x = 0;
            int y = 0;
            while (val == false)
            {
                Console.Write("Square to place in:  ");
                string inp = Console.ReadLine();
                if (inp.ToLower() == "h" | inp.ToLower() == "help")
                {
                    Console.WriteLine(HelpGrid());
                }
                else
                {
                    bool is_num = int.TryParse(inp, out square_num);
                    if (is_num && square_num <= 9 && square_num >= 1)
                    {
                        val = true;
                    }
                    else
                    {
                        Console.WriteLine("{0} is not a valid input (must be 1 to 9 - type 'h' for help)", inp);
                    }
                }
            }
            square_num--;
            x = square_num / 3;
            y = square_num % 3;
            return (x, y);

        }
        // Will return a random pair of array indeces for empty squares on the grid.
        static (int, int) CompMove(string[,] grid)
        {
            List<List<int>> empties = new List<List<int>>();
            Random rand = new Random();
            for (int i = 0; i < 3; i++)
            {
                for (int j = 0; j < 3; j++)
                {
                    if (grid[i, j] == " ")
                    {
                        List<int> empt = new List<int>();
                        empt.Add(i);
                        empt.Add(j);
                        empties.Add(empt);
                    }
                }
            }
            Console.WriteLine("empties = {0}", empties.ToArray());
            int rand_choice = rand.Next(0, empties.Count);
            return (empties[rand_choice][1], empties[rand_choice][1]);

        }
        // Return true if the given move resulted in a three-in-a-row, by checking along the horizontal, vertical and diagonal lines it fell under.
        // (Note that a move into the middle square would be checked along both diagonals (x is y and the both add up to 2).
        static bool IsThreeInRow(string[,] grid, int x, int y, string turn)
        {
            // Along horizontal
            if (grid[y,0] == turn && grid[y,1] == turn && grid[y,2] == turn)
            {
                return true;
            }
            Console.WriteLine("TIR: Not vertical");
            // Along vertical
            if (grid[0,x] == turn && grid[1,x] == turn && grid[2,x] == turn)
            {
                return true;
            }
            Console.WriteLine("TIR: Not horizontal");
            // Along diagonal
            if (x == y)
            {
                // If last move was in the diagonal from top-left to bottom-right
                if (grid[0,0] == turn && grid[1,1] == turn && grid[2,2] == turn)
                {
                    return true;
                }
                
            }
            Console.WriteLine("TIR: Not diagonal X");
            if (x + y == 2)
            {
                // If last move was in the diagonal from top-right to bottom-left
                if (grid[0, 2] == turn && grid[1, 1] == turn && grid[2, 0] == turn)
                {
                    return true;
                }
            }
            Console.WriteLine("TIR: Not diagonal Y");
            return false;

        }
        // Returns the string for the other player based on the player string you gave it.
        static string GetOther(string player)
        {
            if (player == "X")
            {
                return "O";
            }
            else if (player == "O")
            {
                return "X";
            }
            else
            {
                return "?";
            }
        }

        // bool 'gover' is whether the game is finished or not; string 'winner' is the victor, or "-" if there isn't one.
        // string 'turn' represents the player to go next; int 'moves' is the number of moves taken in the game total.
        // Note that X is the human player, O is the computer.
        static (string, string[,]) GameVComputer()
        {
            // Initialise game values
            string[,] grid = new string[3, 3] {{ " ", " ", " " }, { " ", " ", " " }, { " ", " ", " " } };
            bool gover = false;
            string winner = "-";
            string turn = "X";
            int moves = 0;
            while (gover == false)
            {
                Console.WriteLine(GridString(grid));
                if (turn == "X")
                {
                    Console.WriteLine("\nYour move.");
                    (int ind_x, int ind_y) = PlayerMove(grid);
                    grid[ind_x, ind_y] = "X";
                    gover = IsThreeInRow(grid, ind_x, ind_y, turn);
                    if (gover)
                    {
                        winner = turn;
                        Console.WriteLine(GridString(grid));
                    }
                }
                else
                {
                    Console.WriteLine("Opponent's move");
                    (int ind_x, int ind_y) = CompMove(grid);
                    grid[ind_x, ind_y] = "O";
                    gover = IsThreeInRow(grid, ind_x, ind_y, turn);
                    if (gover)
                    {
                        winner = turn;
                        Console.WriteLine(GridString(grid));
                    }
                }
                moves++;
                turn = GetOther(turn);
                if (moves == 9)
                {
                    gover = true;
                    Console.WriteLine(GridString(grid));
                }
            }
            return (winner, grid);
        }
        static void Main(string[] args)
        {
            (string winner, string[,] grid) =GameVComputer();
            if (winner == "X")
            {
                Console.WriteLine("\nYou win!\n");
            }
            else if (winner == "O")
            {
                Console.WriteLine("\nOpponent wins.\n");
            }
            else
            {
                Console.WriteLine("\nIt's a draw!\n");
            }
            Console.WriteLine(GridString(grid));
        }
    }
}
