import pygame

class Pulse_Ease_Out(pygame.sprite.Sprite):
	def __init__(self,position,option,color,value):
		pygame.sprite.Sprite.__init__(self)
		self.position = position
		self.radius = 0
		self.radius_value = option[0]
		self.width = option[1]
		self.duration = option[2]
		self.color = color
		self.play_animation = value

	def update(self,dt):
		if self.play_animation:
			if self.radius > self.duration - 50:
				self.radius_value = 3

		self.radius += self.radius_value * dt
		if self.radius > self.duration:
			self.play_animation = False
			self.kill()

	def draw(self,surface):
		pygame.draw.circle(surface, self.color,(self.position[0],self.position[1]),int(self.radius),self.width)

class Static_Particle(pygame.sprite.Sprite):
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