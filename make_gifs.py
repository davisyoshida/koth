#!/usr/bin/env python3
from graphics import Circle, GraphWin, Image, Line, Point, Rectangle, Text
import json
import os

if __name__ == "__main__":
    results_dir = 'results'
    for f in (f for f in os.listdir(results_dir) if os.path.isfile(os.path.join(results_dir, f))):
        hist = json.load(open(os.path.join(results_dir, f)))
        colors = None
        for i, game in enumerate(hist):
            score = [0, 0]
            images = []
            names = game['players']
            size = int(game['size'])

            dim = 500
            left_marg = 50
            top_marg = 150
            win = GraphWin(game, dim + 2*left_marg, dim + top_marg + 50)

            if not colors:
                colors = {names[0]: 'blue', names[1]: 'red'}
                p1 = Text(Point(left_marg + dim//2, 20), names[0])
                p1.setFill(colors[names[0]])
                score1 = Text(Point(left_marg + dim//4, 50), '0')
                score1.setFill(colors[names[0]])
                score1.setSize(20)

                vs = Text(Point(left_marg + dim//2, 50), 'vs')
                vs.setFill('black')

                p2 = Text(Point(left_marg + dim//2, 80), names[1])
                p2.setFill(colors[names[1]])
                score2 = Text(Point(left_marg + 3*dim//4, 50), '0')
                score2.setFill(colors[names[1]])
                score2.setSize(20)

                score_text = {names[0]: score1, names[1]: score2}

            p1.draw(win)
            vs.draw(win)
            p2.draw(win)
            score1.draw(win)
            score2.draw(win)

            points = [[Point(left_marg + c * dim//size, top_marg + r * dim//size) for c in range(size + 1)] for r in range(size + 1)]
            dots = [[Circle(p, 5) for p in l] for l in points]
            for l in dots:
                for c in l:
                    c.setFill('black')
                    c.draw(win)

            scores = {n: 0 for n in names}

            win.postscript(file=os.path.join(results_dir, '{}.{}.{}.ps').format(f, i, 0), colormode='color')
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
                    score_text[player].setText(str(scores[player]))
                    score_text[player].draw(win)
                else:
                    if is_vert:
                        line = Line(points[r][c], points[r+1][c])
                    else:
                        line = Line(points[r][c], points[r][c+1])
                    line.draw(win)
                    line.setFill(colors[player])
                win.postscript(file=os.path.join(results_dir, '{}.{}.{}.ps').format(f, i, j), colormode='color')

            win.close()
