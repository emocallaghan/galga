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
    """ Encodes the game state of Galaga and keeps track of all attributes
        contains a fighter, a list of bullets fired by my fighter, a list of enemies
        and a list of bullets fired by the enemy"
    """
    def __init__(self):
        """ contructor for the GalagaModel class"""
        self.fighter = Fighter(350-17,660)
        self.myBullets = []
        self.enemyBullets = []
        self.basicEnemies = []
        self.score = 0
        for x in range(0, 10):
            basicEnemy = BasicEnemy(x+50*x+100, 350)
            self.basicEnemies.append(basicEnemy)

    def newBullet(self, x,y):
        """this function creates a new bullet fired from fighter at the passed in locations, x and y"""
        color = (255,0,0)
        self.myBullets.append(Bullet(color,15,5,x,y,-.75))

    def update(self):
        """updates fighter, all bullets, and all enemies"""
        for bullet in self.myBullets:
            bullet.update()
        for bullet in self.enemyBullets:
            bullet.update()
            
        for basicEnemy in self.basicEnemies:
            basicEnemy.update()
            if (basicEnemy.y > 700):
                basicEnemy.y = 0
        self.fighter.update()
        
    def shoot(self, enemy, bulletSpeed):
        """creates a new bullet fired by an enemy from the middle of the enemy"""
        color = (255, 255, 255)
        bullet = Bullet(color, 15,5,enemy.x+enemy.width/2,enemy.y+enemy.height,bulletSpeed)
        self.enemyBullets.append(bullet)
        enemy.lastShootTime = time.time()

class BasicEnemy:
    """basic enemy class contains a constructor and an update method"""
    def __init__(self, x, y):
        """contructor for basic enemy sets location based on passed in variables, and loads the picture
        of an enemy from given file. also sets last shootTime"""
        self.x = x
        self.y = y
        self.height = 35
        self.width = 31
        self.vx = 0
        self.vy = 0
        self.image = pygame.image.load("galgaBasicEnemyShip.jpg")
        self.lastShootTime = time.time()

    def update(self):
        """moves position based on current velocity"""
        self.x += self.vx
        self.y += self.vy

class Fighter:
    """fighter class contains a contruction and update method"""
    def __init__(self, x, y):
        """constructor for fighter sets location based on given values, number of lives, pixle height
        and width inital speed as zero and loads the image of a fighter"""
        self.lives = 1
        self.x = x
        self.y = y
        self.vx = 0.0
        self.height = 40
        self.width = 34
        self.image = pygame.image.load("galaga_ship.jpg")

    def update(self):
        """moves position based on velocity unless at either side of screen and attempting to move
        off screen where it is stopped"""
        if (self.x == 0 and self.vx < 0):
            self.vx = 0            
        elif(self.x == 700-self.width and self.vx>0):
            self.vx = 0
        self.x += self.vx
        

class Bullet:
    """bullet class contains a constructor and update"""
    def __init__(self,color,height,width,x,y,vy):
        """sets color, height, width, position, and velocity based on passed in parameters"""
        self.color = color
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.vy = vy
        
    def update(self):
        """moves position based on velocity"""
        self.y += self.vy

class PyGameWindowView:
    """ A view of Galaga rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        """draws all of the elements on the screen uses a series of subfunctions
        to draw fighters, bullets, and enemy"""
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
        """draws an emeny from what is passed in"""
        screen.blit(basicEnemy.image,(basicEnemy.x,basicEnemy.y))
        
    def drawBullet(self, bullet):
        """draws a rectangle for a bullet based on passed in bullet and its parameters"""
        rectangle = pygame.Rect(bullet.x,bullet.y,bullet.width,bullet.height)
        pygame.draw.rect(self.screen, bullet.color, rectangle)
        
    def drawFighter(self, fighter):
        """draws a fighter from what is passed in"""
        screen.blit(fighter.image,(fighter.x,fighter.y))

class PyGameKeyboardController:
    """ Handles keyboard input for galaga"""
    def __init__(self,model):
        """contructor just sets the model to model"""
        self.model = model
    
    def handle_keyboard_event(self,event):
        """sets how the fighter moves and if the user shoots a bullet"""
        if event.type == KEYDOWN:
            """if the a key is pushed and held down the fighter moves to the left if the d
            key is pushed and held down the fighter moves to the right if the space bar is hit
            a bullet is created"""
            if event.key == pygame.K_a:
                self.model.fighter.vx = -1.0
            if event.key == pygame.K_d:
                self.model.fighter.vx = 1.0
            if event.key == pygame.K_SPACE:
                x = self.model.fighter.x + 17
                y = self.model.fighter.y
                model.newBullet(x,y)
        if event.type == KEYUP:
            """if the a key is lifted up and the player is traveling to the left the player will stop.
            if the d key is lifted and the player is traveling to the right the player will stop."""
            if event.key == pygame.K_a:
                if (self.model.fighter.vx == -1):
                    self.model.fighter.vx = 0
            if event.key == pygame.K_d:
                if (self.model.fighter.vx == 1):
                    self.model.fighter.vx = 0            

class CollisionController:
    """tests if any two objects colloide"""
    def __init__(self, model, collisionController):
        self.model = model
        self.collisionController = collisionController

    def checkCollisions(self):
        fighter = self.model.fighter
        if (len(self.model.basicEnemies) == 0):
            if (self.collisionController.changeTime > 1):
                self.collisionController.changeTime -= 1
                self.collisionController.shootTime -= 1
            elif(self.collisionController.changeTime>.5):
                self.collisionController.changeTime -= .5
                self.collisionController.shootTime -= .5
            else:
                print "You Won!"
                print "Score:"
                print self.model.score
                return False
            for x in range(0, 10):
                basicEnemy = BasicEnemy(x+50*x+100, 350)
                self.model.basicEnemies.append(basicEnemy)
            self.collisionController.vy += .3
            self.collisionController.bulletSpeed += .3
            
            

            return True
        for basicEnemy in self.model.basicEnemies:
            for bullet in self.model.myBullets:
                """checks if any bullets and enemies occupy the same space and removes them from the
                model if they do occupy the same space"""
                if (self.sameSpace(bullet.x, bullet.y, bullet.width, bullet.height, basicEnemy.x, basicEnemy.y, basicEnemy.width, basicEnemy.height)):              
                    self.model.myBullets.remove(bullet)
                    self.model.basicEnemies.remove(basicEnemy)
                    self.model.score += 10
            if (self.sameSpace(fighter.x, fighter.y, fighter.width, fighter.height, basicEnemy.x, basicEnemy.y, basicEnemy.width, basicEnemy.height)):
                """checks if the fighter is in the same place as any of the basic enemies and removes the enemy and takes away a life from the 
                    fighter if this is the case. if the fighter has no more lifes closes window and prints that the player 
                    lost and prints the score"""
                self.model.basicEnemies.remove(basicEnemy)
                self.model.fighter.lives += -1
                if (self.model.fighter.lives == 0):
                    print "Game Over You Died"
                    print "Score:"
                    print self.model.score
                    return False
        for bullet in self.model.enemyBullets:
            """checks if the fighter is in the same place as any of the enemy bullets and removes the enemy bullet and takes away a life from the 
                    fighter if this is the case. if the fighter has no more lifes closes window and prints that the player 
                    lost and prints the score"""
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
        """function checks if thetwo objects occupy the same space."""
        return (x2<= x1+width1 and x2+width2>= x1 and y2 <= y1+height2 and y2+height2 >= y1)
        
class EnemyController:
    """controls all the enemies on the screen.  Has a constructor, move enemy function, 
    and should shoot function"""
    def __init__(self, model):
        self.model = model
        self.vy = .5
        self.changeTime = 3
        self.shootTime = 3
        self.bulletSpeed = .75

    def moveEnemy(self):
        """checks if the an enemy is moving.  If not, starts it to move.
        If so it proceeds to the next one.  Returns once moves an enemy."""
        for enemy in self.model.basicEnemies:
            if (enemy.vy == 0):
                enemy.vy = self.vy
                return
    def shouldShoot(self):
        """shoots if the enemy is moving and if it shot more than two seconds ago shoots again."""
        for enemy in self.model.basicEnemies:
            if(not enemy.vy == 0 and time.time()>enemy.lastShootTime + self.shootTime):
                self.model.shoot(enemy, self.bulletSpeed)
        
if __name__ == '__main__':
    pygame.init()

    size = (700,700)
    screen = pygame.display.set_mode(size)

    model = GalagaModel()
    view = PyGameWindowView(model,screen)

    KeyBoardcontroller = PyGameKeyboardController(model)
    enemyController = EnemyController(model)
    collisionController = CollisionController(model, enemyController)    
    running = True
    
    startTime = time.time()
    
    while running:
        if (time.time() > startTime + enemyController.changeTime): #if an enemy moved more than three seconds ago, moves next enemy
            enemyController.moveEnemy()
            startTime = time.time()
        running = collisionController.checkCollisions()
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            KeyBoardcontroller.handle_keyboard_event(event)
        enemyController.shouldShoot()
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
