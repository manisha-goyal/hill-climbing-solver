import random
import json

class Knapsack:
    def __init__(self, filepath):
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
                
                if 'M' not in data or 'T' not in data or 'Items' not in data:
                    missing_keys = [key for key in ['M', 'T', 'Items'] if key not in data]
                    raise KeyError(f"Missing data: {', '.join(missing_keys)}")
                
                self.M = data['M']
                self.T = data['T']
                self.items = {item['name']: (item['V'], item['W']) for item in data['Items']}
                self.start = data.get('Start', [])
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error in knapsack input file: {e}")
            exit(1)

        self.initial_state()

    def initial_state(self):
        state = [False] * len(self.items)
        if self.start:
            for i, item in enumerate(self.items):
                if item in self.start:
                    state[i] = True
        return state

    def generate_neighbors(self, state):
        neighbors = []
        n = len(self.items)

        for i in range(n):
            new_state = state[:]
            new_state[i] = not new_state[i]
            neighbors.append(new_state)

        for i in range(n):
            if state[i]:
                for j in range(n):
                    if not state[j]:
                        swap_state = state[:]
                        swap_state[i] = False
                        swap_state[j] = True
                        if swap_state not in neighbors:
                            neighbors.append(swap_state)

        neighbors.sort(key=lambda x: sum(x))
        return neighbors
    
    def evaluate_state(self, state):
        total_value = 0
        total_weight = 0
        
        for i, (name, (value, weight)) in enumerate(self.items.items()):
            if state[i]:
                total_value += value
                total_weight += weight
        
        error_value = max(0, self.T - total_value) + max(0, total_weight - self.M)
        return error_value
    
    def choose_next_state(self, current_state, neighbors):
        best_neighbors = [neighbor for neighbor in neighbors if self.evaluate_state(neighbor) == min(self.evaluate_state(n) for n in neighbors)]
        
        if len(best_neighbors) == 1:
            next_state = best_neighbors[0]
        else: 
            # For tie-breakers, choose the neighbor with the higher value and lower weight
            evaluated_ties = [(n, sum(self.items[item][0] for i, item in enumerate(self.items) if n[i]), 
                            sum(self.items[item][1] for i, item in enumerate(self.items) if n[i])) for n in best_neighbors]
            next_state = sorted(evaluated_ties, key=lambda x: (-x[1], x[2]))[0][0]
        
        return next_state

    def goal_test(self, state):
        return self.evaluate_state(state) == 0

    def restart(self):
        return [random.choice([True, False]) for _ in self.items]
    
    def state_representation(self, state):
        included_items = [name for i, (name, _) in enumerate(self.items.items()) if state[i]]
        return f"[{' '.join(included_items)}]"