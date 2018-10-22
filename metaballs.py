# this script makes the metaballs in the scene move sort of randomly around a target object
# the target can be any object in the scene as long as it is called 'target'

import bpy
import math
from random import uniform

def dist(v1, v2):
    a = v2.x - v1.x
    b = v2.y - v1.y
    c = v2.z - v1.z
    return math.sqrt(a ** 2 + b ** 2 + c ** 2)


class Vector():
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    @classmethod
    def st_sub(cls, v1, v2):
        return cls(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
    def add(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z
    def sub(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
    def mult(self, n):
        self.x *= n
        self.y *= n
        self.z *= n
    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    def norm(self):
        m = self.mag()
        self.x /= m
        self.y /= m
        self.z /= m
    def limit(self, n):
        if self.mag() > n:
            self.norm()
            self.mult(n)


class Particle():
    def __init__(self, metaball, x = 0, y = 0, z = 0):
        self.metaball = metaball
        self.scalval = metaball.scale.x
        self.x = x
        self.y = y
        self.z = z
        self.pos = Vector(self.x, self.y, self.z)
        self.vel = Vector(uniform(-.01, .01), 0, uniform(-.01, .01))
        self.acc = Vector()
    def show(self):
        self.metaball.location.x = self.pos.x
        self.metaball.location.y = self.pos.y
        self.metaball.location.z = self.pos.z
    def update(self):
        self.vel.add(self.acc)
        self.vel.limit(1)
        self.pos.add(self.vel)
        self.acc.mult(0)        
    def applyForce(self, f):
        self.acc.add(f)
    def seek(self, target):
        targetpos = Vector(target.location.x, target.location.y, target.location.z)
        desiredvel = Vector.st_sub(targetpos, self.pos)
        steeringforce = Vector.st_sub(desiredvel, self.vel)
        steeringforce.mult(0.001)
        self.applyForce(steeringforce)
    def grow(self, target):
        targetpos = Vector(target.location.x, target.location.y, target.location.z)
        d = dist(self.pos, targetpos)
        scalar = self.scalval * d * 1.25 + .2
        self.metaball.scale = (scalar, scalar, scalar)


def draw(scene):
    for i in p:
        nmult = .0005
        n = Vector(uniform(-nmult, nmult), uniform(-nmult, nmult), uniform(-nmult, nmult))
        i.applyForce(n)
        i.seek(target)
        i.grow(target)
        i.update()
        i.show()


target = bpy.data.objects['target']
p = [Particle(i, i.location.x, i.location.y, i.location.z) for i in bpy.data.objects if i.type == 'META']
bpy.app.handlers.frame_change_pre.clear()
bpy.app.handlers.frame_change_pre.append(draw)
