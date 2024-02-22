import argparse
from knapsack import Knapsack
from nqueens import NQueens
from hillclimber import HillClimber
from sys import exit

def int_type_positive(value):
    try:
        ivalue = int(value)
        if ivalue < 0:
            raise argparse.ArgumentTypeError(f"{value} is not a valid positive integer")
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a valid integer")

def main():
    parser = argparse.ArgumentParser(description="Hill Climbing Algorithm")
    parser.add_argument("-N", type=int_type_positive, help="Number of queens for the N-Queens problem")
    parser.add_argument("knapsack_file", nargs='?', type=str, help="Path to the knapsack input file")
    parser.add_argument("-verbose", action='store_true', help="Enable verbose mode")
    parser.add_argument("-sideways", type=int_type_positive, default=0, help="Number of allowed sideways motions")
    parser.add_argument("-restarts", type=int_type_positive, default=0, help="Number of allowed random restarts")
    args = parser.parse_args()

    if args.N:
        problem = NQueens(args.N)
    elif args.knapsack_file:
        try:
            problem = Knapsack(args.knapsack_file)
        except Exception as e:
            print(f"Error loading knapsack input file: {e}")
            exit(1)
    else:
        print("Error: Please specify either -N for N-Queens or a path to a input file for Knapsack.")
        exit(1)

    hillclimber = HillClimber()
    hillclimber.hill_climber(problem, verbose=args.verbose, sideways=args.sideways, restarts=args.restarts)

if __name__ == "__main__":
    main()