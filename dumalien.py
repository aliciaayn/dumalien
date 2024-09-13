import myObj
import action
import pygame
import math
class Dumalien(myObj.MyObject): 
    def __init__(self,pos,fps=20): 
        spriteSheet=pygame.image.load("dumalien.png")
        size=(32,32)

        myObj.MyObject.__init__(self,spriteSheet,size,pos,4,fps)
        self.playing=1

        self.actions={"BLOBBING":action.Action("BLOBBING", 0, 4, False), "EXPLODING":action.Action("EXPLODING", 4, 4, True)}
        self.vy=0
        self.currentAction=self.actions["BLOBBING"]

    def update(self,dt,t):
        if self.playing and t>self._next_update: 
            if self.currentAction==self.actions["EXPLODING"] and self.current==self.currentAction.startingIndex+self.currentAction.numberFrames-1:
                self.currentAction.done=True
            if self.currentAction.done==False:
                self.current=(((self.current+1)%self.currentAction.numberFrames)+self.currentAction.startingIndex)
                self.source_rect.x=(self.current%self._cols)*self._frame_w
                self.source_rect.y=math.floor(self.current/self._rows)*self._frame_h
                self._next_update=t+self._period

