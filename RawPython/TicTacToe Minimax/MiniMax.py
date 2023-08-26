import random

possible_wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], # horizontal
                 [0, 3, 6], [1, 4, 7], [2, 5, 8], # vertical
                 [0, 4, 8], [2, 4, 6]]            # diagonal
player = "O"


class GameState:
    def __init__(self, to_move="X", board=[" ", " ", " ", " ", " ", " ", " ", " ", " "], label=""):
        self.to_move = to_move
        self.board = board
        self.label = label

    def __repr__(self):
        return f"{self.board[0]}|{self.board[1]}|{self.board[2]}\n{self.board[3]}|{self.board[4]}|{self.board[5]}\n{self.board[6]}|{self.board[7]}|{self.board[8]}\n"

    def get_children(self) -> list:
        children = []
        for i in range(9):
            if(self.board[i] == " "):
                new_board = self.board.copy()
                new_board[i] = self.to_move
                new_to_move = "X" if self.to_move == "O" else "O"
                children.append(GameState(new_to_move, new_board, f"{self.label}, {self.to_move}{i}"))
        return children

    def evaluate(self) -> int:
        total = 0        
        if(player == "X"):
            opponent = "O"
        else:
            opponent = "X"
        for row in possible_wins:
            count = 0
            if(self.over()):
                for row in possible_wins:
                    if(self.board[row[0]] == self.board[row[1]] == self.board[row[2]] == player):
                        return 10000
                    elif(self.board[row[0]] == self.board[row[1]] == self.board[row[2]] == opponent):
                        return -10000
                return 0
            else:
                for i in row:
                    if(self.board[i] == player):
                        count += 1
                    elif(self.board[i] == opponent):
                        count = 0
                        break
                total += count
        return total
        
    def over(self) -> bool:
        if self.board.count(" ") == 0:
            return True
        for row in possible_wins:
            if(self.board[row[0]] == self.board[row[1]] == self.board[row[2]] and self.board[row[0]] != " "):
                return True
        return False
    
    def winner(self):
        for row in possible_wins:
            if(self.board[row[0]] == self.board[row[1]] == self.board[row[2]] == "X"):
                return "Player \"X\" Wins!!!"
            if(self.board[row[0]] == self.board[row[1]] == self.board[row[2]] == "O"):
                return "Player \"O\" Wins!!!"
        return "Draw!"
    
    def play(self, square: int):
        if(self.board[square - 1] != " "):
            print("Please try a different square")
            return self.play(int(input()))
        new_board = self.board
        new_board[square - 1] = self.to_move
        new_to_move = "X" if self.to_move == "O" else "O"
        return GameState(new_to_move, new_board, f"{self.label}, {self.to_move}{square}")

def minimax(game: GameState, depth=1, max_player=True, max_depth=100000):
    move = None
    if(depth > max_depth or game.over()):
        return (game.evaluate()/depth, game)
    if(max_player):
        value = -100000
        for child in game.get_children():
            result = minimax(child, depth+1, not max_player, max_depth)
            # if depth == 1: print(f"{result[0]}\n{child}\n")
            if(result[0] > value):
                value = result[0]
                move = child
            elif(result[0]/depth == value):
                move = child if random.randint(0, 1) == 0 else move
        return (value, move)
    else:
        value = 100000
        for child in game.get_children():
            result = minimax(child, depth+1, not max_player, max_depth)
            if(result[0]/depth < value):
                value = result[0]
                move = child
            elif(result[0]/depth == value):
                move = child if random.randint(0, 1) == 0 else move
        return (value, move)



# game = GameState("X", board=["X", "O", "X", "O", "X", "O", "O", " ", " "])
game = GameState()
AITurn = False
while(True):
    if(game.over()):
        print(game)
        print(game.winner())
        break
    elif(AITurn):
        print(game)
        choice = minimax(game, max_depth=300)
        print(f"Gain: {choice[0]}")
        game = choice[1]
    else:
        print(f"Play your move \"{game.to_move}\"")
        print(game)
        game = game.play(int(input()))
    AITurn = not AITurn
    print()