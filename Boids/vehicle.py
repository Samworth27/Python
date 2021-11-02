# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 13:02:47 2021

@author: samwo
"""

import pygame as pg



class Vehicle (pg.sprite.Sprite):
    image = pg.Surface((10,10),pg.SRCALPHA)
    pg.draw.polygon(image,pg.Color('white'),[(15,5),(0,2),(0,8)])
    
    def __init__(self, position, velocity, minVelocity, maxVelocity,
                 maxForce,maxTurn, can_wrap):
       super().__init__()
       
       #define max limits
       self.vmin = minVelocity
       self.vmax = maxVelocity
       self.fmax = maxForce
       self.tmax = maxTurn
    
       #set pos     #only 2D
       assert (len(position)==2),"Invalid Position"
       
       self.pos=pg.Vector2(position)
       self.vel = pg.Vector2(velocity)
       self.dv = pg.Vector2(0,0)
       self.dir = 0.0
       
       self.rect = self.image.get_rect(center=self.pos)
       
    def update(self,dt,steering):
        self.dv = steering*dt
        
        ### enfore turn limit ###
        _,oldH = self.vel.as_polar()#take the direction component of vel as a polar vector
        newV = self.vel + self.dv * dt
        speed,newH = newV.as_polar()
        
        ### actual enforcement ###
        dH = 180 - (180 - newH + oldH) %360
        if abs(dH) > self.tmax:
            if dH > self.tmax:
                newH = oldH + self.tmax
            else:
                newH = oldH - self.tmax
            
        self.vel.from_polar((speed,newH))
        
        
        ### Enforce Speed Limits ###
        speed, self.heading = self.vel.as_polar()
        if speed < self.vmin:
            self.vel.scale_to_length(self.vmin)
        if speed > self.vmax:
            self.vel.scale_to_length(self.vmax)
        
        
        ### MOVE ###
        self.pos += self.vel*dt
        
        if self.can_wrap:
            self.wrap()
            
        self.image = pg.transform.rotate(Vehicle.image, -self.heading)
        self.rect = self.image.get_rect(center=self.pos)
        
    ### AVOID EDGES ###
    def avoidEdge(self):
        left = self.edges[0]-self.pos.x
        up = self.edges[1]-self.pos.y
        right = self.pos.x - self.edges[2]
        down = self.pos.y - self.edges[3]
        
        boundsTest = max(left,up,right,down)
        
        if boundsTest > 0:
            centre = (Vehicle.max_x/2,Vehicle.max_y/2)
            steering = pg.Vector2(centre) - self.pos
        else:
            steering = pg.Vector2()
        return steering
        
    def wrap(self):
        if self.pos.x < 0:
            self.pos.x += Vehicle.max_x
        elif self.pos.x > Vehicle.max_x:
            self.pos.x -= Vehicle.max_x

        if self.pos.y < 0:
            self.pos.y += Vehicle.max_y
        elif self.pos.y > Vehicle.max_y:
            self.pos.y -= Vehicle.max_y
    
        
        
        
    @staticmethod
    def set_boundary(edge_distance_pct):
        info = pg.display.Info()
        Vehicle.max_x = info.current_w
        Vehicle.max_y = info.current_h
        margin_w = Vehicle.max_x * edge_distance_pct / 100
        margin_h = Vehicle.max_y * edge_distance_pct / 100
        Vehicle.edges = [margin_w, margin_h, Vehicle.max_x - margin_w,
                         Vehicle.max_y - margin_h]

    def clamp_force(self, force):
        if 0 < force.magnitude() > self.fmax:
            force.scale_to_length(self.fmax)
        
        return force
