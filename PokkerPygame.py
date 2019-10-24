import pygame
from sys import exit
class pokkeriPõhi:
    def __init__(self):
        pygame.init()
        ekraani_laius = 900
        ekraani_kõrgus = 600
        self.aken = pygame.display.set_mode((ekraani_laius,ekraani_kõrgus))
        self.fpsKell = pygame.time.Clock()
    
    def pokkeriKordus(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            kaart = pygame.image.load("kaardid\/ärtu2.png")
            kaart = pygame.transform.rotozoom(kaart, 0, 0.15)
            self.aken.blit(kaart, (0, 0))
            pygame.display.update()
            self.fpsKell.tick(30)

põhiaken = pokkeriPõhi()
põhiaken.pokkeriKordus()
