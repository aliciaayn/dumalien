import math
import pygame
class MyObject(pygame.sprite.Sprite): 
    def __init__(self,spriteSheet,size,pos,numSprites,fps=20): 
        pygame.sprite.Sprite.__init__(self)
        self.current=0
        self.source_rect=pygame.Rect((0,0),size)
        self._frame_w=size[0]
        self._frame_h=size[1]
        self.image=spriteSheet
        self.x=pos[0]
        self.y=pos[1]
        self.rect=pygame.Rect(pos,size)
        self._cols=self.image.get_width()/self._frame_w
        self._rows=self.image.get_height()/self._frame_h

        self.playing=0
        self._num_sprites=numSprites
        self._next_update=0
        self._inv_period=fps/1000
        self._period=1000/fps
        self._start_time=0
        self._paused_time=0
        self._pause_start=0


    def update(self,dt,t): 
        if self.playing and t>self._next_update:
            self.current+=1
            self.current=self.current%self._num_sprites
            self.source_rect.x=(self.current%self._cols)*self._frame_w
            self.source_rect.y=math.floor(self.current/self._rows)*self._frame_h
            self._next_update=t+self._period
        

            
        

