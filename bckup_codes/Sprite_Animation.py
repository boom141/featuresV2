import pygame,os

class VFX:
    def __init__(self):
      self.Sprites = []
      self.frame1 = 0
      self.frame2 = 0
      self.frame3 = 0
    
    def Load_Sprite(self, folder_n,file_n,length):
        for i in range(length):
            self.Sprites.append(pygame.image.load(os.path.join(folder_n, f'{file_n}{i}.png')))
        return self.Sprites
    
    def Animate1(self,speed,dt,length):
        self.frame1 += speed
        if self.frame1 >= length:
            self.frame1 = 0
        return self.frame1
    
    def Animate2(self,speed,dt,length):
        self.frame2 += speed
        if self.frame2 >= length:
            self.frame2 = 0
        return self.frame2

    def Animate3(self,speed,dt,length):
        self.frame3 += speed *dt
        if self.frame3 >= length:
            self.frame3 = 0
        return self.frame3

class Player_Animation:
    def __init__(self):
        self.Sprites = []
        self.current_sprites = []
        self.frame = 0
    def Load_Sprites(self,folder_n,file_n,length):
        for i in range(length):
            self.Sprites.append(pygame.image.load(os.path.join(folder_n, f'{file_n}{i}.png')))
        return self.Sprites
    
    def Import_Sprite(self,jump_l,jump_r,left,right,idle_l,idle_r,facing,action):
        if action[0] == action[1] == action[2]:
            if facing == 'left':
                self.current_sprites = idle_l
            else:
                self.current_sprites = idle_r
        elif action[1] and action[0] == False:
            self.current_sprites = left
        elif action[2] and action[0] == False:
            self.current_sprites = right
        elif action[0] and action[1]:
            self.current_sprites = jump_l
        elif action[0] and action[2]:
            self.current_sprites = jump_r

        return self.current_sprites

    def Animate(self,speed,length,dt):
        self.frame += speed * dt
        if self.frame >= length:
            self.frame = 0
        return self.frame