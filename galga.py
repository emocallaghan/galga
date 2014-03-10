# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 16:10:25 2014

@author: eocallaghan
"""

import pygame
from pygame.locals import *
import random
import math
import time

class GalagaModel:
    """ Encodes the game state of Galaga"""
    def __init__(self):
        self.fighter = Fighter()
        self.bullets =[]
        self.basicEnemies = []

    def newBullet():
        self.bullets.append(Bullet())
        
    def update():
        for basicEnemy in self.basicEnemies:
            basicEnemy.update()
        
        for bullet in self.bullets:
            bullet.update()
            
        self.fighter.update()

class BasicEnemy:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.image = pygame.image.load("galgaBasicEnemyShip.jpg")
        self.image.set.set_colorkey(get_at(0,0))

    def update():
        self.x += self.vx
        self.y += self.vy

class Fighter:
    def __init__(self, x, y):
        self.lives(3)
        self.x = x
        self.y = y
        self.image = pygame.image.load("galaga_ship.jpg")
        self.image.set_colorkey(get_at(0,0))

    
    def update(self,x):
        pass
        

class Bullet:
    
    def __init__(self,color,height,width,x,y,vy):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = vy
        
    def update():
        self.y += self.vy

class PyGameWindowView:
    """ A view of Galaga rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        for basicEnemy in self.model.basicEnemies:
            self.drawEnemy(basicEnemy)
            
        for bullet in self.model.bullets:
            self.drawBullet(bullet)

        self.drawFighter(self.model.fighter)
        
        pygame.display.update()
        
    def drawEnemy(basicEnemy):
        screen.blit(basicEnemy.image,(basicEnemy.x,basicEnemy.y)) #blit the enemy image to the screen
        
    def drawBullet(bullet):
        pygame.draw.rect(self.screen, pygame.Color(bullet.color[0], bullet.color[1], bullet.color[2]), pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height))
        
    def drawFighter(fighter):
        fighter.image = pygame.transform.smoothscale(fighter.image, (40,60), DestSurface = None)
        screen.blit(fighter.image,(fighter.x,fighter.y)) #blit the fighter image to the screen
        

class PyGameKeyboardController:
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_a:
            self.model.fighter.x += -20.0
        if event.key == pygame.K_d:
            self.model.fighter.x += 20.0
        if event.key == pygame.K_SPACE:
            self.model.newBullet()    