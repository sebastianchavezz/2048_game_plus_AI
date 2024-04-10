import random
from game import Game
from typing import List
from enum import Enum
from collections import Counter
import pickle

class Move(Enum):
    LEFT = 0
    RIGHT = 1
    TOP = 2
    BOT = 3

class Agent:

    def __init__(self, initial_board:List[List[int]] , eps:float, eps_decay:float, min_eps:float ):
        self.eps = eps
        self.eps_decay = eps_decay
        self.min_eps = min_eps
        # previous board
        #previous board
        self.board = initial_board
        self.prev_score = 0
        #keep track on how many big boys are in the board
        self.big_scores_counters = {16:0,32:0,64:0,128:0,256: 0, 512: 0, 1024:0 , 2048:0}
        #Q table
        self.q_table = {}
        

    def reset(self, board):
        self.board = board
        self.prev_score = 0
        #keep track on how many big boys are in the board
        self.big_scores_counters = {16:0,32:0,64:0,128:0,256: 0, 512: 0, 1024:0 , 2048:0}


    def flatten_board(self, board: List[List[int]]):
        return [cell for row in board for cell in row]


    def _encode(self, board: List[int]):
        #encode to bit representation
        bit_representation = 0
        for i, cell in enumerate(board):
            if cell != 0: bit_representation |= (1 << i)
        return bit_representation

    def get_state(self):
        flattened_board = self.flatten_board(self.board)
        encoded_stat = self._encode(flattened_board)
        return encoded_stat

    def _get_achievements_score(self, new_board: List[int]):
        # Initialize a dictionary to count occurrences of each score
        counter = {16:0,32:0,64:0,128:0,256: 0, 512: 0, 1024:0 , 2048:0}

        # Count occurrences of each score in the new board
        for cell in new_board:
            if cell in counter:
                counter[cell] += 1

        score = 0
        # Check if any of the counters exceed the previous count
        for key, value in counter.items():
            if value > self.big_scores_counters[key]:
                # Update the counter and calculate the score
                self.big_scores_counters[key] = value
                score += key * 4 if key >= 128 else key  

        return score

    def get_reward(self, new_board: List[List[int]], new_points:int, is_game_over:bool):
        total_score = 0
        flat_board =  self.flatten_board(new_board)
        # the more 0's the greater the reward
        merge_reward_counter = Counter(flat_board)
        #count how many 0's there are
        total_score += merge_reward_counter[0] if merge_reward_counter[0] > 8 else -100
        #check delta amount
        total_score += (new_points - self.prev_score)
        #add Achivement Rewards
        total_score += self._get_achievements_score(flat_board)

        if is_game_over: total_score -= 20000

        return total_score
    
    def get_action(self, state):
        if random.random() < self.eps:
            # Exploration: Choose a random action
            action = random.choice([Move.LEFT, Move.RIGHT, Move.TOP, Move.BOT])
        else:
            # Exploitation: Choose the action with the highest Q-value
            if state in self.q_table:
                action = max(self.q_table[state], key=self.q_table[state].get)
            else:
                # If the state is not in the Q-table, choose a random action
                action = random.choice([Move.LEFT, Move.RIGHT, Move.TOP, Move.BOT])
        return action

    def update_epsilon(self):
        self.eps = max(self.min_eps, self.eps * self.eps_decay)
    
    def updateQValue(self, state, action, reward, next_state, alpha, gamma):
        if state not in self.q_table:
            self.q_table[state] = {action: random.random() for action in [Move.BOT, Move.TOP, Move.LEFT, Move.RIGHT]}
        elif action not in self.q_table[state]:
            self.q_table[state][action] = random.random()

        if next_state not in self.q_table:
            self.q_table[next_state] = {action: random.random() for action in [Move.BOT, Move.TOP, Move.LEFT, Move.RIGHT]}

        #The Q value update
        max_next_q = max(self.q_table[next_state].values()) if next_state in self.q_table else 0
        td_target = reward + gamma * max_next_q
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += alpha * td_error
        

    def save_q_table(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, file_path):
        with open(file_path, 'rb') as f:
            self.q_table = pickle.load(f)