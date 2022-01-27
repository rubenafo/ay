from dataclasses import dataclass

import numpy
from numpy.random import random

from ay.Point import Point


class Field:

    def __init__(self, pos: Point = Point(0,0), mass: float = 100.0, decay: float = 0.0):
        self.pos = pos
        self.mass = mass
        self.decay = decay

    def update_decay(self):
        self.mass = self.mass - self.decay


class Particle:

    def __init__(self, pos: Point = Point(0,0), speed: Point = Point(0,0), ttl: float = -1):
        self.position = pos
        self.speed = speed
        self.initial_speed = speed.cp()
        self.acceleration = Point(0,0)
        self.ttl = ttl
        self.alive = True
        self.trace = [self.position]

    def submit (self, fs: list[Field]):
        total_acc = Point(0,0)
        for field in fs:
            v = field.pos - self.position
            mag = (v.x * v.x) + (v.y * v.y)
            force = field.mass / mag
            total_acc = total_acc + v * force
        self.acceleration = total_acc
        return self

    def move(self):
        self.speed = self.speed + self.acceleration
        self.position = self.position + self.speed
        self.trace.append(self.position)
        return self


@dataclass
class Emitter:
    pos: Point = Point(0, 0)
    speed: Point = 0.0
    xsize: int = 10
    ysize: int = 10
    particle_life: float = 10
    spread: float = 1.0
    rate: float = 5.0
    rnd: numpy.random = random()

    def emit_particle(self):
        part_pos = self.pos + (self.xsize * self.rnd(), self.ysize * self.rnd())
        return Particle(pos=part_pos, speed=self.speed, ttl=self.particle_life)


class ParticleSystem:

    def __init__(self, seed: float = 1.0):
        self.elapsed: int = 0
        self.particles: list[Particle] = []
        self.max_particles:int = 2000
        self.emitters: list[Emitter] = []
        self.fields: list[Field] = []
        self.seed: float = seed
        self.rnd: numpy.random = random(self.seed)

    def add_emitter(self, pos: Point, speed: Point, xsize: int, ysize: int, life: int, spread: float, rate: float):
        emitter = Emitter(pos, speed, xsize, ysize, life, spread, rate, self.rnd)
        self.emitters.append(emitter)
        return self

    def add_field (self, pos: Point, mass: float, decay: float):
        self.fields.append(Field(pos, mass, decay))
        return self

    def __add_particles (self):
        particles = [ e.emit_particle() for e in self.emitters]
        self.particles.append(particles)

    def evolve(self, steps: int):
        for i in range(0, steps):
            if len(self.particles) < self.max_particles:
                self.__add_particles()
            [p.submit(self.fields).move() for p in self.particles]
            [field.decay() for field in self.fields]
