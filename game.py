import os
import random
from collections import deque

class Game:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(2):
            x, y = self.random_coordinate()
            self.populate_board(x, y)
        #self.draw_board()
        self.game_over = False
        self.score = 0
        self.won = False

    def random_number(self):
        return random.choice([2, 4])

    def random_coordinate(self):
        x, y = random.randint(0, 3), random.randint(0, 3)
        return x, y
    
    def populate_board(self, x, y):
        while self.board[y][x] != 0:
            x, y = self.random_coordinate()
        self.board[y][x] = self.random_number()        

    def draw_board(self):
        os.system('clear')  # Clear the terminal screen
        
        # Draw the board
        for row in self.board:
            print('|'.join(str(cell).rjust(4) if cell != 0 else ' ' * 4 for cell in row))
            print('-' * 21)
    
    def update(self):
        x, y = self.random_coordinate()
        self.populate_board(x, y)
        #self.draw_board()
    
    def move(self,queue):
        new_row = []
        while queue:
            while queue and queue[0] == 0:
                queue.popleft()
            if queue:  # Check if the queue is not empty
                first = queue.popleft()
            else:
                break  # Exit the loop if the queue is empty
            while queue and queue[0] == 0:
                queue.popleft()
            
            if queue and first == queue[0]:
                new_row.append(first * 2)
                self.score += first * 2
                #check if won
                if first * 2 == 2048: 
                    self.won = True
                    self.game_over = True
                queue.popleft()  
            else:
                new_row.append(first)
        
        # Populate the rest of the new row with zeros
        new_row += [0] * (4 - len(new_row))
        return new_row

    def left(self):
        change = False
        for i in range(4):
            queue = deque(self.board[i])
            
            new_row = self.move(queue)
            
            #check for change 
            if new_row != self.board[i]: change = True

            # Update the current row with the modified new_row
            self.board[i] = new_row

        if change: self.update()
        else: self.game_over = self.is_game_over()

    def right(self):
        change = False
        for i in range(4):
            queue = deque(self.board[i][::-1])

            new_row = self.move(queue)
            
            #check for change
            if new_row != self.board[i][::-1]: change = True

            # Update the current row with the modified new_row
            self.board[i] = new_row[::-1 ]
        if change: self.update()
        else: self.game_over = self.is_game_over()

    def top(self):
        # Transpose the board
        self.board = [[self.board[j][i] for j in range(4)] for i in range(4)]
        # Use left() logic
        self.left()
        # Transpose back the board
        self.board = [[self.board[j][i] for j in range(4)] for i in range(4)]
        #self.draw_board()

    def bottom(self):
        # Transpose the board
        self.board = [[self.board[j][i] for j in range(4)] for i in range(4)]
        # Use right() logic
        self.right()
        # Transpose back the board
        self.board = [[self.board[j][i] for j in range(4)] for i in range(4)]
        #self.draw_board()


    def is_game_over(self):
        # Check if there are any empty cells
        if any(0 in row for row in self.board):
            return False
        
        # Check if adjacent cells have the same value
        for y in range(4):
            for x in range(4):
                if x < 3 and self.board[y][x] == self.board[y][x + 1]:
                    return False
                if y < 3 and self.board[y][x] == self.board[y + 1][x]:
                    return False
        
        return True