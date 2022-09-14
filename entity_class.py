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
		self.player_image = pygame.image.load(os.path.join('asset/player-idle', 'player_idle_right0.png')).convert()    
		self.player_image.set_colorkey((0,0,0))
		self.image_copy = self.player_image.copy()
		self.rect = self.image_copy.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.player_animation = 0
		self.jumping_animation = 0
		self.free_fall = 0
		self.double_jump = 0
		self.animation = 0
		self.landing = False
		self.facing = 'right'
		self.state = 'player-'
		self.vertical_momentum = 0
		self.hit_box = None
		self.hit_countdown = 0
		self.hit = False
		self.collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
		
	def collision_test(self):
		hit_list = []
		for tile in map.tiles:
			if tile.colliderect(self.rect):
				hit_list.append(tile)
		return hit_list

	def move(self,meter,dt):
#player controller -----------------------------------------------------#    
		player_movement = ['idle',0,0]
		if keys['left']:
			player_movement[1] -= 3
		if keys['right']:
			player_movement[1] += 3
		if keys['jump']:
			if self.collision_types['bottom']:
				self.jumping_animation = 0
				self.free_fall = 0
				self.vertical_momentum = -5
				self.landing = True

			elif self.free_fall > 30 and self.double_jump == 0:
				self.vertical_momentum -= 8
				self.double_jump = 1
				self.jumping_animation = 0
	
		player_movement[2] += self.vertical_momentum
		self.vertical_momentum += 0.2
		if self.vertical_momentum > 3:
			self.vertical_momentum = 3
		if self.collision_types['bottom'] == False:
			player_movement[0] = 'jump'
			self.free_fall += 1
		if (player_movement[1] > 0 or player_movement[1] < 0) and self.collision_types['bottom']:
			player_movement[0] = 'walk'
# player hit -------------------------------------------------------------#
		if self.hit_countdown <= 0:
			self.hit = False
			self.hit_countdown = 0
			self.state = 'player-'
			
		if self.hit:
			self.hit_countdown -= 1
			self.state = 'hit-'		
		
		if meter.decrease_value == 3:
			self.hit = True
			self.hit_countdown = 50

# player_collision -------------------------------------------------------#
		self.collision_types = {'top':False,'bottom':False,'right':False,'left':False} 
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
				self.collision_types['bottom'] = True
			elif player_movement[2] < 0:
				self.rect.top = tile.bottom

		self.hit_box = self.rect.copy()
		self.hit_box.x = self.rect.x - int(scroll[0]) + 10
		self.hit_box.y = self.rect.y - int(scroll[1]) + 15
		self.hit_box.width = 40
		self.hit_box.height = 20

		self.update(player_movement,dt)
	
	def update(self,status,dt):
		if status[1] > 0:
			self.facing = 'right'
		if status[1] < 0:
			self.facing = 'left'
		if self.player_animation >= player_sprites[status[0]]['frames']:
			self.player_animation = 0
		if self.jumping_animation >= player_sprites[status[0]]['frames']:
			self.jumping_animation = player_sprites[status[0]]['frames']
		if status[0] == 'jump'and self.free_fall > 0:
			self.jumping_animation += 0.185 * dt
			self.animation = self.jumping_animation
		else:
			self.player_animation += 0.185 * dt
			self.animation = self.player_animation
		if self.player_animation <= player_sprites[status[0]]['frames']:
			self.player_image = pygame.image.load(os.path.join(f'asset/{self.state}{status[0]}', 
			f'{player_sprites[status[0]][self.facing]}{int(self.animation)}.png'))
			self.player_image.set_colorkey((0,0,0))

# landing animation ----------------------------------------------------------------#
		if self.collision_types['bottom'] and self.landing:
			self.double_jump = 0
			landing = Landing([self.rect.x - int(scroll[0]), self.rect.y - int(scroll[1])],[20,-15],[self.landing,5])
			effects.add(landing)
			self.landing = False

	def draw(self,surface):
		#pygame.draw.rect(surface, 'green', self.hit_box, 1)
		surface.blit(self.player_image,(self.rect.x - int(scroll[0]),self.rect.y + 3 - int(scroll[1])))


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

	def player_hit(self,player):
#enemy attacking towards the position of the player ------------------------------------------------#
		if self.hit_box.colliderect(player):
			if (player.right > self.hit_box.left
				 and player.left < self.hit_box.left ):
					self.facing = 'left'
			if (player.right > self.hit_box.right
				 and player.left < self.hit_box.right):
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
	
	def move(self,player,dt):
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
		self.hit_box.x = self.rect.x - 75
		self.hit_box.y = self.rect.y
		self.hit_box.width = 200
		
		self.update(dt)
		self.player_hit(player)
		
	def update(self,dt):
		if self.animation >= enemy_sprites[self.status]['frames']:
			self.animation = 0
		self.animation += 0.175 * dt
		if self.animation <= enemy_sprites[self.status]['frames']:
			self.image = pygame.image.load(os.path.join(f'asset/enemy-{self.status}', 
			f'{enemy_sprites[self.status][self.facing]}{int(self.animation)}.png'))
			self.image.set_colorkey((0,0,0)) 

	def draw(self,surface):
		#pygame.draw.rect(surface, "green", (self.hit_box.x - int(scroll[0]),self.hit_box.y + 3 - int(scroll[1]), self.hit_box.width, self.hit_box.height),1) # hit-box highlight
		surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y + 3 - int(scroll[1])))

class Meter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.water_meter = pygame.image.load(os.path.join('asset/misc', 'water_meter.png'))
		self.image1 = pygame.transform.scale(self.water_meter,(105,15))
		self.image1.set_colorkey((0,0,0))
		self.rect = pygame.Rect(5,6,self.image1.get_width(),self.image1.get_height()-2)
		self.color = ((56,136,156))
		self.delay = 10
		self.seconds = 0
		self.reset = 30
		self.decrease_value = 0.1

	def update(self,dt):
		if self.decrease_value > 0.1:
			self.reset -= 1

		if self.seconds >= self.delay:
			self.rect.width -= self.decrease_value * dt
			self.seconds = 0

		if self.reset <= 0:
			self.reset = 30
			self.decrease_value = 0.1	

		self.seconds += 0.5 * dt
		print(self.rect.width)
		
	def draw(self,surface):
		pygame.draw.rect(surface, self.color, self.rect)
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

	def player_collision(self,player,meter):
		if self.rect.colliderect(player):
			meter.rect.width += 3
			pulse1 = Pulse_Ease_Out([player.centerx - int(scroll[0]),player.centery - int(scroll[1])],[5,3,100],((225,225,225)),True)
			pulse2 = Pulse_Ease_Out([player.centerx - int(scroll[0]),player.centery - int(scroll[1])],[3,2,100],((4,174,184)),True)
			effects.add(pulse1,pulse2)  
			for i in range(50):
				disperse = Static_Particle([self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])],[random.randrange(-5,5),
				random.randrange(-5,5)],[random.randint(4,6),0,0.1,0,self.color[random.randint(0,2)]],[0,map.tile_map,map.tile_size,10])
				particles.add(disperse)      
			self.kill()
	
	def update(self,player,meter,dt):
		if self.animation >= 7:
			self.animation = 0
		self.animation += 0.2 * dt
		if self.animation <= 7:
			self.image = pygame.image.load(os.path.join('asset/droplet', f'water_droplet{int(self.animation)}.png')).convert_alpha()
			self.image.set_colorkey((0,0,0))
   
		self.player_collision(player,meter)
	
	def draw(self,surface):
		surface.blit(self.image,(self.rect.x - int(scroll[0]),self.rect.y - int(scroll[1])))

class Projectile(pygame.sprite.Sprite):
	def __init__(self,position,direction,options): #option are [radius,trajectory,width,color]
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.direction = direction
		self.options = options
		self.trajectory = 0
		self.rect = None
		self.map = None

	def collision(self,player,meter):
		loc_str = f'{int(self.position[0] / map.tile_size)}:{int(self.position[1] / map.tile_size)}'
		if loc_str in map.tile_map or self.rect.colliderect(player):
			pulse1 = Pulse_Ease_Out([self.position[0], self.position[1]],[5,3,40],((255,255,255)),True)
			pulse2 = Pulse_Ease_Out([self.position[0], self.position[1]],[3,1,40],self.options[3][1],True)
			effects.add(pulse1,pulse2)
			
			for i in range(30):
				scatter = Static_Particle([self.rect.x, self.rect.y],[random.randint(-5,8),random.randint(-5,2)],
				[random.randint(4,6),0,0.1,0,self.options[3][random.randint(0,2)]],[0,map.tile_map,map.tile_size,0])
				effects.add(scatter)

			meter.decrease_value = 3
			self.kill()
			
	def update(self,player,meter,dt):
		self.position[0] += self.direction[0] * dt
		self.position[1] += self.direction[1] * dt

		self.direction[1] += self.trajectory 
		self.trajectory += self.options[1]

		self.rect = pygame.Rect(int(self.position[0]) - 10,int(self.position[1]) - 10, 20,20)
		for i in range(10):
			effect = Static_Particle([int(self.position[0]),int(self.position[1])],[2,0],
			[self.options[0],0.1,0.5,0,self.options[3][random.randint(0,2)]],[0,map.tile_map,map.tile_size,0])
			effects.add(effect)

		self.collision(player,meter)

	def draw(self,surface):
# hit_box-----------------------------------------------------------------#
		pygame.draw.rect(surface, 'green', self.rect, 1)
		pygame.draw.circle(surface, self.options[3][random.randint(0,2)], (int(self.position[0]), int(self.position[1])), self.options[0], self.options[2])