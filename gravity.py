import math
G=1

class planet(object):
    def __init__(self,pos,diam,mass):
        self.pos=pos
        self.diam=diam
        self.mass=mass
        self.orient=None

class small_body(object):
    def __init__(self,pos,speed):
        self.pos=pos
        self.speed=speed
        self.orient=None

def add((x1,y1),(x2,y2)):
    return x1+x2,y1+y2

def length((x,y)):
    return math.sqrt(x*x+y*y)

def scale((x,y),f):
    return x*f,y*f

def norm(v,l):
    return scale(v,l/length(v))

def sub((x1,y1),(x2,y2)):
    return x1-x2,y1-y2

def gravity_at_point(point,planets):
    """ return gravity in pixels per second per second """
    g=0,0
    for planet in planets:
        r = sub(point,planet.pos)
        l = length(r)
        if l==0:
            continue
        if l<planet.diam:
            r=norm(r,planet.diam)
        a=scale(norm(r,1),(-1*planet.mass*G)/length(r)**2)
        g=add(g,a)
    return g

def simulate(planets, small_bodies, t,n=1):
    """imulate for t seconds"""
    for i in range(n):
        for body in small_bodies:
            a = gravity_at_point(body.pos,planets)
            v = add(body.speed, scale(a,t))
            s = add(body.pos, scale(v,t))
            body.speed,body.pos,body.acc=v,s,a
