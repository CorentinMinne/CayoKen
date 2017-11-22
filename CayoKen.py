#!/usr/bin/python3

import pygame, os
from pygame.locals import *

pygame.init()

fenetre = pygame.display.set_mode((640, 480), RESIZABLE) 
pygame.display.set_caption("Cayo Ken")


ciel = pygame.image.load("cuiel").convert_alpha()


sol = pygame.sprite.Sprite()
sol.image = pygame.image.load("sol.png").convert_alpha()
sol.rect = sol.image.get_rect()
sol.mask = pygame.mask.from_surface(sol.image)


fond = pygame.sprite.Sprite()
fond.image = pygame.image.load("fond.png").convert_alpha()
fond.rect = fond.image.get_rect()
fond.mask = pygame.mask.from_surface(fond.image)

done = False 

def load_images(path):
    images = []
    for file_name in os.listdir(path):
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

    def update_frame_dependent(self):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        if self.vx > 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
            self.image_jump = self.image_jump_r
        elif self.vx < 0:
            self.images = self.images_left
            self.image_jump = self.image_jump_l

        self.current_frame += 1
        if self.vx == 0 and self.vy == 0 and self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = 0
            self.test.image = self.images[self.index]
        elif self.vy != 0 and self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = 0
            self.test.image = self.image_jump
        elif self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.test.image = self.images[self.index]
        
        self.test.rect = self.test.rect.move(self.vx, 0)

    def update(self, dt):
        self.update_frame_dependent()

images = load_images(path='temp')  # Make sure to provide the relative or full path to the images directory.
player = anim(position=(100, 0), images=images)
jump = False
time = 0
want_jump = False

while not done:

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
               player.vx = player.velocityx
            elif event.key == K_LEFT:
                player.vx = -player.velocityx
            elif event.key == K_UP and jump == False:
                jump = True
                want_jump = True
                player.vy = 2.5
        
        elif event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_LEFT:
                player.vx = 0
    
    if pygame.sprite.collide_mask(fond, player.test):
        if jump == True:
            player.vy = 0
            jump = False
        player.velocityy -= 1.8 * 1/60
        player.velocityy += player.vy
        player.test.rect.y -= player.vy

    if pygame.sprite.collide_mask(sol, player.test):
        if jump == True and want_jump == False:
            jump = False
        time = 0
        if want_jump == False:
            player.vy = 0
        player.test.rect.y = player.test.rect.y
        
    elif jump == False:
        print ("RIEN")
        player.vy -= 1.8 * 1/60
        player.velocityy += player.vy
        player.test.rect.y -= player.vy
      
        
    if jump == True: # SI LE JOUEUR EST EN TRAIN DE SAUTER
        player.vy -= 1.8 * 1/60
        player.velocityy += player.vy
        player.test.rect.y -= player.vy
        time += 1
        
    if time > 5:
        want_jump = False
        
    player.update(60)
    fenetre.blit(ciel, (0,0))
    fenetre.blit(sol.image, (0,0))
    fenetre.blit(fond.image, (0,0))
    fenetre.blit(player.test.image, player.test.rect)    
    pygame.display.flip()

pygame.quit()