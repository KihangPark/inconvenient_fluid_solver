import math
from utils import NoiadUtils


class Params(object):

    # time interval
    # this param is very important to get stable simulation
    # to get stable simulation, the calculation must be calculated by below function
    # Umax = 2.0 * sqrt(9.8 * height)
    # deltaT < ((0.2 * distance between particles(= PARTICLE_DISTANCE)) / Umax)
    # original source : https://www.jstage.jst.go.jp/article/jsces/2010/0/2010_0_20100013/_pdf
    TIME_INTERVAL = 0.005

    # distance between particles
    PARTICLE_DISTANCE = 1

    # distance limitation, particles can not be reduced under distance limitation
    DISTANCE_LIMIT_RATIO = 0.9
    RADIUS_LIMIT = PARTICLE_DISTANCE * DISTANCE_LIMIT_RATIO
    RADIUS_LIMIT_SQUARE = RADIUS_LIMIT * RADIUS_LIMIT

    # density value come from physical value
    DENSITY_PARTICLE = 1000
    INVERSE_DENSITY_PARTICLE = 1.0 / 1000
    DENSITY_WALL = 1000
    INVERSE_DENSITY_WALL = 1.0 / 1000

    # reflection ratio when particle collides
    COLLISION_RATIO = 0.2
    COLLISION = 1.0 + COLLISION_RATIO

    # distance which receive pressure
    EFFECT_RADIUS = PARTICLE_DISTANCE * 2.1
    EFFECT_RADIUS_SQUARE = EFFECT_RADIUS * EFFECT_RADIUS

    COEFFICIENT_OF_KINEMATIC_VISCOSITY = 0.000001

    # speed of sound, this value must be determined by below calculation
    # c < (1.0 * distance between particles) / deltaT
    SPEED_OF_SOUND = 200.0

    # dimension
    DIMENSION = 2

    # courant number
    COURANT_NUMBER = 0.1

    MIN_X = 17
    MAX_X = 63
    MIN_Y = 17
    MAX_Y = 53

    def __init__(self):

        temporaryNZero = 0
        temporaryLamda = 0

        # calculate initial pressure
        for indexX in range(-4, 5):
            for indexY in range(-4, 5):

                x = self.PARTICLE_DISTANCE * indexX
                y = self.PARTICLE_DISTANCE * indexY
                distanceSquare = x * x + y * y

                if distanceSquare < self.EFFECT_RADIUS_SQUARE:
                    if distanceSquare == 0.0:
                        continue
                    distance = math.sqrt(distanceSquare)
                    temporaryNZero += NoiadUtils.weight(distance, self.EFFECT_RADIUS)
                    temporaryLamda += distanceSquare * NoiadUtils.weight(distance, self.EFFECT_RADIUS)

        # initial particle density
        self.N_ZERO = temporaryNZero

        # lamda coefficient
        self.LAMDA = temporaryLamda / temporaryNZero

        # coefficient for gradient model
        self.LAPLACIAN_COEFFICIENT = (2.0 * 3 * self.COEFFICIENT_OF_KINEMATIC_VISCOSITY) / (self.N_ZERO * self.LAMDA)

        # temporary coefficient for pressure
        self.TEMPORARY_PRESSURE_COEFFICIENT = self.SPEED_OF_SOUND * self.SPEED_OF_SOUND / self.N_ZERO

        # coefficient for pressure gradient
        self.PRESSURE_GRADIENT_COEFFICIENT = -1.0 * self.DIMENSION / self.N_ZERO

        # coefficients for bucket feature
        self.BUCKET_LENGTH = self.EFFECT_RADIUS * (1.0 + self.COURANT_NUMBER)
        self.BUCKET_LENGTH_SQUARE = self.BUCKET_LENGTH * self.BUCKET_LENGTH
        self.INVERSE_BUCKET_NUMBER = 1.0 / self.BUCKET_LENGTH

        self.X_BUCKET_NUMBER = int((self.MAX_X - self.MIN_X) * self.INVERSE_BUCKET_NUMBER) + 3
        self.Y_BUCKET_NUMBER = int((self.MAX_Y - self.MIN_Y) * self.INVERSE_BUCKET_NUMBER) + 3
        self.XY_BUCKET_NUMBER = self.X_BUCKET_NUMBER * self.Y_BUCKET_NUMBER
