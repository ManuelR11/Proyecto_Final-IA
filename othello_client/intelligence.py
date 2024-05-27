import random


def is_valid_move(board, player, row, col):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if board[row][col] != 0:
        return False

    opponent = -player

    for direction in directions:
        dr, dc = direction
        r, c = row + dr, col + dc
        found_opponent = False

        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            r += dr
            c += dc
            found_opponent = True

        if found_opponent and 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            return True

    return False
def valid_moves(board, player):
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if is_valid_move(board, player, row, col):
                valid_moves.append((row, col))

    return valid_moves

def apply_move(board, move, player):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    new_board = [row[:] for row in board]
    r, c = move
    new_board[r][c] = player
    for dr, dc in directions:
        rr, cc = r + dr, c + dc
        to_flip = []
        while 0 <= rr < 8 and 0 <= cc < 8 and new_board[rr][cc] == -player:
            to_flip.append((rr, cc))
            rr += dr
            cc += dc
        if 0 <= rr < 8 and 0 <= cc < 8 and new_board[rr][cc] == player:
            for fr, fc in to_flip:
                new_board[fr][fc] = player
    return new_board

def evaluate_board(board, player):
    opponent = -player
    score = 0
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for r in range(8):
        for c in range(8):
            if board[r][c] == player:
                score += 1
            elif board[r][c] == opponent:
                score -= 1
    for corner in corners:
        if board[corner[0]][corner[1]] == player:
            score += 10
        elif board[corner[0]][corner[1]] == opponent:
            score -= 10
    valid_moves_player = valid_moves(board, player)
    valid_moves_opponent = valid_moves(board, opponent)
    score += len(valid_moves_player) - len(valid_moves_opponent)
    return score

def minimax(board, depth, alpha, beta, maximizing_player, player):
    valid_moves_list = valid_moves(board, player if maximizing_player else -player)
    if depth == 0 or not valid_moves_list:
        return evaluate_board(board, player), None
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in valid_moves_list:
            new_board = apply_move(board, move, player)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False, player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in valid_moves_list:
            new_board = apply_move(board, move, -player)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def AI_MOVE(board, player):
    depth = 3  # You can adjust the depth for better performance
    _, best_move = minimax(board, depth, float('-inf'), float('inf'), True, player)
    return best_move