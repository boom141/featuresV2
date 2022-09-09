import pygame ,os, math, sys

pygame.init()

WIDTH ,HEIGHT = 400,400
Display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Aim and shoot Test')
clock = pygame.time.Clock()

facing = 'left'

class Current_Weapon:
    def __init__(self, weapon_name, facing,):
        self.weapon_name = weapon_name
        self.facing = facing
    
    def Deploy_Weapon(self):
        sprite_image = pygame.image.load(os.path.join('asset', f'{self.weapon_name}{self.facing}.png')) #original image
        sprite_image_copy =  sprite_image.copy() # reserve for containing the upadated transform in image / also the one that we need to blit
        sprite_image_rect = sprite_image_copy.get_rect(center=(200,200)) # declaring values for the center position of the image

        return sprite_image, sprite_image_copy, sprite_image_rect

sprite_image_crosser = pygame.image.load(os.path.join('asset', 'crosser.png'))
sprite_crosser_object = sprite_image_crosser.copy()

while True:
    Display.fill((30,30,30))
    clock.tick(60)
    pygame.mouse.set_visible(False)

    sprite_image_gun, sprite_object,  sprite_rect = Current_Weapon('gun_ak_', facing).Deploy_Weapon()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    sprite_x, sprite_y = sprite_rect.center

    distance_x = mouse_x - sprite_x
    distance_y = mouse_y - sprite_y
    
    horizontal_grid_size = (mouse_x//30)
    
    angle = math.degrees(math.atan2(distance_y,distance_x))

    sprite_crosser_object = pygame.transform.scale(sprite_image_crosser,(30,30)).convert_alpha()
    sprite_crosser_rect = sprite_crosser_object.get_rect()

    Display.blit(sprite_crosser_object,(mouse_x - sprite_crosser_rect.centerx,mouse_y - sprite_crosser_rect.centery))

    if horizontal_grid_size < 6:
        facing = 'right'
    else:
        facing = 'left'
    
    sprite_object = pygame.transform.rotate(sprite_image_gun, -angle).convert_alpha()
    sprite_rect = sprite_object.get_rect(center=(sprite_x,sprite_y)) #reposition of image
    
    Display.blit(sprite_object,sprite_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
