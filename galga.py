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
        self.fighter = Fighter(350,680)
        self.bullets = []
        self.basicEnemies = []

    def newBullet(self, x,y):
        color = (255,0,0)
        self.bullets.append(Bullet(color,10,5,x,y,-1))
        
    def update(self):
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

    def update(self):
        self.x += self.vx
        self.y += self.vy

class Fighter:
    def __init__(self, x, y):
        self.lives = 3
        self.x = x
        self.y = y
        self.color = (250,250,0)
        self.height = 20
        self.width = 10
        #self.image = pygame.transform.smoothscale(pygame.image.load("galaga_ship.jpg"), (40,60), DestSurface = None)
        self.image = pygame.image.load("galaga_ship.jpg")
        #self.image.set_colorkey(get_at(0,0))

    def update(self):
        return
        

class Bullet:
    
    def __init__(self,color,height,width,x,y,vy):
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = vy
        
    def update(self):
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
        fighter = self.model.fighter
        self.drawFighter(fighter)
        
        pygame.display.update()
        
    def drawEnemy(self, basicEnemy):
        screen.blit(basicEnemy.image,(basicEnemy.x,basicEnemy.y)) #blit the enemy image to the screen
        
    def drawBullet(self, bullet):
        rectangle = pygame.Rect(bullet.x,bullet.y,bullet.width,bullet.height)
        pygame.draw.rect(self.screen, bullet.color, rectangle)
        #pygame.draw.rect(screen, bullet.color, (bullet.height, bullet.width))
        
    def drawFighter(self, fighter):
        rectangle = pygame.Rect(fighter.x,fighter.y,fighter.width,fighter.height)
        pygame.draw.rect(self.screen, fighter.color, rectangle)
        #screen.blit(fighter.image,(fighter.x,fighter.y)) #blit the fighter image to the screen

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
            x = self.model.fighter.x
            y = self.model.fighter.y
            model.newBullet(x,y)    
            

if __name__ == '__main__':
    pygame.init()

    size = (700,700)
    screen = pygame.display.set_mode(size)

    model = GalagaModel()
    view = PyGameWindowView(model,screen)

    KeyBoardcontroller = PyGameKeyboardController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                KeyBoardcontroller.handle_keyboard_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()