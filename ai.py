from setup import*
import random, os

class Enemy(pygame.sprite.Sprite):
	def __init__(self,position):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.hit_box = pygame.Rect(self.position[0],self.position[1],50,50)
		self.frames = None
		self.frame_count = 0
		self.walk_countdown = 0
		self.idle_countdown = -1
		self.walk_direction = True
		self.vertical_momentum = 0
		self.state = 'walk'
	

	def collision_test(self):
		hit_list = []
		for tile in tiles:
			if tile.colliderect(self.rect):
				hit_list.append(tile)
		return hit_list
	
	def move(self,delta_time):
		move = [0,0] 
		# move[1] += self.vertical_momentum 
		# self.vertical_momentum += 0.2
		# if self.vertical_momentum > 3:
		# 	self.vertical_momentum = 3
		
		if self.idle_countdown > 0:
			self.idle_countdown -= 1

		if random.randint(1,200) == 1 and self.idle_countdown == 0 and self.state != 'attack':
			self.state = 'idle'
			self.idle_countdown = 50 

		if self.idle_countdown <= 0 and self.state != 'attack':
			self.state = 'walk'
			self.idle_countdown = 0

			if self.walk_countdown >= 80:
				self.walk_direction = not self.walk_direction
				self.walk_countdown = 0
			self.walk_countdown += 2
			
			if self.walk_direction:
				move[0] += 2 * delta_time
			else:
				move[0] -= 2 * delta_time


		self.position[0] += int(move[0])
		# self.position[1] += move[1]
		hit_list = self.collision_test()
		for tile in hit_list:
			if move[1] > 0:
				self.rect.bottom = tile.top
			elif move[1] < 0:
				self.rect.top = tile.bottom

		self.hit_box.x = self.position[0]
		self.hit_box.y = self.position[1]

		self.update(delta_time)
		
	def update(self,delta_time):
		self.frames = os.listdir(f'asset/enemy-{self.state}')
		self.frame_count += 0.2 * delta_time
		if self.frame_count >= (len(self.frames) - 1):
			self.frame_count = 0
		

	def draw(self,surface):
		pygame.draw.rect(surface, 'green', self.hit_box, 1)
		if self.frame_count <= (len(self.frames) - 1):
			image = pygame.image.load(os.path.join(f'asset/enemy-{self.state}', self.frames[int(self.frame_count)]))
			image_copy = image.copy()
			image_copy = pygame.transform.flip(image, self.walk_direction, False)
			image_copy.set_colorkey((0,0,0))
			surface.blit(image_copy, (self.position[0],self.position[1]))

tiles = []
enemy = Enemy([200, 180])

while True: # game loop
# framerate independence -------------------------------------------------#
	delta_time = time.time() - last_time
	delta_time *= 60
	last_time = time.time()
	display.fill((25,25,25))

# fill the screen --------------------------------------------------------#  
	screen.fill((25,25,25))

	enemy.move(delta_time)
	enemy.draw(screen)

	for event in pygame.event.get(): # event loop
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		
	pygame.display.update()
	clock.tick(60)
