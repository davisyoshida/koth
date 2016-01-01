#!/usr/bin/env python3
from graphics import Circle, GraphWin, Line, Point, Rectangle, color_rgb, Text
import json
import os


def printer(win, results_dir, f, i, j):
    win.postscript(file=os.path.join(results_dir, '{}.{:04}.{:04}.ps').format(f, i, j+1), colormode='color')

if __name__ == "__main__":
    results_dir = 'results'
    for f in (f for f in os.listdir(results_dir) if f.endswith('.log')):
        hist = json.load(open(os.path.join(results_dir, f)))
        colors = None
        for i, game in enumerate(hist):
            score = [0, 0]
            images = []
            names = game['players']
            size = int(game['size'])

            dim = 600
            left_marg = 50
            top_marg = 200
            win = GraphWin(game, dim + 2*left_marg, dim + top_marg + 50)
            win.setBackground(color_rgb(255, 255, 255))

            if not colors:
                colors = {names[0]: 'blue', names[1]: 'red'}
                p1 = Text(Point(left_marg + dim//2, 30), names[0])
                p1.setFill(colors[names[0]])
                p1.setSize(20)
                score1 = Text(Point(left_marg + dim//6, 70), '0:0')
                score1.setFill(colors[names[0]])
                score1.setSize(30)

                vs = Text(Point(left_marg + dim//2, 70), 'vs')
                vs.setFill('black')
                vs.setSize(20)

                p2 = Text(Point(left_marg + dim//2, 110), names[1])
                p2.setFill(colors[names[1]])
                p2.setSize(20)
                score2 = Text(Point(left_marg + 5*dim//6, 70), '0:0')
                score2.setFill(colors[names[1]])
                score2.setSize(30)

                score_text = {names[0]: score1, names[1]: score2}

                wins = {n: 0 for n in names}

            scores = {n: 0 for n in names}
            p1.draw(win)
            vs.draw(win)
            p2.draw(win)
            for player, st in score_text.items():
                st.setText('{}:{}'.format(wins[player], scores[player]))
                st.draw(win)

            points = [[Point(left_marg + c * dim//size, top_marg + r * dim//size) for c in range(size + 1)] for r in range(size + 1)]
            dots = [[Circle(p, 5) for p in l] for l in points]
            for l in dots:
                for c in l:
                    c.setFill('black')
                    c.draw(win)

            printer(win, results_dir, f, i, 0)
            for j, (player, entry) in enumerate(game['history'], start=1):
                # Box finished
                is_vert, r, c = entry
                r = int(r)
                c = int(c)
                if is_vert == '':
                    rec = Rectangle(points[r][c], points[r+1][c+1])
                    rec.setFill(colors[player])
                    rec.draw(win)
                    scores[player] += 1
                    score_text[player].undraw()
                    score_text[player].setText('{}:{}'.format(wins[player], scores[player]))
                    score_text[player].draw(win)
                else:
                    if is_vert:
                        line = Line(points[r][c], points[r+1][c])
                    else:
                        line = Line(points[r][c], points[r][c+1])
                    line.draw(win)
                    line.setFill(colors[player])

                printer(win, results_dir, f, i, j)
            (n1, s1), (n2, s2) = scores.items()
            if s1 > s2:
                winner = n1
            elif s2 > s1:
                winner = n2
            else:
                winner = None

            if winner:
                wins[winner] += 1
                score_text[winner].undraw()
                score_text[winner].setText('{}:{}'.format(wins[winner], scores[winner]))
                score_text[winner].draw(win)
            printer(win, results_dir, f, i, j+1)

            win.close()
