from collections import defaultdict
import itertools
import random


class C3PO:
    def __init__(self, size):
        self.side_to_boxes = defaultdict(list)
        self.box_to_sides = defaultdict(list)
        for r, c in itertools.product(range(size), range(size)):
            for side in [(False, r, c), (True, r, c), (False, r + 1, c), (True, r, c + 1)]:
                self.side_to_boxes[side].append((r, c))
                self.box_to_sides[r, c].append(side)

        self.count_to_boxes = defaultdict(set)
        self.count_to_boxes[0] = set(itertools.product(range(size), range(size)))
        self.box_to_count = defaultdict(int)

    def make_move(self, move):
        for box in self.side_to_boxes[move]:
            self.box_to_sides[box].remove(move)
            count = self.box_to_count[box]
            self.count_to_boxes[count].remove(box)
            self.count_to_boxes[count + 1].add(box)
            self.box_to_count[box] = count + 1
        del self.side_to_boxes[move]

    def get_move(self):
        move = self.select_move()
        self.make_move(move)
        return move

    def select_move(self):
        if self.count_to_boxes[3]:
            box = random.choice(tuple(self.count_to_boxes[3]))
            move, = self.box_to_sides[box]
            return move
        else:
            for count in [1, 0]:
                for box in sorted(self.count_to_boxes[count], key=shuffle_key):
                    for side in sorted(self.box_to_sides[box], key=shuffle_key):
                        if all(self.box_to_count[box] != 2 for box in self.side_to_boxes[side]):
                            return side

        return random.choice(tuple(self.side_to_boxes))


def shuffle_key(*args):
    return random.random()

if __name__ == "__main__":
    setup = input().strip().split(':')
    size = int(setup[0])
    whoami = int(setup[1])

    player = C3PO(size)

    try:
        while True:
            line = input().strip()
            if line.strip() == 'MOVE':
                is_vert, row, col = player.get_move()
                print('{}:{}:{}'.format('V' if is_vert else 'H', row, col))
            else:
                c, i, j = line.split(':')
                move = (c == 'V', int(i), int(j))
                player.make_move(move)
    except EOFError:
        pass
