import pygame
import random
import pokker
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
        self.c = False
        self.atugevus = 0
        self.btugevus = 0
        self.kaardid = ['2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣','A♣',
               '2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦','A♦',
               '2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥','A♥',
               '2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠','A♠',]
        self.uued = self.kaardid.copy()
        self.font = pygame.font.SysFont('arial', 32) 
            
            
    def joonista_kaardid(self):
        kaardid = self.a
        i = 0
        for nimi in kaardid:
            kaart = pygame.image.load("Kaardid/"+nimi+".png")
            kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
            self.aken.blit(kaart, (i+325, 50))
            i += 150
        kaardid = self.b
        i = 0
        for nimi in kaardid:
            kaart = pygame.image.load("Kaardid/"+nimi+".png")
            kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
            self.aken.blit(kaart, (i+325, 400))
            i += 150
        
        
    def joonista_flop(self):
        kaardid = self.c[:3]
        i = 0
        for nimi in kaardid:
            kaart = pygame.image.load("Kaardid/"+nimi+".png")
            kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
            self.aken.blit(kaart, (i+100, 225))
            i += 150
    
    def joonista_turn(self):
        kaart = pygame.image.load("Kaardid/"+self.c[3]+".png")
        kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
        self.aken.blit(kaart, (400, 225))
    
    def joonista_river(self):
        kaart = pygame.image.load("Kaardid/"+self.c[4]+".png")
        kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
        self.aken.blit(kaart, (550, 225))

#    def joonista_tekst(self):
#        if self.atugevus[1]>self.btugevus[1]:
#            võitja = "A on võitja"
#        elif self.atugevus[1]<self.btugevus[1]:
#            võitja = "B on võitja"
#        else:
#            võitja = "Viik"

#        self.aken.blit(self.font.render(võitja, False, (255, 255, 255)), (10,10))

#        self.aken.blit(self.font.render(self.atugevus[0], False, (255, 255, 255)), (300,50))

#        self.aken.blit(self.font.render(self.btugevus[0], False, (255, 255, 255)), (300,250))
        

    def käsi(self):
        käsi = []
        for i in range(2):
            k1 = random.choice(self.uued)
            self.uued.pop(self.uued.index(k1))
            käsi.append(k1)
        return käsi

    def lauaKaardid(self):
        laud = []
        for i in range(5):
            k1 = random.choice(self.uued)
            self.uued.pop(self.uued.index(k1))
            laud.append(k1)
        return laud

    def pokkeriKordus(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            if not self.a:
                self.a = self.käsi()
                print(self.a)
#                self.atugevus = pokker.käsi(self.a[0], self.a[1], self.a[2], self.a[3], self.a[4])
#                print(self.atugevus)
            if not self.b:
                self.b = self.käsi()
                print(self.b)
#                self.btugevus = pokker.käsi(self.b[0], self.b[1], self.b[2], self.b[3], self.b[4])
#                print(self.btugevus)
            if not self.c:
                self.c = self.lauaKaardid()
                print(self.c)
            self.joonista_kaardid()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.joonista_flop()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.juunista_turn()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    self.juunista_river()
                
#            self.joonista_tekst()
            pygame.display.update()
            self.fpsKell.tick(30)

põhiaken = pokkeriPõhi()
põhiaken.pokkeriKordus()
