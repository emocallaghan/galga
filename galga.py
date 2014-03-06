# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 16:10:25 2014

@author: eocallaghan
"""

import pygame
from pygame.locals import *

class GalagaModel:
    def __init__(self):
        self.fighter = Fighter()
        self.bullets =[]
        self.basicEnemies = []
    def newBullet():
        self.bullets.append(Bullet())
        
class BasicEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Fighter:
    def __init__(self):
        self.lives(3)
        self.vx = 0.0
        

class Bullet:
    def __init__(self,color,height,width,x,y):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y

class PyGameWindowView:
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for bullet in self.model.bullets:
            pygame.draw.rect(self.screen, pygame.Color(bullet.color[0],bullet.color[1],bullet.color[2]),pygame.Rect(bullet.x,bullet.y,bullet.width,bullet.height))  
        pygame.display.update()

class PyGameKeyboardController:
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_a:
            self.model.fighter.vx += -1.0
        if event.key == pygame.K_d:
            self.model.fighter.vx += 1.0
        if event.key == pygame.K_SPACE:
            self.model.newBullet()

    
    