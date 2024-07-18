
def flip_x(board: int) -> int:
    """
    Mirror bitboard across x-axis

    :param board: bitboard
    :return: transformed bitboard
    """
    return (
       ((board >> 54)) |
       ((board >> 36) & 0b000000000000000000000000000000000000000000000000111000000000000) |
       ((board >> 18) & 0b000000000000000000000000000000000000011111110000000000000000000) |
       ((board)       & 0b000000000000000000000000000011111110000000000000000000000000000) |
       ((board << 18) & 0b000000000000000000111111110000000000000000000000000000000000000) |
       ((board << 36) & 0b000000000000111000000000000000000000000000000000000000000000000) |
       ((board << 54))
    )

def flip_y(board: int) -> int:
    """
    Mirror bitboard across y-axis

    :param board: bitboard
    :return: transformed bitboard
    """
    return (
        ((board >> 6) & 0b000000000000000000000000010000000010000000010000000000000000000) |
        ((board >> 4) & 0b000000000000000000000000100000000100000000100000000000000000000) |
        ((board >> 2) & 0b000001000000001000000001000000001000000001000000001000000001000) |
        ((board)      & 0b000010000000010000000010000000010000000010000000010000000010000) |
        ((board << 2) & 0b000100000000100000000100000000100000000100000000100000000100000) |
        ((board << 4) & 0b000000000000000000001000000001000000001000000000000000000000000) |
        ((board << 6) & 0b000000000000000000010000000010000000010000000000000000000000000)
    )