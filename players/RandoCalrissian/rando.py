import random
import sys

if __name__ == "__main__":
    i = input()
    with open(sys.argv[1] + '.log', 'a') as f:
        f.write("Init: " + i)
    setup = i.strip().split(':')
    size = int(setup[0])
    whoami = int(setup[1])

    moves = set(('V', i, j) for i in range(size) for j in range(size + 1))
    moves |= set(('H', j, i) for i in range(size) for j in range(size + 1))
    while True:
        line = input().strip()
        with open(sys.argv[1] + '.log', 'a') as f:
            f.write("line: " + line)
        if line == 'MOVE\n':
            print('{}:{}:{}'.format(*random.choice(list(moves))))
        else:
            c, i, j = line.split(':')
            moves.remove((c, int(i), int(j)))
