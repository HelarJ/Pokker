import pygame
from sys import exit
pygame.init()
screen_width = 900
screen_height = 600
display = pygame.display.set_mode((screen_width,screen_height))


run = True

while run:
    pygame.time.delay(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    ärtuäss = pygame.image.load('ärtuäss.png')
    ärtuäss = pygame.transform.rotozoom(ärtuäss, 0, 0.15)
    display.blit(ärtuäss, (0, 0))
        
    
    pygame.display.update()
    
pygame.quit()
exit()