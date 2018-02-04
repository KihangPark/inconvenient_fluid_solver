import math


class Color(object):

    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 0


class Vector(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    @staticmethod
    def generate(x, y, z):
        result = Vector()
        result.x = x
        result.y = y
        result.z = z
        return result

    @staticmethod
    def minus(p1, p2):
        result = Vector()
        result.x = p1.x - p2.x
        result.y = p1.y - p2.y
        result.z = p1.z - p2.z
        return result

    @staticmethod
    def plus(p1, p2):
        result = Vector()
        result.x = p1.x + p2.x
        result.y = p1.y + p2.y
        result.z = p1.z + p2.z
        return result

    @staticmethod
    def innerProduct(p1, p2):
        result = p1.x * p2.x + p1.y * p2.y + p1.z * p2.z
        return result

    @staticmethod
    def multiply(p1, w):
        result = Vector()
        result.x = p1.x * w
        result.y = p1.y * w
        result.z = p1.z * w
        return result


class Position(Vector):

    def __init__(self):
        super(Vector, self).__init__()
        v = Vector()
        self.x = v.x
        self.y = v.y
        self.z = v.z

    @staticmethod
    def distanceSquare(p1, p2):
        d1 = p1.x - p2.x
        d2 = p1.y - p2.y
        d3 = p1.z - p2.z
        result = d1 * d1 + d2 * d2 + d3 * d3
        return result

    @staticmethod
    def distance(p1, p2):
        d1 = p1.x - p2.x
        d2 = p1.y - p2.y
        d3 = p1.z - p2.z
        result = math.sqrt(d1 * d1 + d2 * d2 + d3 * d3)
        return result


class Velocity(Vector):

    def __init__(self):
        super(Vector, self).__init__()
        v = Vector()
        self.x = v.x
        self.y = v.y
        self.z = v.z


class Acceleration(Vector):

    def __init__(self):
        super(Vector, self).__init__()
        v = Vector()
        self.x = v.x
        self.y = v.y
        self.z = v.z


class Particle(object):

    def __init__(self):
        self.position = Position()
        self.velocity = Velocity()
        self.acceleration = Acceleration()
        self.color = Color()
        self.type = 0
        self.index = 0
        self.pressure = 0
