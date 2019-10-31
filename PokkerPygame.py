import pygame
import random
import pokker
import itertools
from sys import exit

class pokkeriPõhi:
    def __init__(self):
        pygame.init()
        ekraani_laius = 900
        self.lü = ekraani_laius/100 #laiuseühik
        ekraani_kõrgus = 600
        self.kü = ekraani_kõrgus/100 #kõrguseühik
        self.aken = pygame.display.set_mode((ekraani_laius,ekraani_kõrgus))
        self.fpsKell = pygame.time.Clock()
        self.kaardid = ['2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣','A♣',
                        '2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦','A♦',
                        '2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥','A♥',
                        '2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠','A♠',]
        
        self.mängijatearv = 8
        self.algasukohad = [(350,10), (350,450), (10,200), (730,200), (10,10), (10,450), (730, 10), (730,450)]
        self.chipikohad = [(350,140), (350,580), (10,330), (730,330), (10,140), (10,580), (730, 140), (730,580)]
        self.chips = [5000]*self.mängijatearv
        
       
        #Järgmised read vaja muuta uuesti False, et jagada uued kaardid 
        self.mängijad, self.laud, self.tugevused, self.võitja = [],[],[],[]
        self.flop, self.turn, self.river, self.kk = False,False,False,False
        self.uued = self.kaardid.copy()
        
        self.font = pygame.font.SysFont('arial', 32) 
            
            
    def joonista_kaardid(self):
        for i in range(len(self.mängijad)):
            j = 0
            for knimi in self.mängijad[i]:
                kaart = pygame.image.load("Kaardid/"+knimi+".png")
                kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
                self.aken.blit(kaart, (self.algasukohad[i][0]+j, self.algasukohad[i][1]))
                j+=55


        if self.flop:
            self.joonista_flop()
        if self.turn:
            self.joonista_turn()
        if self.river:
            self.joonista_river()
        
        
    def joonista_flop(self):
        kaardid = self.laud[:3]
        i = 0
        for nimi in kaardid:
            kaart = pygame.image.load("Kaardid/"+nimi+".png")
            kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
            self.aken.blit(kaart, (i+200, 225))
            i += 115
    
    def joonista_turn(self):
        kaart = pygame.image.load("Kaardid/"+self.laud[3]+".png")
        kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
        self.aken.blit(kaart, (545, 225))
    
    def joonista_river(self):
        kaart = pygame.image.load("Kaardid/"+self.laud[4]+".png")
        kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
        self.aken.blit(kaart, (657, 225))

    def joonista_tekst(self):
        for i in range(self.mängijatearv):
            self.aken.blit(pygame.font.SysFont('arial', 52).render(str(i+1), True, (10, 10, 10), (200,200,200)), (self.algasukohad[i][0]+50,self.algasukohad[i][1]+30))
        for i in range(self.mängijatearv):
            self.aken.blit(pygame.font.SysFont('arial', 25).render(str(self.chips[i]), True, (10, 10, 10), (200,200,200)), self.chipikohad[i])
        võitjastr = "Mängija " + str(self.võitja[0]) + " on võitja | "+ self.võitja[1][0]
        if self.river:
            self.aken.blit(self.font.render(võitjastr, True, (255, 255, 255)), (250,150))
            
        self.aken.blit(self.font.render("Uus mäng", True, (255, 255, 255), (10,10,10)), (780,10))
        

    def käsi(self):
        käsi = []
        for i in range(2):
            k1 = random.choice(self.uued)
            self.uued.pop(self.uued.index(k1))
            käsi.append(k1)
        return käsi

    def lauaKaardid(self):
        uuslaud = []
        for i in range(5):
            k1 = random.choice(self.uued)
            self.uued.pop(self.uued.index(k1))
            uuslaud.append(k1)
        return uuslaud
    
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
            uustugevus = pokker.käsi(k1,k2,k3,k4,k5)
            if uustugevus[1] > tugevus:
                tugevus = uustugevus[1]
                parim = uustugevus[0]
        print("Mängija", parim, tugevus)
        return (parim, tugevus)
    
    def loo_mängijad(self):
        uuedmängijad = []
        for i in range(self.mängijatearv):
            uuedmängijad.append(self.käsi())
        return uuedmängijad

    def leia_tugevused(self):
        uuedtugevused = []
        for mängija in self.mängijad:
            uuedtugevused.append(self.tugevus(mängija + self.laud))
        print("tugevused", uuedtugevused)
        return uuedtugevused
    
    def leia_võitja(self):
        uusvõitja = [[0],(0,0)]
        for i in range(len(self.tugevused)):
            if self.tugevused[i][1] > uusvõitja[1][1]:
                uusvõitja = ([i+1],self.tugevused[i])
            elif self.tugevused[i][1] == uusvõitja[1][1]:
                uusvõitja[0].append(i+1)

        print("võitja", uusvõitja)
        self.võitja = uusvõitja
        
            

    def pokkeriKordus(self):
        while True:
            self.aken.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] in range(770,900) and pygame.mouse.get_pos()[1] in range(0,40):
                       self.mängijad, self.laud, self.tugevused, self.võitja = [],[],[],[]
                       self.flop, self.turn, self.river = False,False,False
                       self.uued = self.kaardid.copy()
                    elif not self.flop and self.kk:
                        self.flop = True
                    elif self.flop and not self.turn and self.kk:
                        self.turn = True
                    elif self.flop and self.turn and not self.river and self.kk:
                        self.river = True
                    
            if not self.mängijad:
                self.mängijad = self.loo_mängijad()
                print("mängijad",self.mängijad)
            
            if not self.laud:
                self.laud = self.lauaKaardid()

            self.joonista_kaardid()
            if not self.tugevused:
                self.tugevused = self.leia_tugevused()
                self.leia_võitja()

            self.joonista_tekst()
            pygame.display.update()
            self.fpsKell.tick(30)

põhiaken = pokkeriPõhi()
põhiaken.pokkeriKordus()
