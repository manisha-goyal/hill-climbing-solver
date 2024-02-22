import random

class NQueens:
    def __init__(self, N):
        self.N = N

    def initial_state(self):
        return [i for i in range(self.N)]

    def generate_neighbors(self, state):
        neighbors = []
        for i in range(self.N):
            for j in range(i + 1, self.N):
                new_state = state[:]
                new_state[i], new_state[j] = new_state[j], new_state[i]
                neighbors.append(new_state)
        return neighbors
    
    def evaluate_state(self, state):
        attacking_pairs = 0
        for i in range(self.N):
            for j in range(i+1, self.N):
                if state[i] == state[j] or abs(state[i] - state[j]) == abs(j - i):
                    attacking_pairs += 1
        return attacking_pairs
    
    def choose_next_state(self, current_state, neighbors):
        evaluated_neighbors = [(neighbor, self.evaluate_state(neighbor)) for neighbor in neighbors]
        evaluated_neighbors.sort(key=lambda x: x[1])
        best_score = evaluated_neighbors[0][1]
        best_neighbors = [n for n, score in evaluated_neighbors if score == best_score]
        
        if len(best_neighbors) == 1:
            next_state = best_neighbors[0]
        else:
            # For tie-breakers, choose the neighbor with the lowest number of rows being swapped
            swaps_count = [(neighbor, sum(1 for i in range(self.N) if neighbor[i] != current_state[i])) for neighbor in best_neighbors]
            min_swaps = min(swaps_count, key=lambda x: x[1])
            next_state = min_swaps[0]
            
        return next_state

    def goal_test(self, state):
        return self.evaluate_state(state) == 0

    def restart(self):
        return random.sample(range(self.N), self.N)
    
    def state_representation(self, state):
        return str(state)