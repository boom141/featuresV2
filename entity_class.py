import pygame, os, random
from setup import*
from game_sprites_data import*
from effects_and_particles import*
from sprite_groups import*
from key_mapping_data import*
from map_loader import*

class Player(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.player_image = pygame.image.load(os.path.join('asset/idle', 'player_idle_right0.png')).convert()    
		self.player_image.set_colorkey((0,0,0))
		self.image_copy = self.player_image.copy()
		self.rect = self.image_copy.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.landing_image = pygame.image.load(os.path.join('asset/effects/landing', '0.png')).convert()
		self.landing_image_copy = self.landing_image.copy()
		self.landing_image_rect = self.landing_image_copy.get_rect()
		self.player_animation = 0
		self.effects_animation = -1
		self.effects_type = 'landing'
		self.animate = False
		self.facing = 'right'
		self.vertical_momentum = 0
		self.jump_cooldown = 0
		
	def collision_test(self):
		hit_list = []
		for tile in map.tiles:
			if tile.colliderect(self.rect):
				hit_list.append(tile)
		return hit_list

	def move(self,dt):
		collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
#player controller -----------------------------------------------------#    
		player_movement = ['idle',0,0]
		if keys['left']:
			player_movement[1] -= 3
			player_movement[0] = 'walk'
		if keys['right']:
			player_movement[1] += 3
			player_movement[0] = 'walk'
		if keys['jump']:
			if self.jump_cooldown == 0:
				self.jump_cooldown = 65 #60 for single jump 30 for multiple/double jumps
				self.vertical_momentum = -5
		player_movement[2] += self.vertical_momentum
		self.vertical_momentum += 0.2
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3
		if self.jump_cooldown > 0:
			self.jump_cooldown -= 1
			player_movement[0] = 'jump'

# player_collision -------------------------------------------------------#
		self.rect.x += player_movement[1] * dt
		hit_list = self.collision_test()
		for tile in hit_list:
			if player_movement[1] > 0:
				self.rect.right = tile.left
			elif player_movement[1] < 0:
				self.rect.left = tile.right
		self.rect.y += player_movement[2] * dt
		hit_list = self.collision_test()
		for tile in hit_list:
			if player_movement[2] > 0:
				self.rect.bottom = tile.top
				collision_types['bottom'] = True
			elif player_movement[2] < 0:
				self.rect.top = tile.bottom
		
		self.update(player_movement,collision_types,dt)
	
	def update(self,status,collision_types,dt):
		if status[1] > 0:
			self.facing = 'right'
		if status[1] < 0:
			self.facing = 'left'
		if self.player_animation >= player_sprites[status[0]]['frames']:
			self.player_animation = 0
		self.player_animation += 0.185 * dt
		if self.player_animation <= player_sprites[status[0]]['frames']:
			self.player_image = pygame.image.load(os.path.join(f'asset/{status[0]}', 
			f'{player_sprites[status[0]][self.facing]}{int(self.player_animation)}.png'))
			self.player_image.set_colorkey((0,0,0))

# landing animation ----------------------------------------------------------------#
		if collision_types['bottom'] == False:
			self.effects_animation = 0
	   
		if collision_types['bottom']:
			self.effects_animation += 0.395 * dt
			self.animate = True
			self.effects_type = 'landing'

		if self.effects_animation >= 4:
			self.effects_animation = 4
			self.animate = False

		self.landing_image = pygame.image.load(os.path.join(f'asset/effects/{self.effects_type}', f'{int(self.effects_animation)}.png'))
		self.landing_image_copy = pygame.transform.scale(self.landing_image,(105,30))
		self.landing_image_copy.set_colorkey((0,0,0))
	def draw(self,surface):
		surface.blit(self.player_image,(self.rect.x - int(scroll[0]),self.rect.y + 3 - int(scroll[1])))
		if self.animate:
			surface.blit(self.landing_image_copy,((self.rect.x - 20)- int(scroll[0]),(self.rect.bottom - 15) - int(scroll[1])))


class Enemy(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('asset/enemy-idle', 'idle_right0.png')).convert()
		self.image.set_colorkey((0,0,0))
		self.image_copy = self.image.copy()
		self.rect = self.image_copy.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.hit_box = None
		self.animation = 0
		self.walk_countdown = 0
		self.idle_countdown = -1
		self.walk_direction = True
		self.vertical_momentum = 0
		self.status = 'walk'
		self.facing = 'right'
		self.color = [(147,48,59),(31,14,28),(210,100,113)]

	def player_hit(self,player_rect):
#enemy attacking towards the position of the player ------------------------------------------------#
		if self.hit_box.colliderect(player_rect):
			if (player_rect.right > self.hit_box.left
				 and player_rect.left < self.hit_box.left ):
					self.facing = 'left'
			if (player_rect.right > self.hit_box.right
				 and player_rect.left < self.hit_box.right):
					self.facing = 'right'
			self.status = 'attack' 
		else:
			self.status = 'walk'
		
		self.shoot_player()
	
	def shoot_player(self):
		if (self.status == 'attack' and int(self.animation) == enemy_sprites[self.status]['frames']):
			if self.facing == 'right':
				direction = [7,-4]
			else:
				direction = [-7,-4]
			projectile = Projectile([self.rect.centerx - int(scroll[0]),self.rect.centery - int(scroll[1])],direction,[4,0.1,0,self.color])
			projectiles.add(projectile)

	def collision_test(self):
		hit_list = []
		for tile in map.tiles:
			if tile.colliderect(self.rect):
				hit_list.append(tile)
		return hit_list
	
	def move(self,dt):
		direction = [0,0] 
		direction[1] += self.vertical_momentum 
		self.vertical_momentum += 0.2
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3
		
		if self.idle_countdown > 0:
			self.idle_countdown -= 1

		if random.randint(1,200) == 1 and self.idle_countdown == 0 and self.status != 'attack':
			self.status = 'idle'
			self.idle_countdown = 50 

		if self.idle_countdown <= 0 and self.status != 'attack':
			self.status = 'walk'
			self.idle_countdown = 0

			if self.walk_countdown >= 80:
				self.walk_direction = not self.walk_direction
				self.walk_countdown = 0
			self.walk_countdown += 2
			
			if self.walk_direction:
				direction[0] += 2 * dt
				self.facing = 'right'
			else:
				direction[0] -= 2 * dt
				self.facing = 'left'


		self.rect.x += int(direction[0])
		self.rect.y += direction[1]
		hit_list = self.collision_test()
		for tile in hit_list:
			if direction[1] > 0:
				self.rect.bottom = tile.top
			elif direction[1] < 0:
				self.rect.top = tile.bottom
		
		self.hit_box = self.rect.copy()
		self.hit_box.width = 250
		self.hit_box.left = 200
		self.update(dt)

	def update(self,dt):
		if self.animation >= enemy_sprites[self.status]['frames']:
			self.animation = 0
		self.animation += 0.175 * dt
		if self.animation <= enemy_sprites[self.status]['frames']:
			self.image = pygame.image.load(os.path.join(f'asset/enemy-{self.status}', 
			f'{enemy_sprites[self.status][self.facing]}{int(self.animation)}.png'))
			self.image.set_colorkey((0,0,0)) 

	def draw(self,surface,player_rect):
		#pygame.draw.rect(surface, "green", (self.hit_box.x - int(scroll[0]),self.hit_box.y + 3 - int(scroll[1]), self.hit_box.width, self.hit_box.height),1) # hit-box highlight
		self.player_hit(player_rect)
		surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y + 3 - int(scroll[1])))

class Meter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.water_meter = pygame.image.load(os.path.join('asset/misc', 'water_meter.png'))
		self.image1 = pygame.transform.scale(self.water_meter,(105,13))
		self.image1.set_colorkey((0,0,0))

	def update(self):
		pass

	def draw(self,surface):
		surface.blit(self.image1,(5,5))

class Trees(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('asset/tree', 'tree0.png'))
		self.image_copy = self.image.copy()
		self.rect = self.image_copy.get_rect()
		self.rect.x = x
		self.rect.bottom = y
		self.animation = 0
	
	def update(self,dt):
		if self.animation >= 8:
			self.animation =0
		self.animation += 0.2 * dt
		if self.animation <= 8:
			self.image = pygame.image.load(os.path.join('asset/tree', f'tree{int(self.animation)}.png')).convert_alpha()
			self.image.set_colorkey((0,0,0))
			
	def draw(self,surface):
		surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])))

class Droplet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('asset/droplet', 'water_droplet0.png'))
		self.image_copy = self.image.copy()
		self.rect = self.image_copy.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.animation = 0
		self.color = [(255,255,255),(4,174,184),(56,136,156)]

	def update(self,dt):
		if self.animation >= 7:
			self.animation = 0
		self.animation += 0.2 * dt
		if self.animation <= 7:
			self.image = pygame.image.load(os.path.join('asset/droplet', f'water_droplet{int(self.animation)}.png')).convert_alpha()
			self.image.set_colorkey((0,0,0))
   
	def player_collision(self,player_rect):
		if self.rect.colliderect(player_rect):
			pulse1 = Pulse_Ease_Out([player_rect.centerx - int(scroll[0]),player_rect.centery - int(scroll[1])],[5,3,100],((225,225,225)),True)
			pulse2 = Pulse_Ease_Out([player_rect.centerx - int(scroll[0]),player_rect.centery - int(scroll[1])],[3,2,100],((4,174,184)),True)
			effects.add(pulse1,pulse2)  
			for i in range(50):
				disperse = Static_Particle([self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])],[random.randrange(-5,5),
				random.randrange(-5,5)],[random.randint(4,6),0,0.1,0,self.color[random.randint(0,2)]],[0.5,map.tile_map,map.tile_size,10])
				particles.add(disperse)       
			self.kill()     
	
	def draw(self,surface):
		surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])))

class Projectile(pygame.sprite.Sprite):
	def __init__(self,position,direction,options): #option are [radius,trajectory,width,color]
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.direction = direction
		self.options = options
		self.trajectory = 0
		self.hit_box = None
		self.map = None

	def collision(self):
		for tile in map.tiles:
			if (tile.colliderect(self.hit_box)):
				for i in range(30):
					scatter = Static_Particle([self.hit_box.x, self.hit_box.y],[random.randint(-5,8),random.randint(-5,2)],
					[random.randint(4,6),0,0.1,0,self.options[3][random.randint(0,2)]],[0,map.tile_map,map.tile_size,0])
					effects.add(scatter)	
				self.kill()

	def update(self,dt):
		self.position[0] += self.direction[0] * dt
		self.position[1] += self.direction[1] * dt

		self.direction[1] += self.trajectory 
		self.trajectory += self.options[1]

		self.hit_box = pygame.Rect(int(self.position[0]) - 10,int(self.position[1]) - 10, 20,20)
		for i in range(10):
			effect = Static_Particle([int(self.position[0]),int(self.position[1])],[2,0],
			[self.options[0],0.1,0.5,0,self.options[3][random.randint(0,2)]],[0,map.tile_map,map.tile_size,0])
			effects.add(effect)
		self.collision()
	def draw(self,surface):
# hit_box-----------------------------------------------------------------#
		pygame.draw.rect(surface, 'green', self.hit_box, 1)
		pygame.draw.circle(surface, self.options[3][random.randint(0,2)], (int(self.position[0]), int(self.position[1])), self.options[0], self.options[2])