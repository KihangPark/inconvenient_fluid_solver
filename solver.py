from param import Params
from data import Particle, Position, Velocity, Acceleration
from utils import NoiadUtils
import math


class NoiadSolver(object):

    logFile = None
    logFlag = False

    def __init__(self):
        self.params = Params()

    # calculate viscosity
    def addViscosityTerm(self, particles):
        for pi in particles:
            if not pi.type == 0:
                continue
            pi.acceleration.x = 0
            pi.acceleration.y = 0
            pi.acceleration.z = 0
            for pj in particles:
                # skip same particle checking
                if pi.index == pj.index:
                    continue
                distanceSquare = Position.distanceSquare(pj.position, pi.position)
                if distanceSquare < self.params.EFFECT_RADIUS_SQUARE:
                    distance = math.sqrt(distanceSquare)
                    weight = NoiadUtils.weight(distance, self.params.EFFECT_RADIUS)
                    vec = Velocity.multiply(Velocity.minus(pj.velocity, pi.velocity), weight)
                    pi.acceleration = Acceleration.plus(pi.acceleration, vec)
            pi.acceleration = Acceleration.multiply(pi.acceleration, self.params.LAPLACIAN_COEFFICIENT)
        return particles

    # add gravity
    def addGravityTerm(self, particles):
        for p in particles:
            if p.type == 0:
                p.acceleration.y += -9.8
        return particles

    # move particle
    def moveParticle(self, particles):
        for p in particles:
            if p.type == 0:
                p.velocity.x += p.acceleration.x * self.params.TIME_INTERVAL
                p.velocity.y += p.acceleration.y * self.params.TIME_INTERVAL
                p.velocity.z += p.acceleration.z * self.params.TIME_INTERVAL
                p.position.x += p.velocity.x * self.params.TIME_INTERVAL
                p.position.y += p.velocity.y * self.params.TIME_INTERVAL
                p.position.z += p.velocity.z * self.params.TIME_INTERVAL
                p.acceleration.x = 0
                p.acceleration.y = 0
                p.acceleration.z = 0
        return particles

    # check collision
    def checkCollision(self, particles):
        for pi in particles:
            if not pi.type == 0:
                continue
            velocityCalculation = pi.velocity
            for pj in particles:
                if pi.index == pj.index:
                    continue
                differnce = Position.minus(pj.position, pi.position)
                distanceSquare = Position.distanceSquare(pj.position, pi.position)
                if distanceSquare < self.params.RADIUS_LIMIT_SQUARE:
                    forceDeltaT = Velocity.innerProduct(Velocity.minus(pi.velocity, pj.velocity), differnce)
                    if forceDeltaT > 0.0:
                        if pi.index == 0:
                            pj.color.r = 1
                            pj.color.b = 1
                        if pi.type == 0:
                            piDensity = self.params.DENSITY_PARTICLE
                        else:
                            piDensity = self.params.DENSITY_WALL
                        if pj.type == 0:
                            pjDensity = self.params.DENSITY_PARTICLE
                        else:
                            pjDensity = self.params.DENSITY_WALL
                        forceDeltaT *= (self.params.COLLISION * pjDensity / (piDensity + pjDensity)) * (1.0 / distanceSquare)
                        velocityCalculation.x -= differnce.x * forceDeltaT
                        velocityCalculation.y -= differnce.y * forceDeltaT
                        velocityCalculation.z -= differnce.z * forceDeltaT
            pi.acceleration.x = velocityCalculation.x
            pi.acceleration.y = velocityCalculation.y
            pi.acceleration.z = velocityCalculation.z
        for p in particles:
            p.velocity.x = p.acceleration.x
            p.velocity.y = p.acceleration.y
            p.velocity.z = p.acceleration.z
        return particles

    # calculate pressure value
    def calculateTemporaryPressure(self, particles):
        for pi in particles:
            temporaryN = 0
            for pj in particles:
                if pi.index == pj.index:
                    continue
                distanceSquare = Position.distanceSquare(pj.position, pi.position)
                if distanceSquare < self.params.EFFECT_RADIUS_SQUARE:
                    distance = math.sqrt(distanceSquare)
                    weight = NoiadUtils.weight(distance, self.params.EFFECT_RADIUS)
                    temporaryN += weight
                    if pi.index == 0:
                        pj.color.g = 1
            if pi.type == 0:
                density = self.params.DENSITY_PARTICLE
            else:
                density = self.params.DENSITY_WALL
            if temporaryN > self.params.N_ZERO:
                pi.pressure = (temporaryN - self.params.N_ZERO) * self.params.TEMPORARY_PRESSURE_COEFFICIENT * density
            else:
                pi.pressure = 0
        return particles

    # calculate pressure gradient
    def calculateModifiedAcceleration(self, particles):
        for pi in particles:
            if not pi.type == 0:
                continue
            acceleration = Acceleration()
            minimumPressure = pi.pressure
            for pj in particles:
                if pi.index == pj.index:
                    continue
                distanceSquare = Position.distanceSquare(pj.position, pi.position)
                if distanceSquare < self.params.EFFECT_RADIUS_SQUARE:
                    if(minimumPressure > pj.pressure):
                        minimumPressure = pj.pressure
            for pj in particles:
                if pi.index == pj.index:
                    continue
                distanceSquare = Position.distanceSquare(pj.position, pi.position)
                if distanceSquare < self.params.EFFECT_RADIUS_SQUARE:
                    distance = math.sqrt(distanceSquare)
                    weight = NoiadUtils.weight(distance, self.params.EFFECT_RADIUS)
                    weight *= (pj.pressure - minimumPressure) / distanceSquare
                    acceleration = Acceleration.plus(acceleration, Acceleration.multiply(Position.minus(pj.position, pi.position), weight))
            pi.acceleration = Acceleration.multiply(acceleration, self.params.INVERSE_DENSITY_PARTICLE * self.params.PRESSURE_GRADIENT_COEFFICIENT)
        return particles

    # set particle final position
    def finalizeParticlePosition(self, particles):
        for p in particles:
            if p.type == 0:
                tempVelocity = Velocity.plus(p.velocity, Acceleration.multiply(p.acceleration, self.params.TIME_INTERVAL))
                p.velocity.x = tempVelocity.x
                p.velocity.y = tempVelocity.y
                p.velocity.z = tempVelocity.z
                tempPosition = Acceleration.plus(p.position, Acceleration.multiply(p.acceleration, (self.params.TIME_INTERVAL * self.params.TIME_INTERVAL)))
                p.position.x = tempPosition.x
                p.position.y = tempPosition.y
                p.position.z = tempPosition.z
                p.acceleration.x = 0
                p.acceleration.y = 0
                p.acceleration.z = 0
        return particles


# particle generator
class ParticleGenerator(object):

    particles = []
    logFlag = False

    def __init__(self):
        self.particles = []

    def generateParticles(self):
        if not len(self.particles) == 0:
            index = len(self.particles)
        else:
            index = 0
        for x in range(20, 25):
            for y in range(20, 50):
                for z in range(0, 1):
                    p = Particle()
                    p.position.x = x
                    p.position.y = y
                    p.position.z = z
                    p.velocity.x = 0
                    p.velocity.y = 0
                    p.velocity.z = 0
                    p.acceleration.x = 0
                    p.acceleration.y = 0
                    p.acceleration.z = 0
                    p.type = 0
                    p.index = index
                    self.particles.append(p)
                    index += 1

    def generateGround(self):
        index = 0
        if not len(self.particles) == 0:
            index = len(self.particles)
        for x in range(20, 60):
            for y in range(17, 20):
                for z in range(0, 1):
                    p = Particle()
                    p.position.x = x
                    p.position.y = y
                    p.position.z = z
                    p.velocity.x = 0
                    p.velocity.y = 0
                    p.velocity.z = 0
                    p.type = 1
                    p.index = index
                    self.particles.append(p)
                    index += 1
        for x in range(17, 20):
            for y in range(17, 50):
                for z in range(0, 1):
                    p = Particle()
                    p.position.x = x
                    p.position.y = y
                    p.position.z = z
                    p.velocity.x = 0
                    p.velocity.y = 0
                    p.velocity.z = 0
                    p.type = 1
                    p.index = index
                    self.particles.append(p)
                    index += 1
        for x in range(60, 63):
            for y in range(17, 50):
                for z in range(0, 1):
                    p = Particle()
                    p.position.x = x
                    p.position.y = y
                    p.position.z = z
                    p.velocity.x = 0
                    p.velocity.y = 0
                    p.velocity.z = 0
                    p.type = 1
                    p.index = index
                    self.particles.append(p)
                    index += 1

