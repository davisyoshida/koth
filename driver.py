#!/usr/bin/env python3
from collections import defaultdict
from csv import reader
from game import Game
import itertools
from operator import itemgetter
import proc_wrapper
import sys
from time import sleep
import traceback


class Tournament(object):
    def __init__(self):
        self.players = {}
        with open('players.txt') as f:
            for line in reader(f):
                self.players[line[0]] = line[1:]

    def run(self):
        """
        Conduct the tournament
        """
        scores = defaultdict(int)
        for p0, p1 in itertools.combinations(self.players, 2):
            # scores[None] if a draw
            scores[self.match([p0, p1])] += 1
        return scores

    def match(self, ps):
        """
        Run a series of games between the two given players
        Args:
            ps: Sequence containing the players
        """
        record = [0, 0]
        for i in range(5):
            res = self.play(ps, 5 + i//10)
            if res >= 0:
                record[res] += 1
            print(record)

        for i in range(5):
            res = self.play(reversed(ps), 5 + i//10)
            if res >= 0:
                record[1 - res] += 1
            print(record)
        return None if record[0] == record[1] else ps[0] if record[0] > record[1] else ps[1]

    def play(self, names, n):
        """
        Run a single game between two players
        Args:
            names: Sequence containing the names of the players
            n: Game board size
        """

        procs = [proc_wrapper.IOProcess(self.players[name], [bytes('{}:{}\n'.format(n, i), encoding='ascii')]) for i, name in enumerate(names)]

        for proc in procs:
            proc.start()

        g = Game(n)
        player = 0
        winner = None
        while winner is None:
            for move in g.get_new_moves(player):
                procs[player].send_no_wait(bytes(move, encoding='ascii'))

            move = procs[player].send_and_receive(b'MOVE\n')
            if not move:
                winner = 1 - player
                continue

            try:
                player = g.str_move(move.decode('ascii'), player)
            except Exception as e:
                sys.stderr.write("%s -- Encountered exception %s\n" % (names[player], e))
                traceback.print_exc()
            winner = g.get_winner()

        for p in procs:
            proc.end()
        sleep(1)
        return winner

if __name__ == "__main__":
    t = Tournament()
    scores = t.run()

    for p, s in sorted(scores.items(), key=itemgetter(1), reverse=True):
        print("{}: {}".format(p, s))
