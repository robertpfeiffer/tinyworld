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

aim_png = pygame.image.load("aim.png")

human_png = pygame.image.load("stick.png")
arrow_png = pygame.image.load("arrow.png")
rocket_png = pygame.image.load("rocket.png")
moon_png = pygame.image.load("moon.png")
dune_png = pygame.image.load("dune.png")
sickle_png = pygame.image.load("sickle.png")
planet_png = pygame.image.load("planet.png")
bazooka_png =  pygame.image.load("bazooka.png")

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

class Planet(pygame.sprite.DirtySprite):
    def __init__(self,pos,diam,mass,img):
        pygame.sprite.DirtySprite.__init__(self)
        self.physics=gravity.planet(pos,diam,mass)
        img = pygame.transform.scale(img,(2*diam,2*diam))
        self.image_orig=img
        self.image=self.image_orig
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.layer=0

class Player(pygame.sprite.DirtySprite):
    def __init__(self,pos,name):
        pygame.sprite.DirtySprite.__init__(self)
        self.ammo={"bow":5,"bazooka":-1,"rocket":1,"bat":2}
        self.physics=gravity.small_body(pos,(0,0))
        self.physics.orient="acceleration"
        self.name=name
        self.down=-1
        self.image_orig=human_png
        self.image=self.image_orig
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.health=100
        self.invincibletime=0
        self.layer=1

class Arrow(pygame.sprite.DirtySprite):
    def __init__(self,pos,aim,force):
        pygame.sprite.DirtySprite.__init__(self)
        shoot_vec = gravity.scale(aim,5*force)
        self.layer=2
        self.dirty=1
        self.physics=gravity.small_body(pos,shoot_vec)
        self.image_orig=arrow_png
        self.physics.orient="speed"
        self.image=self.image_orig
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.name="arrow"
        self.dmg=45
        self.hit=True

class Rocket(pygame.sprite.DirtySprite):
    def __init__(self,pos,aim,force):
        pygame.sprite.DirtySprite.__init__(self)
        shoot_vec = gravity.scale(aim,10*force)
        self.layer=2
        self.dirty=1
        self.physics=gravity.small_body(pos,shoot_vec)
        self.image_orig=rocket_png
        self.physics.orient="speed"
        self.image=self.image_orig
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.name="rocket"
        self.dmg=50
        self.explode=True

class Bazooka(pygame.sprite.DirtySprite):
    def __init__(self,pos,aim,force):
        pygame.sprite.DirtySprite.__init__(self)
        shoot_vec = gravity.scale(aim,3*force)
        self.layer=2
        self.dirty=1
        self.physics=gravity.small_body(pos,shoot_vec)
        self.image_orig=bazooka_png
        self.physics.orient="speed"
        self.image=self.image_orig
        self.rect=self.image.get_rect()
        self.rect.center=pos
        self.name="bazooka"
        self.dmg=30
        self.explode=True

logo=pygame.transform.scale(pygame.image.load("logo.png"),(640,480))
screen.blit(logo, (0,0))
pygame.display.flip()

for i in range(2*30):
    clock.tick(30)
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        break

intro=pygame.image.load("intro.png")
screen.blit(intro, (0,0))
pygame.display.flip()

for i in range(20*30):
    clock.tick(30)
    pygame.event.pump()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        break

pygame.key.set_repeat(1, 1)

newgame = True
while newgame:
 newgame = False
 
 earth=Planet((240,240),110,4*1000*1000,dune_png)
 moon=Planet((430,90),50,400*1000,sickle_png)
 moon2=Planet((550,290),25,200*1000,moon_png)

 #earth=Planet((240,240),100,4*1000*1000,planet_png)
 #moon=Planet((430,90),40,400*1000,moon_png)
 #moon2=Planet((550,290),25,200*1000,moon_png)

 player1=Player((590,50),"one")
 player2=Player((10,50),"two")

 spritegroup1=pygame.sprite.Group(player1,player2)
 playersgroup=spritegroup1
 spritegroup2=pygame.sprite.Group(moon,earth,moon2)
 planetgroup=spritegroup2
 spritegroup3=pygame.sprite.Group()
 foregroundgroup=spritegroup3
 layeredgroup=pygame.sprite.LayeredDirty(player1,player2,moon,moon2,earth)

 font=pygame.font.Font("Ostrich Black.ttf",70)
 font2=pygame.font.Font("orbitron-black.ttf",20)

 direction = 0
 mode = "walk"
 weapon= "bow"
 shoot_angle = 0
 shoot_time = 0
 background=screen.copy()
 background.fill((50,50,75))
 world=screen.copy()
 hud=screen.copy().convert_alpha()

 currentplayer = player1
 otherplayer = player2

 turn_begin=pygame.time.get_ticks()
 wait_begin=pygame.time.get_ticks()

 while mainloop:
    tick_time = clock.tick(30)
    turn_remain=(turn_begin+90000-pygame.time.get_ticks())/1000
    wait_remain=(wait_begin+10000-pygame.time.get_ticks())/1000

    for sprite in layeredgroup.sprites():
        if not sprite.physics.rest:
            sprite.dirty=1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop=False
    if not mainloop:
        break
            
    planets = [sprite.physics for sprite in planetgroup]
    bodies = [player.physics for player in playersgroup]+[f.physics for f in foregroundgroup]

    gravity.simulate(planets,bodies,tick_time/1000.0)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_n] and mode=="over":
        newgame=True
        break

    if keys[pygame.K_q] and mode=="over":
        newgame=False
        break

    if mode == "walk":
        if keys[pygame.K_UP] and currentplayer.physics.rest==True:
            up=gravity.rot(gravity.orient(currentplayer.physics),180)
            currentplayer.physics.pos = gravity.add(currentplayer.physics.pos,gravity.scale(up,2))
            currentplayer.physics.speed = gravity.scale(up,150)
            currentplayer.physics.rest=False
            currentplayer.dirty=1
        if keys[pygame.K_RETURN] and currentplayer.physics.rest==True:
            up=gravity.rot(gravity.orient(currentplayer.physics),180)
            currentplayer.physics.pos = gravity.add(currentplayer.physics.pos,gravity.scale(up,2))
            if direction==0:
                left=gravity.rot(gravity.orient(currentplayer.physics),135)
                currentplayer.physics.speed=gravity.scale(left,80)
            elif direction==1:
                right=gravity.rot(gravity.orient(currentplayer.physics),-135)
                currentplayer.physics.speed=gravity.scale(right,80)
            currentplayer.physics.rest=False
            currentplayer.dirty=1
        if keys[pygame.K_LEFT] and currentplayer.physics.rest==True:
            left=gravity.rot(gravity.orient(currentplayer.physics),135)
            currentplayer.physics.pos = gravity.add(currentplayer.physics.pos,gravity.scale(left,2))
            currentplayer.physics.rest=False
            direction = 0
            currentplayer.dirty=1
        if keys[pygame.K_RIGHT] and currentplayer.physics.rest==True:
            right=gravity.rot(gravity.orient(currentplayer.physics),-135)
            currentplayer.physics.pos = gravity.add(currentplayer.physics.pos,gravity.scale(right,2))
            currentplayer.physics.rest=False
            direction = 1
            currentplayer.dirty=1
        if keys[pygame.K_1] and currentplayer.physics.rest==True:
            if currentplayer.ammo["bow"]!=0:
                mode="shoot"
                weapon="bow"
        if keys[pygame.K_2] and currentplayer.physics.rest==True:
            if currentplayer.ammo["bazooka"]!=0:
                mode="shoot"
                weapon="bazooka"
        if keys[pygame.K_3] and currentplayer.physics.rest==True:
            if currentplayer.ammo["rocket"]!=0:
                mode="shoot"
                weapon="rocket"
        if keys[pygame.K_4] and currentplayer.physics.rest==True:
            if currentplayer.ammo["bat"]!=0:
                mode="shoot"
                weapon="bat"
    elif mode == "shoot":
        if keys[pygame.K_q]:
            mode="walk"
        if keys[pygame.K_UP]:
            if shoot_angle < 90:
                shoot_angle += 2.5
        if keys[pygame.K_LEFT]:
            direction=0
        if keys[pygame.K_RIGHT]:
            direction=1
        if keys[pygame.K_DOWN]:
            if shoot_angle > - 90:
                shoot_angle -= 2.5
        if keys[pygame.K_SPACE]:
            if shoot_time < 60:
                shoot_time += 1
    elif mode == "wait":
        if wait_remain <= 0:
            currentplayer,otherplayer=otherplayer,currentplayer
            turn_begin=pygame.time.get_ticks()
            turn_remain=90
            shoot_angle=0
            mode="walk"

    if turn_remain <= 0 and mode != "wait":
        mode = "wait"
        wait_begin=pygame.time.get_ticks()

    for player in playersgroup.sprites():
        if player.invincibletime > 0:
            player.invincibletime -=1

    if mode == "walk":
        shoot_time=0
    if (shoot_time > 0
        and not keys[pygame.K_SPACE] 
        and mode == "shoot"):
        projectile = None
        if direction==0:
            aim_vec=gravity.rot(gravity.orient(currentplayer.physics),
                                90+shoot_angle)
        if direction==1:
            aim_vec=gravity.rot(gravity.orient(currentplayer.physics),
                               -(90+shoot_angle))
        if weapon == "bow":
            projectile=Arrow(currentplayer.physics.pos,
                        aim_vec,
                        shoot_time)
        elif weapon == "bazooka":
            projectile=Bazooka(currentplayer.physics.pos,
                          aim_vec,
                          shoot_time)
        elif weapon == "rocket":
            projectile=Rocket(currentplayer.physics.pos,
                          aim_vec,
                          shoot_time)
        currentplayer.ammo[weapon]-=1
        if projectile:
            spritegroup3.add(projectile)
            layeredgroup.add(projectile)
        if weapon == "bat":
            if gravity.length(
                gravity.sub(currentplayer.physics.pos,
                            otherplayer.physics.pos)) < 20:
                otherplayer.physics.speed=gravity.scale(aim_vec,180)
                otherplayer.physics.rest=False
                otherplayer.health-=25
        shoot_time = 0
        mode = "wait"
        wait_begin=pygame.time.get_ticks()
        currentplayer.invincibletime=50
    
    impacts=[]
    collided=pygame.sprite.groupcollide(foregroundgroup, playersgroup, False, False)
    for projectile in collided:
        for player in collided[projectile]:
            contact=pygame.sprite.collide_mask(player,projectile)
            if contact and not player.invincibletime:
                contactpoint=gravity.add(player.rect.topleft,contact)
                if hasattr(projectile, "hit"):
                    player.health -= projectile.dmg                
                projectile.physics.speed=(0,0)
                projectile.physics.rest=True
                spritegroup3.remove(projectile)
                layeredgroup.remove(projectile)
                if not projectile in impacts:
                    impacts.append(projectile)

    collided=pygame.sprite.groupcollide(foregroundgroup, planetgroup, False, False)
    for projectile in collided:
        for planet in collided[projectile]:
            contact=pygame.sprite.collide_mask(planet,projectile)
            if contact:
                contactpoint=gravity.add(planet.rect.topleft,contact)
                projectile.physics.speed=(0,0)
                projectile.physics.rest=True
                spritegroup3.remove(projectile)
                if hasattr(projectile, "explode"):
                    layeredgroup.remove(projectile)
                if not projectile in impacts:
                    impacts.append(projectile)

    for player in playersgroup.sprites():
        player.physics.rest=False
                
    collided=pygame.sprite.groupcollide(playersgroup, planetgroup, False, False)
    for s1 in collided:
        for s2 in collided[s1]:
            contact=pygame.sprite.collide_mask(s1,s2)
            if contact:
                contactpoint=gravity.add(s1.rect.topleft,contact)
                v2 = gravity.orient(s1.physics)
                if gravity.length(s1.physics.speed) > 2:
                    v2 = s1.physics.speed
                depth = gravity.dot(gravity.sub(contactpoint,s1.rect.center),v2)
                if depth > 0:
                    s1.physics.speed=(0,0)
                    s1.physics.rest=True

    for projectile in set(impacts):
        pos = projectile.rect.center
        if hasattr(projectile, "explode"):
            for planet in planetgroup.sprites():
                pygame.draw.circle(planet.image_orig, (0,0,0,0), gravity.sub(pos,planet.rect.topleft), projectile.dmg/2)
                planet.dirty=1
            for player in playersgroup.sprites():
                distancev = gravity.sub(player.physics.pos,pos)
                distance = gravity.length(distancev)
                distance = max(1,distance - 15)
                damage = max(0, int(projectile.dmg/distance**0.5) - int(distance/10))
                
                if damage:
                    force = gravity.norm(distancev, min(damage*10, 200))
                    player.physics.rest=False
                    player.physics.speed = gravity.add(force,player.physics.speed)
                    player.health -= damage
    
    for sprite in layeredgroup.sprites():
        rot_img(sprite)
        sprite.rect.center=sprite.physics.pos

    for sprite in layeredgroup.sprites():
        if not sprite.physics.rest:
            sprite.dirty=1
    
    layeredgroup.draw(world,background)
    screen.blit(world,(0,0))
    hud.fill((0,0,0,0))
    
    if mode == "shoot":
        s = (4 + shoot_time / 3) * 10
        surf=pygame.transform.scale(aim_png,(s,min(32,s)))
        angle=gravity.get_angle(currentplayer.physics)
        if direction == 0:
            ov = pygame.transform.rotate(surf,180-shoot_angle+angle)
            r = ov.get_rect()
            r.center = currentplayer.rect.center
            hud.blit(ov,r.topleft)
        else:
            ov = pygame.transform.rotate(surf,shoot_angle+angle)
            r = ov.get_rect()
            r.center = currentplayer.rect.center
            hud.blit(ov,r.topleft)
        weapon_hud=weapon
        if currentplayer.ammo[weapon] > 0:
            weapon_hud += " x"+str(currentplayer.ammo[weapon])
        ren = font2.render(weapon_hud,1,(255,255,255))
        hud.blit(ren,(10,30))

    for player in playersgroup.sprites():
        pos = player.physics.pos
        phealth = font2.render(str(player.health),1,(255,255,255))    
        hud.blit(phealth,gravity.sub(pos,(10,30)))
        dist = gravity.length(gravity.sub((320,240),pos))
        if dist > 1000:
            player.health -= 1
    
    for projectile in foregroundgroup.sprites():
        pos = projectile.physics.pos
        dist = gravity.length(gravity.sub((320,240),pos))
        if dist > 2000:
            foregroundgroup.remove(projectile)
            layeredgroup.remove(projectile)

    if mode == "wait":
        turn = font2.render("waiting "+\
                        " "+str(wait_remain)+"s",1,(255,255,255))
    elif mode == "walk" or mode == "shoot":
        turn = font2.render(currentplayer.name+"s turn"+\
                        " "+str(turn_remain)+"s",1,(255,255,255))

    if not mode == "over":
        hud.blit(turn,(10,10))

    if player1.health > 0 and 1 > player2.health:
        ren = font.render("PLAYER ONE WINS",1,(255,55,55))
        hud.blit(ren,(100,200))
        mode = "over"
    if player2.health > 0 and 1 > player1.health:
        ren = font.render("PLAYER TWO WINS",1,(255,55,55))
        hud.blit(ren,(100,200))
        mode = "over"
    if (player2.health < 1) and (1 > player1.health):
        ren = font.render("DRAW",1,(255,55,55))
        hud.blit(ren,(100,200))
        mode= "over"

    if mode == "over":
        ren = font2.render("press N for new game, Q to quit"
                           ,1,(255,255,255))
        hud.blit(ren,(100,250))

    screen.blit(hud,(0,0))
    pygame.display.flip()
    pygame.display.update()
