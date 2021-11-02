# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 11:00:41 2021

@author: samwo
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
### Imports ###
import argparse
import sys
import pygame as pg
from pygame.locals import *
import random
import numpy as np
from boid import Boid


### VARIABLE DEFINITIONS ###
default_boids = 200
default_geometry = "1800x1000"


### Definitions ##################################
##################################################
def add_boids(boids, num_boids):
    for _ in range(num_boids):
        boids.add(Boid()) 

       
### DISPLAY ######################################        
class App(object):
    """ 
    w: screen width
    h: screen height
    n: number of boids"""
    def __init__(self, args):
        self._running = True
        self.fps = 60.0
        self.fpsClock = pg.time.Clock()

     
    
    def onInit(self):
        pg.init()
        pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])
        window_width, window_height = [int(x) for x in args.geometry.split("x")]
        flags = DOUBLEBUF
        
        self.screen = pg.display.set_mode((window_width, window_height), flags)
        self.screen.set_alpha(None)
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(pg.Color('black'))
        self.boids = pg.sprite.RenderUpdates()

        add_boids(self.boids,args.num_boids)
            
        self.dt = 1/self.fps

   

            
    def onEvent(self, event):
        if event.type == pg.QUIT:
            self._running = False
            
        elif event.type == KEYDOWN:
            mods = pg.key.get_mods()
            if event.key == pg.K_s:
                for boid in self.boids:
                    boid.sepAlt = not boid.sepAlt
                    
            
    def onLoop(self,dt, boids):
        for b in boids:
            b.update(dt,boids)
    
    def onRender(self):
        self.boids.clear(self.screen, self.background)
        dirty = self.boids.draw(self.screen)
        pg.display.update(dirty)




        
    def onCleanup(self):
        pg.quit()
        sys.exit(0)
        
    ### Main Loop ###
    def onExecute(self): 
        ### INIT ###
        if self.onInit() == False:
            self._running = False    
        while(self._running):
            for event in pg.event.get():
                self.onEvent(event)
            self.onLoop(self.dt,self.boids)
            self.onRender()
            self.dt = self.fpsClock.tick(self.fps)
        ### End App
        self.onCleanup()
###################################################        

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='Emergent flocking.')
    parser.add_argument('--geometry', metavar='WxH', type=str,
                        default=default_geometry, help='geometry of window')
    parser.add_argument('--number', dest='num_boids', default=default_boids,
                        help='number of boids to generate')
    args = parser.parse_args()
    
    a = App(args)
    a.onExecute()