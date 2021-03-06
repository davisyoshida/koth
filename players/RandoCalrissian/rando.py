import random

if __name__ == "__main__":
    setup = input().strip().split(':')
    size = int(setup[0])
    whoami = int(setup[1])

    moves = set(('V', i, j) for i in range(size) for j in range(size + 1))
    moves |= set(('H', j, i) for i in range(size) for j in range(size + 1))
    try:
        while True:
            line = input().strip()
            if line.strip() == 'MOVE':
                the_move = random.choice(list(moves))
                moves.remove(the_move)
                print('{}:{}:{}'.format(*the_move))
            else:
                c, i, j = line.split(':')
                moves.remove((c, int(i), int(j)))
    except EOFError:
        pass
