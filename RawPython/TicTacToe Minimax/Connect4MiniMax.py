import random

cols, rows = (7, 6)

vectors = [[0, -1],
           [-1, 0],
           [-1, -1]]

def print_grid(grid):
    for i in grid:
        for j in i:
            if(j != " "):
                print(j, end=" ")
            else:
                print("-", end=" ")
        print()
    print()
    print("1 2 3 4 5 6 7 ")

ai = "@"
counter1 = 0
class ConnectFour:
    def __init__(self, grid=[[" "] * cols for i in range(rows)], turn="@", sequence="") -> None:
        self.grid = grid
        self.turn = turn
        self.sequence = sequence
    
    def get_children(self):
        children = []
        for i in range(cols):    
            if(self.grid[0][i] == " "):
                children.append(self.play(i + 1))
        return children
            
    def play(self, col: int):
        col = (col - 1) % 7
        if(self.grid[0][col] != " "):
            print("INVALID INPUT")
            return -1
        
        row = 0
        while(row < rows and self.grid[row][col] == " "):
            row += 1
        row -= 1
        new_grid = [self.grid[i].copy() for i in range(rows)]
        new_grid[row][col] = self.turn
        return ConnectFour(new_grid, "O" if self.turn == "@" else "@", f"{self.sequence},  {self.turn}{col}")
    
    def evaluate_grid(self):
        player_score = 0
        opponent_score = 0
        gg = False
        for i in reversed(range(rows)):
            for j in range(cols):
                if(self.grid[i][j] != " "):
                    ans = self.evaluate_cell(i, j)
                    if(ans[1]):
                        gg = True
                    if(self.grid[i][j] == ai):
                        player_score += ans[0]
                    else:
                        opponent_score += ans[0]
        return (player_score - opponent_score, gg)
        

    def evaluate_cell(self, i, j):
        player = self.grid[i][j]
        opponent = "O" if player == "@" else "@"
        score = 0
        for y in range(-1, 1):
            if((y > 0 and i > rows - 4) or (y != 0 and i < 3)): continue
            for x in range (-1, 2):
                if((x > 0 and j > cols - 4) or (x < 0 and j < 3) or (y == x and x == 0)): continue
                solution = True
                count = 1
                for n in range(1,4):
                    if(self.grid[i][j] != self.grid[i + y * n][j + x * n]):
                        solution = False
                        if(self.grid[i + y * n][j + x * n] == opponent):
                            count = 0
                        score += count * count
                        break
                if(solution):
                    score += 10000
                    return (score, True)
        return (score, False)
    
    def check_winner(self):
        for i in reversed(range(rows)):
            for j in range(cols):
                if(self.grid[i][j] != " "):
                    for y in range(-1, 1):
                        if((y > 0 and i > rows - 4) or (y != 0 and i < 3)): continue
                        for x in range (-1, 2):
                            if((x > 0 and j > cols - 4) or (x < 0 and j < 3) or (y == x and x == 0)): continue
                            solution = True
                            for n in range(1,4):
                                if(self.grid[i][j] != self.grid[i + y * n][j + x * n]):
                                    solution = False
                            if(solution):
                                return self.grid[i][j]
        return None

def minimax(game: ConnectFour, depth=1, max_player=True, max_depth=100000):
    global counter1
    counter1 += 1
    if(counter1 % 100000 == 0):
        print(counter1)
    
    move = None
    evaluation = game.evaluate_grid()
    if(depth > max_depth or evaluation[1]):
        return (evaluation[0]/depth, game, True)
    if(max_player):
        value = -1000000
        for child in game.get_children():
            result = minimax(child, depth+1, not max_player, max_depth)
            # if depth == 1: print(f"{result[0]}\n{child}\n")
            if(result[0]/depth > value):
                value = result[0]
                move = child
            elif(result[0]/depth == value):
                move = child if random.randint(0, 2) == 0 else move
        return (value, move, False)
    else:
        value = 1000000
        for child in game.get_children():
            result = minimax(child, depth+1, not max_player, max_depth)
            if(result[0]/depth < value):
                value = result[0]
                move = child
            elif(result[0]/depth == value):
                move = child if random.randint(0, 1) == 0 else move
        return (value, move, False)


game = ConnectFour()
# turns = "1223533454544"
# count = 0
# while True and count < len(turns):
#     game = game.play(5-int(turns[count]))
#     count += 1
#     print_grid(game.grid)
#     print(game.check_winner())
#     print()
#     # game = game.play(int(input()))
AITurn = True

while(True):
    if(AITurn):
        print_grid(game.grid)
        choice = minimax(game, max_depth=500)
        print(f"Gain: {choice[0]}")
        game = choice[1]
        if(choice[2]):
            print(f"Player {game.check_winner()} Wins!!!")
    else:
        print(f"Play your move \"{game.turn}\"")
        print_grid(game.grid)
        game = game.play(int(input()))
    AITurn = not AITurn
    print()