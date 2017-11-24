#!/usr/bin/python3

import pygame, os
from pygame.locals import *

pygame.init()

fenetre = pygame.display.set_mode((640, 480), RESIZABLE)
pygame.display.set_caption("Cayo Ken")
clock = pygame.time.Clock()
jump = False
falling = False
time = 0
want_jump = False
ap_l, ap_r = False, False
move_decor = 0

ciel = pygame.image.load("cuiel").convert_alpha()


sol = pygame.sprite.Sprite()
sol.image = pygame.image.load("sol.png").convert_alpha()
sol.rect = sol.image.get_rect()
sol.mask = pygame.mask.from_surface(sol.image)

cote_r = pygame.sprite.Sprite()
cote_r.image = pygame.image.load("cote_r.png").convert_alpha()
cote_r.rect = cote_r.image.get_rect()
cote_r.mask = pygame.mask.from_surface(cote_r.image)

cote_l = pygame.sprite.Sprite()
cote_l.image = pygame.image.load("cote_l.png").convert_alpha()
cote_l.rect = cote_l.image.get_rect()
cote_l.mask = pygame.mask.from_surface(cote_l.image)

fond = pygame.sprite.Sprite()
fond.image = pygame.image.load("fond.png").convert_alpha()
fond.rect = fond.image.get_rect()
fond.mask = pygame.mask.from_surface(fond.image)

groupe = pygame.sprite.Group(fond, cote_l, sol, cote_r)

done = False

def load_images(path):
    images = []
    files = []
    for file_name in os.listdir(path):
        files.append(file_name)
    files = sorted(files)
    for file_name in files:
        image = pygame.image.load(path + os.sep + file_name).convert_alpha()
        image = pygame.transform.scale(image, (72, 72))
        images.append(image)
    return images

class anim(pygame.sprite.Sprite):

    def __init__(self, position, images):
        size = (72, 72)  # This should match the size of the images.
        self.sprite = pygame.sprite.Sprite()
        self.sprite.rect = pygame.Rect(position, size)

        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.image_jump = pygame.image.load("jump.png").convert_alpha()
        self.image_jump = pygame.transform.scale(self.image_jump, (72, 72))
        self.image_jump_r = self.image_jump
        self.image_jump_l = pygame.transform.flip(self.image_jump, True, False)
        self.index = 0
        self.sprite.image = images[self.index]  # 'image' is the current image of the animation.
        self.velocityx = 1.75
        self.vy = 0.0
        self.vx = 0.0
        self.velocityy = 0.0
        self.sprite.mask = pygame.mask.from_surface(self.sprite.image)
        self.animation_time = 0.05
        self.current_time = 0

        self.on_ground = False

    def update_frame_dependent(self, dt):
        if self.vx > 0:
            self.images = self.images_right
            self.image_jump = self.image_jump_r
        elif self.vx < 0:
            self.images = self.images_left
            self.image_jump = self.image_jump_l

        self.current_time += dt

        if self.vx == 0 and self.vy == 0 and self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = 0
            self.sprite.image = self.images[self.index]
        elif self.vy != 0 and self.on_ground == False and self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = 0
            self.sprite.image = self.image_jump
        elif self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            if self.index == 0:
                self.index = 1
            self.sprite.image = self.images[self.index]

    def update(self, dt):
        self.update_frame_dependent(dt)

    def check_collision(self):
        global jump, move_decor, ap_r, ap_l, cote_r, cote_l, fond, sol, want_jump, falling, time

        col_right = pygame.sprite.collide_mask(cote_r, self.sprite)
        col_left = pygame.sprite.collide_mask(cote_l, self.sprite)
        col_sol = pygame.sprite.collide_mask(sol, self.sprite)
        col_plat = pygame.sprite.collide_mask(fond, self.sprite)

        if col_right:
            if self.vx < 0:
                move_decor = 0

        elif col_left:
            if self.vx > 0:
                move_decor = 0

        elif col_plat:
            if jump == True:
                self.vy = -1
                falling = True
                jump = False

        elif col_sol:
            if jump == True and want_jump == False:
                jump = False
            falling = False
            time = 0
            if want_jump == False:
                self.vy = 0
                self.on_ground = True
            self.sprite.rect.y = self.sprite.rect.y

        if col_sol == col_plat == col_left == col_right == None:
            falling = True
            self.on_ground = False
        if col_left == None and ap_r == True:
            move_decor = -2
        if col_right == None and ap_l == True:
            move_decor = 2
            
images = load_images(path='temp')  # Make sure to provide the relative or full path to the images directory.
player = anim(position=(640/2, 100), images=images)

while not done:

    dt = clock.tick(120) / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                move_decor = -2
                player.vx = player.velocityx
                ap_r = True
            elif event.key == K_LEFT:
                move_decor = 2
                player.vx = -player.velocityx
                ap_l = True
            elif event.key == K_UP and jump == False and falling == False:
                jump = True
                player.on_ground = False
                want_jump = True
                player.vy = 2.5

        elif event.type == KEYUP:
            if event.key == K_RIGHT:
                ap_r = False
            if event.key == K_LEFT:
                ap_l = False
            if ap_l == ap_r == False:
                player.vx = 0
                move_decor = 0

    player.check_collision()

    if falling == True:
        player.vy -= 2 * 1/60
        player.velocityy += player.vy
        player.sprite.rect.y -= player.vy

    if jump == True and falling == False:
        player.vy -= 1.8 * 1/60
        player.velocityy += player.vy
        player.sprite.rect.y -= player.vy
        time += 1

    if time >= 0:
        want_jump = False

    for decor in groupe.sprites():
        decor.rect = decor.rect.move(move_decor, 0)

    player.update(dt)
    fenetre.blit(ciel, (0,0))
    groupe.update()
    groupe.draw(fenetre)
    fenetre.blit(player.sprite.image, player.sprite.rect)
    pygame.display.flip()

pygame.quit()
