import random
def update_squares(squares, move):
    for sq in squares:
        try:
            sq.remove(move)
            if len(sq) == 0:
                squares.remove(sq)
        except KeyError:
            pass

if __name__ == "__main__":
    setup = input().strip().split(':')
    size = int(setup[0])
    whoami = int(setup[1])
	
    moves = set(('V', i, j) for i in range(size) for j in range(size + 1))
    moves |= set(('H', j, i) for i in range(size) for j in range(size + 1))
    squares = [set([('V', i, j),('H', i, j),('H', i+1, j),('V', i, j+1)]) for i in range(size-1) for j in range(size)]
    
    try:
        while True:
            line = input().strip()
            if line.strip() == 'MOVE':
                the_move = random.choice(list(moves))
                for sq in squares:
                    if len(sq) == 1:
                        the_move = sq.pop()
                moves.remove(the_move)
                update_squares(squares,the_move)
                print('{}:{}:{}'.format(*the_move))
            else:
                c, i, j = line.split(':')
                new_move = (c,int(i),int(j))
                moves.remove(new_move)
                update_squares(squares,new_move)
    except EOFError:
        pass