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

aim_png = pygame.image.load("aim.png")

human_png = pygame.image.load("stick.png")
arrow_png = pygame.image.load("arrow.png")
moon_png = pygame.image.load("moon.png")
planet_png = pygame.image.load("planet.png")
            
# def blit_body(body,screen):
#     posx,posy=body.pos
#     width,height=body.surf.get_rect().size
#     pos=posx-width/2,posy-height/2
#     rot=body.surf
#     angle = gravity.get_angle(body)
#     if angle:
#         rot=pygame.transform.rotate(body.surf,angle)
#     screen.blit(rot,pos)

def rot_img(sprite):
    angle = gravity.get_angle(sprite.physics)
    if angle:
        if hasattr(sprite,"down") and sprite.down==-1:
            angle+=180
        sprite.image=pygame.transform.rotate(sprite.image_orig,angle)
        sprite.mask=pygame.mask.from_surface(sprite.image)
        center=sprite.rect.center
        sprite.rect=sprite.image.get_rect()
        sprite.rect.center=center

earth=pygame.sprite.Sprite()
earth.physics=gravity.planet((240,240),20,4*1000*1000)
earth.image_orig=pygame.transform.scale(planet_png,(300,300))
earth.image=earth.image_orig
earth.rect=earth.image.get_rect()
earth.rect.center=(240,240)

moon=pygame.sprite.Sprite()
moon.physics=gravity.planet((490,90),20,200*1000)
moon.image_orig=pygame.transform.scale(moon_png,(50,50))
moon.image=moon.image_orig
moon.rect=moon.image.get_rect()
moon.rect.center=(450,90)

human=pygame.sprite.Sprite()
human.physics=gravity.small_body((590,50),(0,0))
human.image_orig=human_png
human.physics.orient="acceleration"
human.down=-1
human.image=human.image_orig
human.rect=human.image.get_rect()
human.rect.center=(550,50)

arrow=pygame.sprite.Sprite()
arrow.physics=gravity.small_body((500,250),(0,0))
arrow.image_orig=arrow_png
arrow.physics.orient="speed"
arrow.image=arrow.image_orig
arrow.rect=arrow.image.get_rect()
arrow.rect.center=(550,250)

#earth=gravity.planet((320,240),20,100000)
#earth.surf=pygame.transform.scale(planet_png,(300,300))

#moon=gravity.small_body((320,240-200),(25,0))
#moon.surf=pygame.transform.scale(moon_png,(50,50))

#arrow=gravity.small_body((320-170,240),(0,-25))
#arrow.surf=arrow_png
#arrow.orient="speed"

#human=gravity.small_body((320+200,240),(0,-25))
#human.surf=human_png
#human.orient="-acceleration"

planets = [earth.physics,moon.physics]
bodies = [human.physics]

sprites=[earth,moon,human,arrow]

spritegroup1=pygame.sprite.Group(human,arrow)
spritegroup2=pygame.sprite.Group(moon,earth)
direction = 0
mode = "walk"
shoot_angle = 0
shoot_time = 0

while mainloop:
    tick_time = clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop=False
    if not mainloop:
        break
            
    screen.fill((50,50,75))
    gravity.simulate(planets,bodies,tick_time/1000.0)
    
    keys = pygame.key.get_pressed()
    if mode == "walk":
        if keys[pygame.K_UP] and human.physics.rest==True:
            up=gravity.rot(gravity.orient(human.physics),180)
            
            human.physics.pos = gravity.add(human.physics.pos,gravity.scale(up,2))
            human.physics.speed = gravity.scale(up,150)
            human.physics.rest=False

        if keys[pygame.K_RETURN] and human.physics.rest==True:
            x,y=gravity.orient(human.physics)
            
            human.physics.pos = gravity.add(human.physics.pos,(2*-x,2*-y))
            if direction==0:
                human.physics.speed=(70*(-y-x),70*(x-y))
            elif direction==1:
                human.physics.speed=(70*(y-x),70*(-x-y))
            human.physics.rest=False
        if keys[pygame.K_LEFT] and human.physics.rest==True:
            left=gravity.rot(gravity.orient(human.physics),-135)
            human.physics.pos = gravity.add(human.physics.pos,gravity.scale(left,2))
            human.physics.rest=False
            direction = 0
        if keys[pygame.K_RIGHT] and human.physics.rest==True:
            right=gravity.rot(gravity.orient(human.physics),135)
            human.physics.pos = gravity.add(human.physics.pos,gravity.scale(right,2))
            human.physics.rest=False
            direction = 1
        if keys[pygame.K_MINUS] and human.physics.rest==True:
            mode="shoot"
    elif mode == "shoot":
        if keys[pygame.K_PLUS]:
            mode="walk"
        if keys[pygame.K_UP]:
            if shoot_angle < 90:
                shoot_angle += 2.5
        if keys[pygame.K_DOWN]:
            if shoot_angle > - 90:
                shoot_angle -= 2.5
        if keys[pygame.K_SPACE]:
            if shoot_time < 60:
                shoot_time += 1

    if mode == "walk":
        shoot_time=0
    if (shoot_time > 0 
        and not keys[pygame.K_SPACE] 
        and mode == "shoot"):
        arrow=pygame.sprite.Sprite()
        arrow.physics=gravity.small_body(gravity.add(human.physics.pos,(10*(-y-x),10*(x-y))),(0,0))
        arrow.image_orig=arrow_png
        arrow.physics.orient="speed"
        arrow.image=arrow.image_orig
        arrow.rect=arrow.image.get_rect()
        arrow.rect.center=(550,250)

        shoot_time = 0

    collided=pygame.sprite.groupcollide(spritegroup1, spritegroup2, False, False)
    for s1 in collided:
        for s2 in collided[s1]:
            contact=pygame.sprite.collide_mask(s1,s2)
            if contact:
                contactpoint=gravity.add(s1.rect.topleft,contact)
                depth = gravity.dot(gravity.sub(contactpoint,s1.rect.center),gravity.orient(s1.physics))
                if depth > 0:
                    s1.physics.speed=(0,0)
                    s1.physics.rest=True

    for sprite in sprites:
        rot_img(sprite)
        sprite.rect.center=sprite.physics.pos

    spritegroup2.draw(screen)
    spritegroup1.draw(screen)

    if mode == "shoot":
        s = (1 + shoot_time / 3) * 10
        surf=pygame.transform.scale(aim_png,(s,min(32,s)))
        angle=gravity.get_angle(human.physics)
        screen.blit(pygame.transform.rotate(surf,180-shoot_angle+angle),human.rect)

    pygame.display.flip()
    pygame.display.update()
