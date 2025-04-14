'''
Ball class with all data about ball
Author: Noah Sokol
date: 2/14/24
'''

class Ball:
    def __init__(self, color, startY, velo, a, m):
        #set color
        self.color = color
        
        #only one x pos
        self.x = [0]

        #declare starting y position
        self.y = [startY]

        #declare motion of ball
        self.velo = velo
        self.a = a

        self.m = m
    
    def setVelo(self, velo = 0):
        self.velo = velo

    def setColor(self, color):
        #set new color
        self.color = color

    def getPos(self):
        return self.y[-1]

    def step(self, dt):
        self.y.append(dt * self.velo + self.y[-1])

    def move(self, dt, k, i):
        self.step(dt)
        #print("time:" , i * dt, "accel:", self.a.__round__(2), self)
        self.a = -k * self.y[-1] / self.m
        self.velo = self.velo + dt * self.a

    
    def __str__(self):
        return f"pos: {self.y[-1].__round__(2)} velo: {self.velo.__round__(3)} color: {self.color}"
