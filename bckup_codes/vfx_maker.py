import pygame, sys, random, os, time

pygame.init()
Window = pygame.display.set_mode((400,400))
Display = pygame.Surface((400,400))
Fps = pygame.time.Clock()
last_time = time.time()

GRID_SIZE = 80
slide =  [0,0]

right, left = False, False


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

class Map:
	def __init__(self):
		self.tiles = []
		self.tile_map = {}
		self.tile_size = 20
	
	def Initialize(self):
		self.tiles = []
		self.tile_map = {}
		for i in range(400//GRID_SIZE):
			tile = pygame.draw.rect(Display, 'grey', (i* GRID_SIZE - slide[0], 320, GRID_SIZE, GRID_SIZE))
			self.tiles.append(tile)
			self.tile_map[f'{int(tile.x/GRID_SIZE)}:{int(tile.y/GRID_SIZE)}'] = 0

 
map = Map()
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
	
	move = [0,0]
	if right:
		move[0] += 3
	if left:
		move[0] -= 3

	slide[0] += move[0]

	map.Initialize()
# Spawn per click -------------------------------------------------#
	if pygame.mouse.get_pressed()[0]:
		for i in range(30):
			scatter = Create_Particle([mouse_x, mouse_y],[random.randrange(-3,3),random.randrange(-3,3)],
			[random.randint(4,8),0.1,0.1,0,((225,0,0))],[0.5,map.tile_map,GRID_SIZE])
			effects.add(scatter)

	for effect in effects:
		effect.update(dt)
		effect.draw(Display)
	for projectile in projectiles:
		projectile.update(dt)
		projectile.draw(Display)
	
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

