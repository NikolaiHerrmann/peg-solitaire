
import random
from queue import Queue, LifoQueue
from flips import flip_x, flip_y


START_POSITION = 0b000111000000111000011111110011101110011111110000111000000111000
END_POSITION   = 0b000000000000000000000000000000010000000000000000000000000000000
LEGAL_PEGS = START_POSITION | END_POSITION


def print_board(board: int) -> None:
    """
    Print bitboard

    :param board: Bitboard
    """
    idx = 62
    while idx >= 0:
        bit_idx = 1 << idx
        if bit_idx & LEGAL_PEGS:
            print("1" if board & bit_idx else "0", end="")
        else:
            print(" ", end="")
        if idx % 9 == 0:
            print()  # newline
        idx -= 1
    print()


def in_bounds(idx: int) -> bool:
    """
    Check if index is a valid peg on the board

    :param idx: Bitboard index
    :return: True if index is in bounds of board else False
    """
    return idx >= 0 and idx < 63 and ((1 << idx) & LEGAL_PEGS)


def generate_moves() -> list[tuple[int, int]]:
    """
    Generates all 76 possible peg moves

    A move is defined as a tuple. First element gives a mask of the three cells
    involved in a move. Second element gives a mask of the pegs that need to be 
    on the board to make the move.

    :return: List of possible moves
    """
    moves = []
    possible_directions = [1, -1, 9, -9]  # left, right, up, down

    for idx in range(63):
        if ((1 << idx) & LEGAL_PEGS) == 0:
            continue

        for direction in possible_directions:
            second_idx = idx + direction
            third_idx = second_idx + direction

            if in_bounds(second_idx) and in_bounds(third_idx):
                peg_positions = (1 << idx) | (1 << second_idx)
                moves.append((peg_positions | (1 << third_idx), peg_positions))

    return moves


def solve(start_board: int, all_possible_moves: list[tuple[int, int]],
          instructions: dict[int, int]) -> bool:
    """
    Finds a solution for peg solitaire using either depth first search or 
    breadth first search

    :param start_board: Initial starting position
    :param all_possible_moves: List of all possible moves that a player can make
    :param instructions: Dictionary that keeps track which positions have been
                         visited (key) and the corresponding previous 
                         positions (values)
    :return: True if a solution was found else False
    """
    container = LifoQueue()  # can also try Queue()
    container.put(start_board)

    while not container.empty():
        board = container.get()
        if board == END_POSITION:
            return True

        for move in all_possible_moves:
            if board & move[0] == move[1]:  # is this move legal?
                new_board = board ^ move[0]  # make move
                if new_board in instructions:  # have we seen this board before?
                    continue
                container.put(new_board)
                # add to visited list (and needed for backtracking)
                instructions[new_board] = board

                # Not sure if this helps, seems to slow down the system

                # new_board_x_flip = flip_x(new_board)
                # if new_board_x_flip not in instructions:
                #     instructions[new_board_x_flip] = None

                # new_board_y_flip = flip_y(new_board)
                # if new_board_y_flip not in instructions:
                #     instructions[new_board_y_flip] = None

    return False


def print_solution(instructions: dict[int, int]) -> None:
    """
    Print the steps to solve the puzzle using the :func:`print_board` function

    :param instructions: Dictionary holding all visited states. We can use this
                         to backtrack from :param:`END_POSITION` to 
                         :param:`START_POSITION`
    """
    board = END_POSITION
    board_list = [END_POSITION]

    while board != START_POSITION:
        board = instructions[board]
        board_list.append(board)

    [print_board(board) for board in reversed(board_list)]


if __name__ == "__main__":
    moves = generate_moves()

    # Different seeds can speed or slow down the search
    # random.seed(44)
    # random.shuffle(moves)

    instructions = {}
    solve(START_POSITION, moves, instructions)

    print_solution(instructions)
