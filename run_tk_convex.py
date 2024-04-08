#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


def draw_square(tk):
    for i in range(15):
        tk.draw_circle(R2Point(0, (3/14)*i), 1)
        tk.draw_circle(R2Point(3, (3/14)*i), 1)
        tk.draw_circle(R2Point((3/14)*i, 0), 1)
        tk.draw_circle(R2Point((3/14)*i, 3), 1)
    tk.draw_grey_line(R2Point(0, 0), R2Point(0, 3))
    tk.draw_grey_line(R2Point(0, 3), R2Point(3, 3))
    tk.draw_grey_line(R2Point(3, 3), R2Point(3, 0))
    tk.draw_grey_line(R2Point(3, 0), R2Point(0, 0))


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
f = Void()
tk.clean()
draw_square(tk)

try:
    while True:
        f = f.add(R2Point())
        tk.clean()
        draw_square(tk)
        f.draw(tk)
        print(f"answer = {f.get_cnt()}")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
