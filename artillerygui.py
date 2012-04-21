import pygame,math,random
from pygame.locals import *
import gravity

# HACK: uncomment this line only on win32 when packaging
# import pygame._view # for py2exe

pygame.init()


mainloop=True
clock = pygame.time.Clock() # create clock object

screen = pygame.display.set_mode([640,480],pygame.DOUBLEBUF)
screen.fill([0,0,0])
pygame.key.set_repeat(1, 1)

aim_png = pygame.image.load("aim.png")

human_png = pygame.image.load("stick.png")
arrow_png = pygame.image.load("arrow.png")
rocket_png = pygame.image.load("rocket.png")
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

earth=pygame.sprite.DirtySprite()
earth.physics=gravity.planet((240,240),20,4*1000*1000)
earth.image_orig=pygame.transform.scale(planet_png,(200,200))
earth.image=earth.image_orig
earth.rect=earth.image.get_rect()
earth.rect.center=(240,240)

moon=pygame.sprite.DirtySprite()
moon.physics=gravity.planet((390,90),20,400*1000)
moon.image_orig=pygame.transform.scale(moon_png,(80,80))
moon.image=moon.image_orig
moon.rect=moon.image.get_rect()
moon.rect.center=(390,90)

moon2=pygame.sprite.DirtySprite()
moon2.physics=gravity.planet((550,290),20,200*1000)
moon2.image_orig=pygame.transform.scale(moon_png,(50,50))
moon2.image=moon2.image_orig
moon2.rect=moon.image.get_rect()
moon2.rect.center=(550,290)

human=pygame.sprite.DirtySprite()
human.physics=gravity.small_body((590,50),(0,0))
human.image_orig=human_png
human.physics.orient="acceleration"
human.down=-1
human.image=human.image_orig
human.rect=human.image.get_rect()
human.rect.center=(550,50)

# arrow=pygame.sprite.DirtySprite()
# arrow.physics=gravity.small_body((500,250),(0,0))
# arrow.image_orig=arrow_png
# arrow.physics.orient="speed"
# arrow.image=arrow.image_orig
# arrow.rect=arrow.image.get_rect()
# arrow.rect.center=(550,250)

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

planets = [earth.physics,moon.physics,moon2.physics]
bodies = [human.physics]

sprites=[earth,moon,human,moon2]
human.layer=1

spritegroup1=pygame.sprite.Group(human)
spritegroup2=pygame.sprite.Group(moon,earth,moon2)
spritegroup3=pygame.sprite.Group()
layeredgroup=pygame.sprite.LayeredDirty(human,moon,moon2,earth)

font=pygame.font.Font("Ostrich Black.ttf",70)

direction = 0
mode = "walk"
weapon= "bow"
shoot_angle = 0
shoot_time = 0
background=screen.copy()
background.fill((50,50,75))
world=screen.copy()
hud=screen.copy().convert_alpha()

while mainloop:
    tick_time = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop=False
    if not mainloop:
        break
            
    gravity.simulate(planets,bodies,tick_time/1000.0)
    
    keys = pygame.key.get_pressed()
    if mode == "walk":
        if keys[pygame.K_UP] and human.physics.rest==True:
            up=gravity.rot(gravity.orient(human.physics),180)
            human.physics.pos = gravity.add(human.physics.pos,gravity.scale(up,2))
            human.physics.speed = gravity.scale(up,150)
            human.physics.rest=False
            human.dirty=1
        if keys[pygame.K_RETURN] and human.physics.rest==True:
            up=gravity.rot(gravity.orient(human.physics),180)
            human.physics.pos = gravity.add(human.physics.pos,gravity.scale(up,2))
            if direction==0:
                left=gravity.rot(gravity.orient(human.physics),135)
                human.physics.speed=gravity.scale(left,70)
            elif direction==1:
                right=gravity.rot(gravity.orient(human.physics),-135)
                human.physics.speed=gravity.scale(right,70)
            human.physics.rest=False
            human.dirty=1
        if keys[pygame.K_LEFT] and human.physics.rest==True:
            left=gravity.rot(gravity.orient(human.physics),135)
            human.physics.pos = gravity.add(human.physics.pos,gravity.scale(left,2))
            human.physics.rest=False
            direction = 0
            human.dirty=1
        if keys[pygame.K_RIGHT] and human.physics.rest==True:
            right=gravity.rot(gravity.orient(human.physics),-135)
            human.physics.pos = gravity.add(human.physics.pos,gravity.scale(right,2))
            human.physics.rest=False
            direction = 1
            human.dirty=1
        if keys[pygame.K_1] and human.physics.rest==True:
            mode="shoot"
            weapon="bow"
        if keys[pygame.K_2] and human.physics.rest==True:
            mode="shoot"
            weapon="rocket"
    elif mode == "shoot":
        if keys[pygame.K_RETURN]:
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
        if direction==0:
            aim_vec=gravity.rot(gravity.orient(human.physics),90+shoot_angle)
        if direction==1:
            aim_vec=gravity.rot(gravity.orient(human.physics),-(90+shoot_angle))
        if weapon == "bow":
            shoot_vec=gravity.scale(aim_vec,5*shoot_time)
            arrow=pygame.sprite.DirtySprite()
            arrow.layer=2
            arrow.dirty=1
            arrow.physics=gravity.small_body(human.physics.pos,shoot_vec)
            arrow.image_orig=arrow_png
            arrow.physics.orient="speed"
            arrow.image=arrow.image_orig
            arrow.rect=arrow.image.get_rect()
            arrow.rect.center=(550,250)
            spritegroup3.add(arrow)
            layeredgroup.add(arrow)
            bodies.append(arrow.physics)
            sprites.append(arrow)
            shoot_time = 0
            mode = "walk"
        else:
            shoot_vec=gravity.scale(aim_vec,3*shoot_time)
            rocket=pygame.sprite.DirtySprite()
            rocket.layer=2
            rocket.dirty=1
            rocket.physics=gravity.small_body(human.physics.pos,shoot_vec)
            rocket.image_orig=rocket_png
            rocket.physics.orient="speed"
            rocket.image=rocket.image_orig
            rocket.rect=rocket.image.get_rect()
            rocket.rect.center=(550,250)
            rocket.explode=True
            spritegroup3.add(rocket)
            layeredgroup.add(rocket)
            bodies.append(rocket.physics)
            sprites.append(rocket)
            shoot_time = 0
            mode = "walk"
    
    impacts=[]
    collided=pygame.sprite.groupcollide(spritegroup3, spritegroup1, False, False)
    for projectile in collided:
        for player in collided[projectile]:
            contact=pygame.sprite.collide_mask(player,projectile)
            if contact:
                contactpoint=gravity.add(player.rect.topleft,contact)
                if hasattr(projectile, "hit"):
                    projectile.hit(player)

                depth = gravity.dot(gravity.sub(player.rect.center,projectile.rect.center),gravity.orient(projectile.physics))
                if depth>0:
                    projectile.physics.speed=(0,0)
                    projectile.physics.rest=True
                    spritegroup3.remove(projectile)
                    if hasattr(projectile, "explode"):
                        layeredgroup.remove(projectile)
                        sprites.remove(projectile)
                    bodies.remove(projectile.physics)
                    if not projectile in impacts:
                        impacts.append(projectile)

    collided=pygame.sprite.groupcollide(spritegroup3, spritegroup2, False, False)
    for projectile in collided:
        for planet in collided[projectile]:
            contact=pygame.sprite.collide_mask(planet,projectile)
            if contact:
                contactpoint=gravity.add(planet.rect.topleft,contact)
                depth = gravity.dot(gravity.sub(contactpoint,projectile.rect.center),gravity.orient(projectile.physics))
                if depth>0:
                    projectile.physics.speed=(0,0)
                    projectile.physics.rest=True
                    spritegroup3.remove(projectile)
                    if hasattr(projectile, "explode"):
                        sprites.remove(projectile)
                        layeredgroup.remove(projectile)
                    bodies.remove(projectile.physics)
                    if not projectile in impacts:
                        impacts.append(projectile)

                
    collided=pygame.sprite.groupcollide(spritegroup1, spritegroup2, False, False)
    for s1 in collided:
        for s2 in collided[s1]:
            contact=pygame.sprite.collide_mask(s1,s2)
            if contact:
                contactpoint=gravity.add(s1.rect.topleft,contact)
                depth = gravity.dot(gravity.sub(contactpoint,s1.rect.center),gravity.orient(s1.physics))
                s1.physics.speed=(0,0)
                if depth > 0:
                    s1.physics.rest=True

    for projectile in impacts:
        pos = projectile.rect.center
        if hasattr(projectile, "explode"):
            for planet in earth,moon:
                pygame.draw.circle(planet.image_orig, (0,0,0,0), gravity.sub(pos,planet.rect.topleft), 20)
                planet.dirty=1
    
    for sprite in sprites:
        rot_img(sprite)
        sprite.rect.center=sprite.physics.pos
        if not sprite.physics.rest:
            sprite.dirty=1
    
    layeredgroup.draw(world,background)
    screen.blit(world,(0,0))
    hud.fill((0,0,0,0))
    
    if mode == "shoot":
        s = (1 + shoot_time / 3) * 10
        surf=pygame.transform.scale(aim_png,(s,min(32,s)))
        angle=gravity.get_angle(human.physics)
        if direction == 0:
            hud.blit(pygame.transform.rotate(surf,180-shoot_angle+angle),human.rect)
        else:
            hud.blit(pygame.transform.rotate(surf,shoot_angle+angle),human.rect)
        ren = font.render(weapon,1,(255,255,255))
        hud.blit(ren,(10,10))

    screen.blit(hud,(0,0))
    pygame.display.flip()
    pygame.display.update()
