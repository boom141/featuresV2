import pygame, os
from setup import* 

class Map:
	def __init__(self):
		self.tiles = []
		self.tile_map = {}
		self.tile_size = 16
	
	def initialize(self,surface):
		self.tiles = []
		self.tile_map = {}
		for i in range(600//16):
			image = pygame.image.load(os.path.join('asset', 'tile1.png'))
			image.set_colorkey((0,0,0))
			rect = surface.blit(image,(i*self.tile_size - int(scroll[0]),180 - int(scroll[1])))
			self.tiles.append(pygame.Rect(i*self.tile_size,180,self.tile_size,self.tile_size))
			self.tile_map[f'{int(rect.x / self.tile_size)}:{int(rect.y / self.tile_size)}'] = 0


map = Map()