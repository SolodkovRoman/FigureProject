from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def __init__(self):
        self._cnt = 0

    def get_cnt(self):
        return self._cnt

    @staticmethod
    def check_dot(a):
        if 1 < a.x < 2 and 1 < a.y < 2:
            return False
        if a.x > 4 or a.x < -1 or a.y > 4 or a.y < -1:
            return False
        if min(a.dist(R2Point(0, 0)), a.dist(R2Point(0, 3)),
               a.dist(R2Point(3, 0)), a.dist(R2Point(3, 3))) <= 1:
            return True
        if a.x < 0 and a.y < 0 or a.x < 0 and a.y > 3 or \
           a.x > 3 and a.y < 0 or a.x > 3 and a.y > 3:
            return False
        return True


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p
        self._cnt = 1*Figure.check_dot(p)

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q
        self._cnt = 1*Figure.check_dot(p) + 1*Figure.check_dot(q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return Segment(self.p, r)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._cnt = (1*Figure.check_dot(a) +
                     1*Figure.check_dot(b) + 1*Figure.check_dot(c))

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._cnt -= 1*Figure.check_dot(p)
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._cnt -= 1*Figure.check_dot(p)
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление новой точки
            self._cnt += 1*Figure.check_dot(t)
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
