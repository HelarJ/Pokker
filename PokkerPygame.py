import pygame
import random
import pokker
import itertools
from sys import exit

class pokkeriPõhi:
    def __init__(self):
        pygame.init()
        ekraani_laius = 900
        ekraani_kõrgus = 600
        self.aken = pygame.display.set_mode((ekraani_laius,ekraani_kõrgus))
        self.fpsKell = pygame.time.Clock()
        self.kaardid = ['2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣','A♣',
                       '2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦','A♦',
                       '2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥','A♥',
                       '2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠','A♠',]
        
        #Järgmised 8 rida vaja muuta uuesti False, et jagada uued kaardid 
        self.a = False
        self.b = False
        self.c = False
        self.flop = False
        self.turn = False
        self.river = False
        self.aTugevus = False
        self.bTugevus = False
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
        if self.flop:
            self.joonista_flop()
        if self.turn:
            self.joonista_turn()
        if self.river:
            self.joonista_river()
        
        
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
        self.aken.blit(kaart, (550, 225))
    
    def joonista_river(self):
        kaart = pygame.image.load("Kaardid/"+self.c[4]+".png")
        kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
        self.aken.blit(kaart, (700, 225))

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
        global laud
        laud = []
        for i in range(5):
            k1 = random.choice(self.uued)
            self.uued.pop(self.uued.index(k1))
            laud.append(k1)
        return laud
    
    def tugevus(self, seitsekaarti):
        print(seitsekaarti)
        kõik_variandid = itertools.combinations(seitsekaarti,5)
        parim = "Kõrge kaart"
        tugevus = 0
        for variant in kõik_variandid:
            k1 = variant[0]
            k2 = variant[1]
            k3 = variant[2]
            k4 = variant[3]
            k5 = variant[4]
            if pokker.käsi(k1,k2,k3,k4,k5)[1] > tugevus:
                tugevus = pokker.käsi(k1,k2,k3,k4,k5)[1]
                parim = pokker.käsi(k1,k2,k3,k4,k5)[0]
        print("Mängija", parim, tugevus)
        return (parim, tugevus)
    
        

    def pokkeriKordus(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
            #ALATES SIIT
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not self.flop:
                        self.flop = True
                    elif self.flop and not self.turn:
                        self.turn = True
                    elif self.flop and self.turn and not self.river:
                        self.river = True  
            if not self.a:
                self.a = self.käsi()
                print(self.a)
            if not self.b:
                self.b = self.käsi()
                print(self.b)
            if not self.c:
                self.c = self.lauaKaardid()
                print(self.c)
            self.joonista_kaardid()
            if not self.aTugevus and not self.bTugevus and self.a and self.b and self.c:
                self.aKaardid = self.a + laud
                self.aTugevus = self.tugevus(self.aKaardid)
                self.bKaardid = self.b + laud
                self.bTugevus = self.tugevus(self.bKaardid)
           
           #KUNI SIIANI on ühe käe mängimine. Kui käsi mängitud, vaja see osa nullist alustada
           
           

            pygame.display.update()
            self.fpsKell.tick(30)

põhiaken = pokkeriPõhi()
põhiaken.pokkeriKordus()
