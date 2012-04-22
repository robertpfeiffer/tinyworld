import math
G=1

class planet(object):
    def __init__(self,pos,diam,mass):
        self.pos=pos
        self.diam=diam
        self.mass=mass
        self.orient=None
        self.rest=True

class small_body(object):
    def __init__(self,pos,speed):
        self.rest=False
        self.pos=pos
        self.speed=speed
        self.orient=None
        self.rest=False

def add((x1,y1),(x2,y2)):
    return x1+x2,y1+y2

def dot((x1,y1),(x2,y2)):
    return x1*x2+y1*y2

def rot((x,y), angle):
    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    return (x*cos - y*sin, x*sin + y*cos)

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
            if not body.rest:
                a = gravity_at_point(body.pos,planets)
                v = add(body.speed, scale(a,t))
                s = add(body.pos, scale(v,t))
                body.speed,body.pos,body.acc=v,s,a

def orient(body):
    if body.orient=="speed":
        if body.speed!=(0,0):
            return norm(body.speed,1)
    if body.orient=="acceleration":
        return norm(body.acc,1)
    return 0,0

def get_angle(body):
    pos=body.pos
    if not body.orient:
        return 0
    else:
        if body.orient=="speed":
            if body.speed==(0,0):
                return 0
            v = norm(body.speed,1)
        if body.orient=="acceleration":
            v = norm(body.acc,1)
        x,y=v
        if y != 0.0:
            angle=180*math.atan(x/y)/math.pi
            if y > 0:
                angle = 180 + angle
        else:
            if x>0:
                angle=270
            else:
                angle=90
        return angle
