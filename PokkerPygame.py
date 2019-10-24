import pygame
import random
from sys import exit
class pokkeriPõhi:
    def __init__(self):
        pygame.init()
        ekraani_laius = 900
        ekraani_kõrgus = 600
        self.aken = pygame.display.set_mode((ekraani_laius,ekraani_kõrgus))
        self.fpsKell = pygame.time.Clock()
        self.a = False
        self.b = False
        self.kaardid = ['2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣','A♣',
               '2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦','A♦',
               '2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥','A♥',
               '2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠','A♠',]
        self.uued = self.kaardid.copy()
    
    def pokkeriKordus(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            kaart = pygame.image.load("kaardid/ärtu2.png")
            kaart = pygame.transform.rotozoom(kaart, 0, 0.15)
            self.aken.blit(kaart, (0, 0))
            pygame.display.update()
            self.fpsKell.tick(30)
            if not self.a:
                self.a = self.käsi()
                print(self.a)
            if not self.b:
                self.b = self.käsi()
                print(self.b)
            
    def joonista_kaardid(self):
        kaardid = self.a
        for kaart in kaardid:
            
            
    def käsi(self):
        käsi = []
        for i in range(5):
            k1 = random.choice(self.uued)
            self.uued.pop(self.uued.index(k1))
            käsi.append(k1)
        return käsi

põhiaken = pokkeriPõhi()
põhiaken.pokkeriKordus()
