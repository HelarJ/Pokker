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
    
        
        
    display.fill((50, 150, 40))
    pygame.display.update()
    
pygame.quit()
exit()