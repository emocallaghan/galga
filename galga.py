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
        self.fighter = Fighter(350-17,660)
        self.myBullets = []
        self.enemyBullets = []
        self.basicEnemies = []
        self.score = 0
        for x in range(0, 10):
            basicEnemy = BasicEnemy(x+50*x+100, 350)
            self.basicEnemies.append(basicEnemy)

    def newBullet(self, x,y):
        color = (255,0,0)
        self.myBullets.append(Bullet(color,15,5,x,y,-.75))

    def update(self):
        for bullet in self.myBullets:
            bullet.update()
        for bullet in self.enemyBullets:
            bullet.update()
            
        for basicEnemy in self.basicEnemies:
            basicEnemy.update()
            if (basicEnemy.y > 700):
                basicEnemy.y = 0
        self.fighter.update()
        
    def shoot(self, enemy):
        color = (255, 255, 255)
        bullet = Bullet(color, 15,5,enemy.x+enemy.width/2,enemy.y+enemy.height,.75)
        self.enemyBullets.append(bullet)
        enemy.lastShootTime = time.time()

class BasicEnemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.height = 35
        self.width = 31
        self.color = (255,255,255)
        self.vx = 0
        self.vy = 0
        self.image = pygame.image.load("galgaBasicEnemyShip.jpg")
        self.lastShootTime = time.time()

    def update(self):
        self.x += self.vx
        self.y += self.vy

class Fighter:

    def __init__(self, x, y):
        self.lives = 1
        self.x = x
        self.y = y
        self.vx = 0.0
        self.color = (250,250,0)
        self.height = 40
        self.width = 34
        self.image = pygame.image.load("galaga_ship.jpg")

    def update(self):
        if (self.x == 0 and self.vx < 0):
            self.vx = 0            
        elif(self.x == 700-self.width and self.vx>0):
            self.vx = 0
        self.x += self.vx
        

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
            
        for bullet in self.model.myBullets:
            self.drawBullet(bullet)
        for bullet in self.model.enemyBullets:
            self.drawBullet(bullet)
        fighter = self.model.fighter
        self.drawFighter(fighter)
        
        pygame.display.update()

    def drawEnemy(self, basicEnemy):
        screen.blit(basicEnemy.image,(basicEnemy.x,basicEnemy.y))
        
    def drawBullet(self, bullet):
        rectangle = pygame.Rect(bullet.x,bullet.y,bullet.width,bullet.height)
        pygame.draw.rect(self.screen, bullet.color, rectangle)
        
    def drawFighter(self, fighter):
        screen.blit(fighter.image,(fighter.x,fighter.y))

class PyGameKeyboardController:
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_a:
                self.model.fighter.vx = -1.0
            if event.key == pygame.K_d:
                self.model.fighter.vx = 1.0
            if event.key == pygame.K_SPACE:
                x = self.model.fighter.x + 17
                y = self.model.fighter.y
                model.newBullet(x,y)
        if event.type == KEYUP:
            if event.key == pygame.K_a:
                if (self.model.fighter.vx == -1):
                    self.model.fighter.vx = 0
            if event.key == pygame.K_d:
                if (self.model.fighter.vx == 1):
                    self.model.fighter.vx = 0            

class CollisionController:
    def __init__(self, model):
        self.model = model

    def checkCollisions(self):
        fighter = self.model.fighter
        if (len(self.model.basicEnemies) == 0):
            print "Game Over! You Won"
            print "Score: "
            print self.model.score
            return False
        for basicEnemy in self.model.basicEnemies:
            for bullet in self.model.myBullets:
                if (self.sameSpace(bullet.x, bullet.y, bullet.width, bullet.height, basicEnemy.x, basicEnemy.y, basicEnemy.width, basicEnemy.height)):              
                    self.model.myBullets.remove(bullet)
                    self.model.basicEnemies.remove(basicEnemy)
                    self.model.score += 10
            if (self.sameSpace(fighter.x, fighter.y, fighter.width, fighter.height, basicEnemy.x, basicEnemy.y, basicEnemy.width, basicEnemy.height)):
                self.model.basicEnemies.remove(basicEnemy)
                self.model.fighter.lives += -1
                if (self.model.fighter.lives == 0):
                    print "Game Over You Died"
                    print "Score:"
                    print self.model.score
                    return False
        for bullet in self.model.enemyBullets:
            if (self.sameSpace(bullet.x, bullet.y, bullet. width, bullet.height, fighter.x, fighter.y, fighter.width, fighter.height)):              
                self.model.enemyBullets.remove(bullet)
                self.model.fighter.lives += -1
                if (self.model.fighter.lives == 0):
                    print "Game Over You Died"
                    print "Score:"
                    print self.model.score
                    return False
        return True
    
    def sameSpace(self, x1, y1, width1, height1, x2, y2, width2, height2):
        return (x2<= x1+width1 and x2+width2>= x1 and y2 <= y1+height2 and y2+height2 >= y1)
        
class EnemyController:
    def __init__(self, model):
        self.model = model

    def moveEnemy(self):
        for enemy in self.model.basicEnemies:
            if (enemy.vy == 0):
                enemy.vy = .5
                return
    def shouldShoot(self):
        for enemy in self.model.basicEnemies:
            if(not enemy.vy == 0 and time.time()>enemy.lastShootTime +2):
                self.model.shoot(enemy)
        
if __name__ == '__main__':
    pygame.init()

    size = (700,700)
    screen = pygame.display.set_mode(size)

    model = GalagaModel()
    view = PyGameWindowView(model,screen)

    KeyBoardcontroller = PyGameKeyboardController(model)
    collisionController = CollisionController(model)
    enemyController = EnemyController(model)
    running = True
    
    startTime = time.time()
    
    while running:
        if (time.time() > startTime+3):
            enemyController.moveEnemy()
            startTime = time.time()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            KeyBoardcontroller.handle_keyboard_event(event)
        running = collisionController.checkCollisions()
        enemyController.shouldShoot()
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
