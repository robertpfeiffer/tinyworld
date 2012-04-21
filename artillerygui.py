import pygame,math,random
from pygame.locals import *
import gravity

# HACK: uncomment this line only on win32 when packaging
# import pygame._view # for py2exe

pygame.init()
pygame.font.init()

mainloop=True
clock = pygame.time.Clock() # create clock object

screen = pygame.display.set_mode([640,480],pygame.DOUBLEBUF)
screen.fill([0,0,0])
pygame.key.set_repeat(1, 1)

human_png = pygame.image.load("stick.png")
arrow_png = pygame.image.load("arrow.png")
moon_png = pygame.image.load("moon.png")
planet_png = pygame.image.load("planet.png")


            
            
def blit_body(body,screen):
    posx,posy=body.pos
    width,height=body.surf.get_rect().size
    pos=posx-width/2,posy-height/2
    rot=body.surf
    angle = gravity.get_angle(body)
    if angle:
        rot=pygame.transform.rotate(body.surf,angle)
    screen.blit(rot,pos)

earth=gravity.planet((320,240),20,100000)
earth.surf=pygame.transform.scale(planet_png,(300,300))

moon=gravity.small_body((320,240-200),(25,0))
moon.surf=pygame.transform.scale(moon_png,(50,50))

arrow=gravity.small_body((320-170,240),(0,-25))
arrow.surf=arrow_png
arrow.orient="speed"

human=gravity.small_body((320+200,240),(0,-25))
human.surf=human_png
human.orient="-acceleration"

planets = [earth]
bodies = [moon,arrow,human]

while mainloop:
    tick_time = clock.tick(30)
    screen.fill((50,50,75))
    gravity.simulate(planets,bodies,tick_time/1000.0)
    for b in bodies:
        blit_body(b,screen)
    for b in planets:
        blit_body(b,screen)
    pygame.display.flip()
    pygame.display.update()
