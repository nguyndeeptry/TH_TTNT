import numpy as np

def is_valid_state(state, num_queens):
    return len(state) == num_queens

def get_candidates(state, num_queens):
    if not state: return range(num_queens)
    position = len(state)
    candidates = set(range(num_queens))
    for row, col in enumerate(state):
        candidates.discard(col)
        dist = position - row
        candidates.discard(col + dist)
        candidates.discard(col - dist)
    return candidates

def search(state, solutions, num_queens):
    if is_valid_state(state, num_queens):
        solutions.append(state.copy())
    for candidate in get_candidates(state, num_queens):
        state.append(candidate)
        search(state, solutions, num_queens)
        state.remove(candidate)

def solve(num_queens):
    solutions = []
    state = []
    search(state, solutions, num_queens)
    return solutions

if __name__ == "__main__":
    num_queens = 8
    solutions = solve(num_queens)
    print("Tổng số giải pháp là:", len(solutions))
    for solution in solutions[:5]:  # In thử 5 giải pháp đầu
        board = np.full((num_queens, num_queens), "-")
        for row, col in enumerate(solution):
            board[row][col] = "Q"
        print(f"\nSolution: {solution}")
        print(board)
