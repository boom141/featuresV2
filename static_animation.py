import os
from setup import*

class Static_Animation(pygame.sprite.Sprite):
    def __init__(self, position, folder_name, speed):
        pygame.sprite.Sprite.__init__(self)
        self.folder_name =folder_name
        self.frames = os.listdir(f'asset/{self.folder_name}')
        self.frame_count = 0
        self.position = position
        self.speed = speed

    def update(self,delta_time):    
        self.frame_count += self.speed * delta_time
        if self.frame_count >= (len(self.frames) - 1):
            self.frame_count = 0

    def draw(self,surface):
        if self.frame_count <= (len(self.frames) - 1):
            image = pygame.image.load(os.path.join(f'asset/{self.folder_name}', self.frames[int(self.frame_count)]))
            image.set_colorkey((0,0,0))
            surface.blit(image, (self.position[0],self.position[1]))

static_animations = pygame.sprite.Group()

location1 = [[30,183],[250, 183]]

for location in location1:
    tree = Static_Animation(location, 'tree', 0.2,)
    static_animations.add(tree) 

while True: # game loop
# framerate independence -------------------------------------------------#
    delta_time = time.time() - last_time
    delta_time *= 60
    last_time = time.time()
    display.fill((25,25,25))

# fill the screen --------------------------------------------------------#  
    screen.fill((25,25,25))

    for animation in static_animations:
        animation.update(delta_time)
        animation.draw(screen)

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
    pygame.display.update()
    clock.tick(60)
