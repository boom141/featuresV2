import pygame, sys, random, os, time

pygame.init()
Window = pygame.display.set_mode((400,400))
Display = pygame.Surface((400,400))
Fps = pygame.time.Clock()
last_time = time.time()

GRID_SIZE = 80
slide =  [0,0]

right, left = False, False

tile_map = {}
tile_rect = []


for i in range(400//GRID_SIZE):
	tile_rect.append(pygame.Rect(i* GRID_SIZE, 320, GRID_SIZE, GRID_SIZE))


class Create_Particle(pygame.sprite.Sprite):
	def __init__(self,position,direction,options,physics): # options are [duration,gravity,seconds,width,color], physics are [bounce,tile_map,tile_size]
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.direction = direction
		self.options = options
		self.physics = physics
		self.gravity = 0
	def update(self,dt): 
			self.position[0] += self.direction[0]
			loc_str = f'{int(self.position[0] / self.physics[2])}:{int(self.position[1] / self.physics[2])}'
			if self.physics[0] > 0:
				if loc_str in self.physics[1]:
					self.direction[0] = -self.physics[0] * self.direction[0]
					self.direction[1] *= 0.95
					self.position[0] += self.direction[0] * 2
			self.position[1] += self.direction[1]
			loc_str = f'{int(self.position[0] / self.physics[2])}:{int(self.position[1] / self.physics[2])}'
			if self.physics[0] > 0:
				if loc_str in self.physics[1]:
					self.direction[1] = -self.physics[0] * self.direction[1]
					self.direction[0] *= 0.95
					self.position[1] += self.direction[1] * 2
			self.options[0] -= self.options[2]
			self.direction[1] += self.gravity
			self.gravity += self.options[1]
			if self.options[0] <= 0:
				self.kill()
	
	def draw(self,surface):
		pygame.draw.circle(surface, self.options[4], [self.position[0], self.position[1]], self.options[0], self.options[3])


class Projectile(pygame.sprite.Sprite):
	def __init__(self,position,direction,options): #option are [radius,trajectory,width,color]
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.direction = direction
		self.options = options
		self.trajectory = 0
		self.rect = pygame.Surface((30,30))
		self.rect.fill((0,225,0))
		self.rect.set_colorkey((0,225,0))
		self.hit_box = None

	def collision(self,hit_box):
		for tile in tile_rect:
			if tile.colliderect(hit_box):
				for i in range(50):
					scatter = Create_Particle([hit_box.centerx, hit_box.centery],[random.randrange(-5,5),random.randrange(-5,5)],
					[random.randint(4,6),0,0.1,0,self.options[3][random.randint(0,2)]],[0,tile_map,GRID_SIZE])
					effects.add(scatter)
				self.kill()

	def update(self,dt):
		self.position[0] += self.direction[0] * dt
		self.position[1] += self.direction[1] * dt

		self.direction[1] += self.trajectory 
		self.trajectory += self.options[1]

		for i in range(10):
			effect = Create_Particle([int(self.position[0]),int(self.position[1])],[random.randrange(-2,2),random.randrange(-2,2)],
			[self.options[0],0.1,0.5,0,self.options[3][random.randint(0,2)]],[0,tile_map,GRID_SIZE])
			effects.add(effect)

	def draw(self,surface):
# hit_box-----------------------------------------------------------------#
		self.hit_box = surface.blit(self.rect,(int(self.position[0]) - int(self.rect.get_width()/2), int(self.position[1])- int(self.rect.get_height()/2)))
		self.collision(self.hit_box)
		pygame.draw.circle(surface, self.options[3][random.randint(0,2)], (int(self.position[0]), int(self.position[1])), self.options[0], self.options[2])
   
projectiles = pygame.sprite.Group()
effects = pygame.sprite.Group()

color = [(147,48,59),(31,14,28),(210,100,113)]
while 1:
#framerate independence -------------------------------------------------#
	dt = time.time() - last_time
	dt *= 60
	last_time = time.time()
	Display.fill((25,25,25))
	Fps.tick(60)
	mouse_x, mouse_y = pygame.mouse.get_pos()
	facing = int(mouse_x / GRID_SIZE)

# Spawn per click -------------------------------------------------#

	if pygame.mouse.get_pressed()[0]:
		if facing > 2: 
			direction = [-9,-4]
		else:
			direction = [9,-4]
		projectile = Projectile([mouse_x, mouse_y],direction,[8,0.1,0,color])
		if len(projectiles) == 0:
			projectiles.add(projectile)

	for effect in effects:
		effect.update(dt)
		effect.draw(Display)
	for projectile in projectiles:
		projectile.update(dt)
		projectile.draw(Display)
	
	move = [0,0]
	if right:
		move[0] += 3
	if left:
		move[0] -= 3

	slide[0] += move[0]

	for tile in tile_rect:
		pygame.draw.rect(Display, 'grey', (tile.x - int(slide[0]), tile.y, tile.width, tile.height))
		tile_map[f'{int(tile.x//GRID_SIZE)}:{int(tile.y//GRID_SIZE)}'] = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				right = True
			if event.key == pygame.K_a:
				left = True

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_d:
				right = False
			if event.key == pygame.K_a:
				left = False

	Window.blit(Display,(0,0))
	pygame.display.update()

