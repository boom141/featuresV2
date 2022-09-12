from setup import*
from map_loader import*
from entity_class import*


player = Player(125,80)
enemy = Enemy(280,120)
meter = Meter()


location1 = [[30,183],[250, 183]]
location2 = [[200,100],[400,140]]

for position in location1:
    tree = Trees(position[0], position[1])
    trees.add(tree)

for position in location2:
    droplet = Droplet(position[0], position[1])
    droplets.add(droplet)
 

while True: # game loop
#framerate independence -------------------------------------------------#
    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()
    display.fill((25,25,25)) 

#camera ----------------------------------------------------------------#
    scroll[0] += (player.rect.x-scroll[0]-128)/20
    scroll[1] += (player.rect.y-scroll[1]-115)/20
# draw section----------------------------------------------------------#
    for tree in trees:
        tree.update(dt)
        tree.draw(display)
    
    for droplet in droplets:
        droplet.update(dt)
        droplet.player_collision(player.rect)
        droplet.draw(display)
    
    for projectile in projectiles:
        projectile.update(dt)
        projectile.draw(display)

    map.initialize(display)
    player.move(dt)
    player.draw(display)
    enemy.move(dt)
    enemy.draw(display,player.rect)
    meter.draw(display)

    for particle in particles:
        particle.update(dt)
        particle.draw(display)   
    
    for effect in effects:
        effect.update(dt)
        effect.draw(display)
    


    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_d:
                keys['right'] = True
            if event.key == K_a:
               keys['left'] = True
            if event.key == K_SPACE:
                keys['jump'] = True

        if event.type == KEYUP:
            if event.key == K_d:
               keys['right'] = False
            if event.key == K_a:
               keys['left'] = False
            if event.key == K_SPACE:
               keys['jump'] = False
        
    screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)
