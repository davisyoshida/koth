class Game:
    """
    Class for managing games of dots and boxes

    Attributes:
        n: Side length of game board (there will be n^2 boxes)
        players: Sequence of player names
    """
    def __init__(self, size, players):
        self.size = size

        self.new_moves = [[], []]
        self.moves = set()

        self.count = [[0 for _ in range(size)] for _ in range(size)]

        self.scores = [0, 0]
        self.remaining_boxes = size**2

        self.next_move = 0

        self.players = players
        self.history = []

    def str_move(self, s, player):
        """
        Make a move by using a string
        Args:
            s: String of the form: "<'V' or 'H'>:<row>:<col>". E.g. V:0:3
            player: player index
        """
        move_type, row, col = s.split(':')
        return self.move(move_type == 'V', int(row), int(col), player)

    def move(self, is_vert, row, col, player):
        """
        Make a move. Updates the
        Args:
            is_vert: True if this is a vertical move
            row: int in  [0, n)
            col: int in [0, n)
            player: player index

        Returns:
            Returns the index of the next player whose move it is

        Raises:
            ValueError: If the move is not legal
        """
        if self.move_invalid(is_vert, row, col):
            raise ValueError("Invalid move: {}:{}:{}".format(is_vert, row, col))

        if (is_vert, row, col) in self.moves:
            raise ValueError("Move in occupied space")
        else:
            move = is_vert, row, col
            self.moves.add(move)
            s_move = '{}:{}:{}\n'.format('V' if is_vert else 'H', row, col)
            self.new_moves[1 - player].append(s_move)
            self.history.append((self.players[player], move))

        boxes = []
        if is_vert:
            if col < self.size:
                boxes.append((row, col))

            if col:
                boxes.append((row, col - 1))

        else:
            if row < self.size:
                boxes.append((row, col))

            if row:
                boxes.append((row - 1, col))

        next_player = (player + 1) % 2
        for r, c in boxes:
            self.count[r][c] += 1
            if self.count[r][c] == 4:
                self.scores[player] += 1
                self.history.append((self.players[player], ('', r, c)))
                next_player = player
                self.remaining_boxes -= 1

        return next_player

    def move_invalid(self, is_vert, row, col):
        return row < 0 or col < 0 or\
               is_vert and (row >= self.size or col > self.size) or\
               not is_vert and (row > self.size or col >= self.size)

    def get_winner(self):
        """
        Returns:
            None if the game is running, non-negative player number if there is a winner, -1 if there is a tie
        """
        if self.remaining_boxes:
            return None
        else:
            return -1 if self.scores[0] == self.scores[1] else 0 if self.scores[0] > self.scores[1] else 1

    def get_new_moves(self, player):
        t = self.new_moves[player]
        self.new_moves[player] = []
        return t

    def get_history(self):
        return {'size': self.size, 'players': self.players, 'history': self.history}
