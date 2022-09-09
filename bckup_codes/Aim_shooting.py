import pygame ,os, math, sys, random
from weapons import Weapon_List

pygame.init()

WIDTH ,HEIGHT = 400,400
Display = pygame.display.set_mode((WIDTH, HEIGHT))
Window = pygame.Surface((WIDTH,HEIGHT))
pygame.display.set_caption('Aim and shoot Test')
CLOCK = pygame.time.Clock()
GRID_SIZE = 80

bullet_img = pygame.image.load(os.path.join('asset','Laser.png'))
bullet_img_copy = bullet_img.copy()
bullet_img_copy = pygame.transform.scale(bullet_img,(40,30))
bullet_img_copy.set_colorkey((0,0,0))

class Current_Weapon(pygame.sprite.Sprite):
	def __init__(self, surface):
		pygame.sprite.Sprite.__init__(self)
		self.surface = surface

	def Update(self, weapon_name, weapon_position, facing):
		sprite_image = pygame.image.load(os.path.join('asset', f'{weapon_name}{facing}.png')) #original image
		sprite_object =  sprite_image.copy() # reserve for containing the upadated transform in image / also the one that we need to blit
		sprite_rect = sprite_object.get_rect(center=(weapon_position[0],weapon_position[0])) # declaring values for the center position of the image
		mouse_position = pygame.mouse.get_pos()
		sprite_center = sprite_rect.center
		distance_x = mouse_position[0] - sprite_center[0]
		distance_y = mouse_position[1] - sprite_center[1]
		angle = math.degrees(math.atan2(distance_y,distance_x))

		self.sprite_object = pygame.transform.rotate(sprite_image, -angle).convert_alpha()
		self.sprite_rect = self.sprite_object.get_rect(center=(sprite_center[0],sprite_center[1])) #reposition of image

	def Draw(self):
		self.surface.blit(self.sprite_object,self.sprite_rect)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, weapon_name, weapon_list, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img_copy
		self.rect = self.image.get_rect()
		self.weapon_list = weapon_list
		self.weapon_name = weapon_name
		self.position = position
		self.mouse_position = pygame.mouse.get_pos()
		self.distance_x = self.mouse_position[0] - self.position[0]
		self.distance_y = self.mouse_position[1] - self.position[1]
		self.direction_x = math.cos(math.atan2(self.distance_y,self.distance_x))
		self.direction_y = math.sin(math.atan2(self.distance_y,self.distance_x))
	
	def update(self):
		self.position[0] += self.direction_x * self.weapon_list[self.weapon_name]['bullet_speed']
		self.position[1] += self.direction_y * self.weapon_list[self.weapon_name]['bullet_speed']
		self.rect.x = self.position[0]
		self.rect.y = self.position[1]
		if self.rect.right < 0 or self.rect.left > WIDTH:
			self.kill()


sprite_image_crosser = pygame.image.load(os.path.join('asset', 'crosser.png'))
sprite_crosser_object = sprite_image_crosser.copy()

facing = 'left'

bullet_list = []
tile_map = {}

cooldown = 0

bullet_list = pygame.sprite.Group()

current_weapon = Current_Weapon(Window)
while True:
	Window.fill((40,40,40))
	CLOCK.tick(60)
	pygame.mouse.set_visible(False)
	
	horizontal_grid_size = (pygame.mouse.get_pos()[0]//30)
	if horizontal_grid_size < 6:
		facing = 'right'
	else:
		facing = 'left'


	current_weapon.Update('gun_ak_', [200,200], facing)
	current_weapon.Draw()

	sprite_crosser_object = pygame.transform.scale(sprite_image_crosser,(30,30)).convert_alpha()
	sprite_crosser_rect = sprite_crosser_object.get_rect()

	Window.blit(sprite_crosser_object,(pygame.mouse.get_pos()[0] - sprite_crosser_rect.centerx,pygame.mouse.get_pos()[1] - sprite_crosser_rect.centery))

	if cooldown > 0:
		cooldown -= 1

	if pygame.mouse.get_pressed()[0]:
		if cooldown == 0:
			cooldown = Weapon_List['gun_ak']['bullet_cooldown']
			bullet = Bullet('gun_ak', Weapon_List, [200,200])
			bullet_list.add(bullet)
	
	bullet_list.update()
	bullet_list.draw(Window)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	Display.blit(Window,(0,0))
	pygame.display.update()
