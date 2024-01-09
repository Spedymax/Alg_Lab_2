def is_safe(board, row, col):
    for i in range(row):
        if board[i] == col or \
           board[i] - i == col - row or \
           board[i] + i == col + row:
            return False
    return True

def F1(board):
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or \
               abs(board[i] - board[j]) == j - i:
                conflicts += 1
    return conflicts

def LDFS(board, col, maxDepth, stats, preplaced):
    stats['iterations'] += 1
    if col >= len(board) or col >= maxDepth:
        stats['solutions'] += int(col >= len(board))
        return col == len(board)

    if (col, board[col]) in preplaced:
        if is_safe(board, col, board[col]):
            return LDFS(board, col + 1, maxDepth, stats, preplaced)
        else:
            return False

    for i in range(len(board)):
        if is_safe(board, col, i):
            stats['states_generated'] += 1
            board[col] = i
            stats['states_in_memory'] = max(stats['states_in_memory'], col + 1)
            if LDFS(board, col + 1, maxDepth, stats, preplaced):
                return True
            board[col] = -1
            stats['dead_ends'] += 1
    return False

def RBFS(board, col, stats, preplaced):
    stats['iterations'] += 1
    if col == len(board):
        stats['solutions'] += 1
        return board, F1(board)

    if (col, board[col]) in preplaced:
        if is_safe(board, col, board[col]):
            return RBFS(board.copy(), col + 1, stats, preplaced)
        else:
            stats['dead_ends'] += 1  # Increment dead end counter
            return None, float('inf')

    min_conflict = float('inf')
    best_board = None
    found_better_solution = False

    for i in range(len(board)):
        if is_safe(board, col, i):
            stats['states_generated'] += 1  # Increment states generated
            board[col] = i
            new_board, temp_conflict = RBFS(board.copy(), col + 1, stats, preplaced)
            stats['states_in_memory'] = max(stats['states_in_memory'], col + 1)  # Update states in memory
            if temp_conflict < min_conflict:
                min_conflict = temp_conflict
                best_board = new_board
                found_better_solution = True
            board[col] = -1

    if not found_better_solution:
        stats['dead_ends'] += 1  # Increment dead end counter if no better solution found

    return best_board, min_conflict



def solve_queens_ldfs(maxDepth, preplaced):
    board = [-1] * 8
    for row, col in preplaced:
        board[row] = col
    stats = {'iterations': 0, 'dead_ends': 0, 'states_generated': 0, 'states_in_memory': 0, 'solutions': 0}
    if LDFS(board, 0, maxDepth, stats, preplaced):
        return board, stats
    else:
        return "No solution found", stats

def solve_queens_rbfs(preplaced):
    board = [-1] * 8
    for row, col in preplaced:
        board[row] = col
    stats = {'iterations': 0, 'dead_ends': 0, 'states_generated': 0, 'states_in_memory': 0, 'solutions': 0}
    solution, _ = RBFS(board, 0, stats, preplaced)
    return solution, stats

# Testing the Algorithms with Pre-Placed Queens
preplaced_queens =  [(7, 0), (3, 3)]

print("LDFS Solution with Pre-Placed Queens:")
# LDFS Solution
ldfs_solution, ldfs_stats = solve_queens_ldfs(8, preplaced_queens)
print(ldfs_solution, ldfs_stats)
print("\nRBFS Solution with Pre-Placed Queens:")
# RBFS Solution
rbfs_solution, rbfs_stats = solve_queens_rbfs(preplaced_queens)
print(rbfs_solution, rbfs_stats)
