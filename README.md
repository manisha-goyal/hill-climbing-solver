
# Hill Climbing Algorithm for N-Queens and Knapsack Problems

This folder contains a Python implementation of the hill climbing algorithm designed to solve the N-Queens and Knapsack problems. The hill climber uses a heuristic approach to find solutions by iteratively moving towards states of better (higher or lower) value.

## Installation

To run this project, you will need Python 3.6 or later, and a copy of this folder to your local machine.

```bash
cd your-repository-directory
```

## Usage

### Options

- `-verbose`: Enable verbose mode to see detailed logs of the algorithm's progress (next choices being considered at each state).
- `-sideways`: Specify the number of allowed sideways moves when no improvement is found (0 by default).
- `-restarts`: Specify the number of allowed random restarts to escape local maxima (0 by default).

### N-Queens Problem

The N-Queens problem involves placing N queens on an N×N chessboard so that no two queens threaten each other. To solve the N-Queens problem using the hill climbing algorithm, run any of the following commands:

```bash
python main.py -N <number_of_queens>

python main.py -N <number_of_queens> -verbose

python main.py -N <number_of_queens> -sideways <number_of_sideways_moves>

python main.py -N <number_of_queens> -sideways <number_of_sideways_moves> -verbose

python main.py -N <number_of_queens> -sideways <number_of_sideways_moves> -restarts <number_of_restarts>

python main.py -N <number_of_queens> -sideways <number_of_sideways_moves> -restarts <number_of_restarts> -verbose

```

### Knapsack Problem 

The Knapsack problem involves selecting a set of items with given weights and values to maximize the total value without exceeding the knapsack's capacity. 

#### Input File Format
For the Knapsack problem, the input file should be in JSON format with the following structure:

```json
{
  "M": 50, // Maximum weight capacity of the knapsack (mandatory field)
  "T": 100, // Target value to achieve (mandatory field)
  "Start": ["A", "E"], // String list of items to start in the knapsackItems (empty if not specified)
  "Items": [ // An object array with item name, value and weight (mandatory field)
    {"name": "item1", "V": 60, "W": 10},
    {"name": "item2", "V": 100, "W": 20},
    ...
  ]
}
```

To solve the knapsack problem using the hill climbing algorithm, run any of the following commands:

```bash
python main.py <path_to_knapsack_input_file.json>

python main.py <path_to_knapsack_input_file.json> -verbose

python main.py <path_to_knapsack_input_file.json> -sideways <number_of_sideways_moves>

python main.py <path_to_knapsack_input_file.json> -sideways <number_of_sideways_moves> -verbose

python main.py <path_to_knapsack_input_file.json> --sideways <number_of_sideways_moves> -restarts <number_of_restarts>

python main.py <path_to_knapsack_input_file.json> --sideways <number_of_sideways_moves> -restarts <number_of_restarts> -verbose
```

## Scripts

Below are detailed descriptions of each script's functionalities.

### `nqueens.py` - N-Queens Problem Solver

This script defines the `NQueens` class, which is the state implementation designed for solving the N-Queens problem. It includes the functionalities: initialization, state generation, state evaluation, selecting the next state, goal test, restart, and state representation.

### `knapsack.py` - Knapsack Problem Solver

This script defines the `Knapsack` class, which is the state implementation designed for solving the Knapsack problem. It includes the functionalities: initialization, state generation, state evaluation, selecting the next state, goal test, restart, and state representation.

### `hillclimber.py` - Generic Hill Climbing Algorithm

Defines the `HillClimber` class, encapsulating the generic logic for performing the hill climbing search algorithm. It takes a problem instance (n-queens or knapsack) and applies the hill climbing strategy, considering optional parameters `verbose` output, `sideways` move limits, and the number of `restarts`. It manages current states, evaluates them, and decides on next states based on evaluations and the parameters provided.

### `main.py` - Main Execution Script

Serves as the entry point for running the hill climbing algorithm on specified problem instances. It integrates command-line argument parsing and triggers the appropriate problem-solving mechanism by using `argparse` to parse command-line options, including problem type (N-Queens/Knapsack), verbosity, sideways moves, and restarts. Based on the input arguments, it instantiates either the `NQueens` or `Knapsack` class and runs the hill climbing algorithm using the `HillClimber` class.

## Algorithm Walkthrough

### Hill Climbing algorithm

#### Restarts

- Restarts in the hill climbing algorithm are a strategy to escape local optima—states where no neighboring states offer an improvement in terms of the evaluation function, yet the current state is not a global optimum. The program has an optional -restarts flag, which if provided enables the given number of restarts before the algorithm terminates.

- A restart is triggered when the algorithm has explored all neighboring states without finding an improved state. This indicates that the current state may be a local optimum. On a restart, the algorithm initializes the problem with a new, random state.

#### Sideways Moves

- Sideways moves allow the algorithm to move to a neighbor state with the same evaluation as the current state, which can be useful in plateaus where improvement is not immediately possible. The program has an optional -sideways flag, which if provided enables the given number of sideways moves before the algorithm terminates or tries restarts.

- A sideways move is triggered when no neighbor improves upon the current state's evaluation, but one or more neighbors have an equal evaluation. To prevent the algorithm from wandering indefinitely on a plateau, a limit is set on the number of consecutive sideways moves allowed. 

- Again, to prevent the algorithm from wandering indefinitely on a plateau, a short-term visited states list is used. The algorithm only considers neighbors that are not in the visited states list. When the limit on sideways moves is exhausted, or a downhill move is found, the visited states list is reset.

- If the algorithm finds a valid downhill move within the allowed number of sideways moves, the sideways moves limit is reset and can be acvitated again.

### N-Queens Problem

- Initial State: The initial state for the N-Queens problem is generated by placing each queen in a unique row in its respective column, starting from the first column to the Nth column.

- Generate Neighbors: Neighbors are generated by swapping the positions of two queens on the board. For a given state, a neighbor is a new state where the position of one queen in one column is swapped with the position of another queen in a different column.

- Evaluate Neighbors: Each neighbor's state is evaluated based on the number of pairs of queens that are attacking each other, either horizontally, vertically, or diagonally. The goal is to minimize this number, with a perfect solution having zero attacking pairs.

- Choose the Next State: The next state is chosen among the neighbors based on the lowest number of attacking pairs. In case of a tie (multiple neighbors with the same, lowest number of attacking pairs), the tie-breaker chooses the neighbor that involves the least movement (i.e., the swap of queens that results in the smallest change in their positions).

- Random Restart: This involves generating a new, random initial state for when the hill climbing algorithm may perform a random restart. A random state is generated such that each queen is in its own row and column.

### Knapsack Problem

- Initial State: The initial state for the Knapsack problem involves reading the problem definition from a JSON file, which specifies an initial selection of items. If an initial selection is not provided, the algorithm will start with an empty knapsack.

- Generate Neighbors: Neighbors are generated by either adding an item not currently in the knapsack, removing an item that is currently in the knapsack, or swapping an item in the knapsack with one not in the knapsack.

- Evaluate Neighbors: Each neighbor's state is evaluated based on the total value of the items in the knapsack while ensuring the total weight does not exceed the knapsack's capacity. The The goal is to maximize the total value.

- Choose the Next State: The next state is chosen among the neighbors with the highest total value that still fits within the knapsack's weight limit. In case of a tie (multiple neighbors with the same total value), the tie-breaker selects the state with the higher value and lower total weight to maximize space efficiency.

- Random Restart: This involves generating a new, random initial state for when the hill climbing algorithm may perform a random restart. A random state is generated by randomly selecting a new set of items.
