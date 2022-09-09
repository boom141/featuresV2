import pygame, os

class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tiles = []
        self.tile_map = {}
        self.tile_size = 16
    
    def setup(self):
        for i in range(600//16):
            image = pygame.image.load(os.path.join('asset', 'tile1.png'))
            image.set_colorkey((0,0,0))
            rect = image.get_rect()
            rect.x = i*self.tile_size
            rect.y = 180
            self.tiles.append([image,rect])
   
    def draw(self,surface,scroll):
        for tile in self.tiles:
            rect = surface.blit(tile[0],(tile[1].x - int(scroll[0]),tile[1].y-int(scroll[1])))
            self.tile_map[f'{int(rect.x // self.tile_size)}:{int(rect.y // self.tile_size)}'] = rect