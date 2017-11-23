#!/usr/bin/python3

import pygame, os
from pygame.locals import *

pygame.init()

fenetre = pygame.display.set_mode((640, 480), RESIZABLE)
pygame.display.set_caption("Cayo Ken")
clock = pygame.time.Clock()


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
        image = pygame.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images

class anim(pygame.sprite.Sprite):

    def __init__(self, position, images):
        size = (32, 32)  # This should match the size of the images.


        self.test = pygame.sprite.Sprite()
        self.test.rect = pygame.Rect(position, size)

        self.images = images
        self.images_right = images
        self.images_left = [pygame.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.image_jump = pygame.image.load("jump.png").convert_alpha()
        self.image_jump_r = self.image_jump
        self.image_jump_l = pygame.transform.flip(self.image_jump, True, False)
        self.index = 0
        self.test.image = images[self.index]  # 'image' is the current image of the animation.
        self.velocityx = 1.75
        self.vy = 0.0
        self.vx = 0.0
        self.velocityy = 0.0
        self.test.mask = pygame.mask.from_surface(self.test.image)

        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = 6
        self.current_frame = 0

    def update_frame_dependent(self, dt):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        if self.vx > 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
            self.image_jump = self.image_jump_r
        elif self.vx < 0:
            self.images = self.images_left
            self.image_jump = self.image_jump_l

        self.current_time += dt
        if self.vx == 0 and self.vy == 0 and self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = 0
            self.test.image = self.images[self.index]
        elif self.vy != 0 and self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = 0
            self.test.image = self.image_jump
        elif self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.test.image = self.images[self.index]

        #self.test.rect = self.test.rect.move(self.vx, 0)

    def update(self, dt):
        self.update_frame_dependent(dt)

images = load_images(path='temp')  # Make sure to provide the relative or full path to the images directory.
player = anim(position=(640/2, 640/2), images=images)
jump = False
falling = False
time = 0
want_jump = False
ap_l, ap_r = False, False
move_decor = 0

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
                want_jump = True
                player.vy = 2.5

        elif event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                player.vx = 0
                move_decor = 0
                ap_l = False
                ap_r = False


    if pygame.sprite.collide_mask(cote_r, player.test):
        if player.vx < 0:
            move_decor = 0
    elif ap_l == True:
        move_decor = 2

    if pygame.sprite.collide_mask(cote_l, player.test):
        if player.vx > 0:
            move_decor = 0
    elif ap_r == True:
        move_decor = -2

    if pygame.sprite.collide_mask(fond, player.test):
        if jump == True:
            player.vy = -1
            falling = True
            jump = False

    if falling == True:
        player.velocityy -= 1.0 * 1/60
        player.velocityy += player.vy
        player.test.rect.y -= player.vy

    if pygame.sprite.collide_mask(sol, player.test):
        if jump == True and want_jump == False:
            jump = False
        falling= False
        time = 0
        if want_jump == False:
            player.vy = 0
        player.test.rect.y = player.test.rect.y

    elif jump == False:
        player.vy -= 1.8 * 1/60
        player.velocityy += player.vy
        player.test.rect.y -= player.vy

    if jump == True and falling == False: # SI LE JOUEUR EST EN TRAIN DE SAUTER
        player.vy -= 1.8 * 1/60
        player.velocityy += player.vy
        player.test.rect.y -= player.vy
        time += 1

    if time > 5:
        want_jump = False

    for decor in groupe.sprites():
        decor.rect = decor.rect.move(move_decor, 0)
    player.update(dt)
    fenetre.blit(ciel, (0,0))
    #fenetre.blit(sol.image, (0,0))
    #fenetre.blit(fond.image, (0,0))
    groupe.update()
    #groupe.draw(fenetre)
    fenetre.blit(player.test.image, player.test.rect)
    pygame.display.flip()

pygame.quit()
