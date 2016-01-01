import random


def update_squares(squares, move):
    to_remove = []
    for sq in squares:
        try:
            sq.remove(move)
            if len(sq) == 0:
                to_remove.append(sq)
        except KeyError:
            pass

    for sq in to_remove:
        squares.remove(sq)

if __name__ == "__main__":
    try:
        setup = input().strip().split(':')
        size = int(setup[0])
        whoami = int(setup[1])
        moves = set(('V', i, j) for i in range(size) for j in range(size + 1))
        moves |= set(('H', j, i) for i in range(size) for j in range(size + 1))
        squares = [set([('V', i, j), ('H', i, j), ('H', i+1, j), ('V', i, j+1)]) for i in range(size) for j in range(size)]

        try:
            while True:
                line = input().strip()
                if line.strip() == 'MOVE':
                    the_move = random.choice(list(moves))
                    for sq in squares:
                        if len(sq) == 1:
                            the_move = sq.pop()
                            break
                    moves.remove(the_move)
                    update_squares(squares, the_move)
                    print('{}:{}:{}'.format(*the_move))
                else:
                    c, i, j = line.split(':')
                    new_move = (c, int(i), int(j))
                    moves.remove(new_move)
                    update_squares(squares, new_move)
        except EOFError:
            pass
    except Exception as e:
        print("Exception: " + repr(e))
