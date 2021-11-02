# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 12:54:12 2021

@author: samwo
"""
from random import uniform
from vehicle import Vehicle
import pygame as pg

### DEFINE BOIDS ##################################

class Boid (Vehicle):
    
    debug = False
    vmin = .01
    vmax = .2
    fmax = 1
    tmax = 5
    perception = 60
    crowding = 15
    can_wrap = False
    edge_distance_pct = 10
    
    
    def __init__(self):
        Boid.set_boundary(Boid.edge_distance_pct)
        self.sepAlt = False
        ### Randomize starting position and velocity
        initpos = pg.Vector2( 
                    uniform(0,Boid.max_x),
                    uniform(0,Boid.max_y))
        
        initvel = pg.Vector2(
                    uniform(-1,1)*Boid.vmax,
                    uniform(-1,1)*Boid.vmax)
        
        super().__init__(
                initpos, initvel,
                Boid.vmin, Boid.vmax,
                Boid.fmax, Boid.tmax, 
                Boid.can_wrap)
      
        self.rect = self.image.get_rect(center=self.pos)
        
    def getNear(self,boids):
        neighbours = []
        for boid in boids:
            if boid != self:
                dist = self.pos.distance_to(boid.pos)
                if dist < self.perception:
                    neighbours.append(boid)
        return neighbours
                    
    def alignment(self,boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.vel
        steering/=len(boids)
        steering -= self.vel
        steering = self.clamp_force(steering)
        return steering
    
    
    def cohesion(self,boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.pos
        steering /= len(boids)
        steering -= self.pos
        steering = self.clamp_force(steering)
        return steering/100
         
        
    def separation(self,boids):
        steering = pg.Vector2()
        for boid in boids:
            steering.x -= self.crowding/ boid.vel.x
            steering.y -= self.crowding/ boid.vel.y
        steering = self.clamp_force(steering)
        return steering/5
    
    def separationAlt(self, boids):
        steering = pg.Vector2()
        for boid in boids:
            dist = self.pos.distance_to(boid.pos)
            if dist < self.crowding:
                steering -= boid.pos - self.pos
        steering = self.clamp_force(steering)
        return steering

    
    def update(self, dt, boids):
        near = self.getNear(boids)
        steering = pg.Vector2()
        
        
        if near:
            
            if self.sepAlt:
                steering += self.separation(near)
            else:
                steering += self.separationAlt(near)
            
            steering += self.alignment(near)
            steering += self.cohesion(near)
        
        
        
        
        
        if not self.can_wrap:
            steering += self.avoidEdge()
        
        
        
        # steering = self.clamp_force(steering)

        super().update(dt, steering)
    
            
    