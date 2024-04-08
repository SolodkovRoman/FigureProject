from pytest import approx
from math import sqrt
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Void()

    # Нульугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        assert isinstance(self.f, Void)

    # Кол-во нужных точек у нульугольника равно 0
    def test_cnt(self):
        assert self.f.get_cnt() == 0

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        assert isinstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint1:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(0.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Кол-во нужных точек у этого одноугольника равно 1
    def test_cnt(self):
        assert self.f.get_cnt() == 1

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestPoint2:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Point(R2Point(-4.0, 0.0))

    # Одноугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        assert isinstance(self.f, Point)

    # Кол-во нужных точек у этого одноугольника равно 0
    def test_cnt(self):
        assert self.f.get_cnt() == 0

    # При добавлении точки одноугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(-4.0, 0.0)) is self.f

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add2(self):
        assert isinstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestSegment:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0))

    # Двуугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        assert isinstance(self.f, Segment)

    # Кол-во нужных точек у этого двугольника равно 2
    def test_cnt(self):
        assert self.f.get_cnt() == 2

    # При добавлении точки двуугольник может не измениться
    def test_add1(self):
        assert self.f.add(R2Point(0.5, 0.0)) is self.f

    # Он не изменяется в том случае, когда добавляемая точка совпадает
    # с одним из концов отрезка
    def test_add2(self):
        assert self.f.add(R2Point(0.0, 0.0)) is self.f

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add3(self):
        assert isinstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add4(self):
        assert isinstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add5(self):
        assert isinstance(self.f.add(R2Point(0.0, 1.0)), Polygon)


class TestPolygon:

    # Инициализация (выполняется для каждого из тестов класса)
    def setup_method(self):
        self.a = R2Point(0.0, 0.0)
        self.b = R2Point(1.0, 0.0)
        self.c = R2Point(0.0, 1.0)
        self.f = Polygon(self.a, self.b, self.c)

    # Многоугольник является фигурой
    def test_figure(self):
        assert isinstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon1(self):
        assert isinstance(self.f, Polygon)

    # Изменение порядка точек при создании объекта всё равно порождает Polygon
    def test_polygon2(self):
        self.f = Polygon(self.b, self.a, self.c)
        assert isinstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes1(self):
        assert self.f.points.size() == 3

    #   добавление точки внутрь многоугольника не меняет их количества
    def test_vertexes2(self):
        assert self.f.add(R2Point(0.1, 0.1)).points.size() == 3

    #   добавление другой точки может изменить их количество
    def test_vertexes3(self):
        assert self.f.add(R2Point(1.0, 1.0)).points.size() == 4

    #   изменения выпуклой оболочки могут и уменьшать их количество
    def test_vertexes4(self):
        assert self.f.add(
            R2Point(
                0.4,
                1.0)).add(
            R2Point(
                1.0,
                0.4)).add(
                    R2Point(
                        0.8,
                        0.9)).add(
                            R2Point(
                                0.9,
                                0.8)).points.size() == 7
        assert self.f.add(R2Point(2.0, 2.0)).points.size() == 4

    # Изменение кол-ва нужных точек многоугольника
    #   изначально 3
    def test_cnt1(self):
        assert self.f.get_cnt() == 3

    #   может не измениться
    def test_cnt2(self):
        self.f.add(R2Point(1.5, 1.5))
        assert self.f.get_cnt() == 3

    #   может не измениться
    def test_cnt3(self):
        self.f.add(R2Point(-1.5, 0.5))
        assert self.f.get_cnt() == 3

    #   может не измениться
    def test_cnt4(self):
        self.f.add(R2Point(4, 4))
        assert self.f.get_cnt() == 3

    #   может измениться
    def test_cnt5(self):
        self.f.add(R2Point(3.7, 3.7))
        assert self.f.get_cnt() == 4

    #   может измениться
    def test_cnt6(self):
        self.f.add(R2Point(1, 4))
        assert self.f.get_cnt() == 4
