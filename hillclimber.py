class HillClimber:
    def hill_climber(self, problem, verbose=False, sideways=0, restarts=0):
        try:
            restart_count = 0

            while restart_count <= restarts:
                current_state = problem.restart() if restart_count > 0 else problem.initial_state()
                current_value = problem.evaluate_state(current_state)
                sideways_count = 0
                visited_states = set()

                if restart_count == 0:
                    print(f"Start: {problem.state_representation(current_state)} = {current_value}")  
                else:
                    print(f"restarting with: {problem.state_representation(current_state)} = {current_value}")
                
                while True:
                    neighbors = problem.generate_neighbors(current_state)
                    if sideways_count > 0:
                        neighbors = [n for n in neighbors if tuple(n) not in visited_states]

                    if not neighbors:
                        break

                    if verbose:
                        for neighbor in neighbors:
                            print(f"{problem.state_representation(neighbor)} = {problem.evaluate_state(neighbor)}")

                    next_state = problem.choose_next_state(current_state, neighbors)
                    next_value = problem.evaluate_state(next_state)

                    if next_value < current_value:
                        current_state = next_state
                        current_value = next_value
                        sideways_count = 0
                        visited_states = set()
                        print(f"choose {problem.state_representation(current_state)} = {current_value}")
                    elif next_value == current_value and sideways_count < sideways:
                        current_state = next_state
                        current_value = next_value
                        sideways_count += 1
                        visited_states.add(tuple(current_state))
                        print(f"choose(sideways): {problem.state_representation(current_state)} = {current_value}")
                    else:
                        if sideways_count >= sideways:
                            break

                    if problem.goal_test(current_state):
                        print(f"Goal: {problem.state_representation(current_state)} = {current_value}")
                        return

                restart_count += 1

            print("not found")
            
        except Exception as e:
            print(f"Error during hill climbing: {e}")
            return None