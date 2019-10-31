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
        self.kaardipildid = {}
        for knimi in self.kaardid:
            kaart = pygame.image.load("Kaardid/"+knimi+".png")
            kaart = pygame.transform.rotozoom(kaart, 0, 0.1)
            self.kaardipildid[knimi] = kaart #Laeb kõik pildid juba mällu et mäng toimuks kiiremini ja programm kasutaks vähem resursse


        self.mängijatearv = 8
        self.algasukohad = [(350,10), (350,450), (10,200), (730,200), (10,10), (10,450), (730, 10), (730,450)]
        self.chipikohad = [(350,140), (350,580), (10,330), (730,330), (10,140), (10,580), (730, 140), (730,580)]
        self.chipid = [5000]*self.mängijatearv
        self.pot = 0
        
       
        #Järgmised read vaja muuta uuesti False, et jagada uued kaardid 
        self.mängijad, self.laud, self.tugevused, self.võitja = [],[],[],[]
        self.flop, self.turn, self.river, self.kk, self.läbi = False,False,False,False,False
        self.kellekäik = 0
        self.uued = self.kaardid.copy()
        
        self.font = pygame.font.SysFont('arial', 32) 
            
    def joonista_kaardid(self):
        for i in range(len(self.mängijad)):
            j = 0
            for knimi in self.mängijad[i]:
                kaart = self.kaardipildid[knimi]
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
        for knimi in kaardid:
            kaart = self.kaardipildid[knimi]
            self.aken.blit(kaart, (i+200, 225))
            i += 115
    
    def joonista_turn(self):
        kaart = self.kaardipildid[self.laud[3]]
        self.aken.blit(kaart, (545, 225))
    
    def joonista_river(self):
        kaart = self.kaardipildid[self.laud[4]]
        self.aken.blit(kaart, (657, 225))

    def joonista_tekst(self):
        for i in range(self.mängijatearv):
            self.aken.blit(pygame.font.SysFont('arial', 52).render(str(i+1), True, (10, 10, 10), (200,200,200)), (self.algasukohad[i][0]+50,self.algasukohad[i][1]+30))
        for i in range(self.mängijatearv):
            self.aken.blit(pygame.font.SysFont('arial', 25).render(str(self.chipid[i]), True, (10, 10, 10), (200,200,200)), self.chipikohad[i])
        võitjastr = "Mängija " + str(self.võitja[0]) + " on võitja | "+ self.võitja[1][0]
        if self.river:
            self.aken.blit(self.font.render(võitjastr, True, (255, 255, 255)), (250,150))
        
        mängijastr = "Mängija " + str(self.kellekäik+1) + " [R] Panusta 100, [F] Fold"
        if not self.river:#joonistab ainult siis kui mäng veel lõppenud pole
            self.aken.blit(self.font.render(mängijastr, True, (255, 255, 255)), (250,400))
            
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
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        if not self.läbi:
                            if self.chipid[self.kellekäik] >= 100: #kui mängijal on piisavalt chippe
                                self.chipid[self.kellekäik] -= 100 #võetakse mängijalt need ära
                                self.pot += 100                    #ja lisatakse potti
                                self.kellekäik += 1
                                if self.kellekäik >= len(self.mängijad): #kui kõik on ära käinud
                                    self.kk = True


                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] in range(770,900) and pygame.mouse.get_pos()[1] in range(0,40):
                       self.mängijad, self.laud, self.tugevused, self.võitja = [],[],[],[]
                       self.flop, self.turn, self.river,self.kk, self.läbi = False,False,False,False,False
                       self.kellekäik = 0
                       self.pot = 0
                       self.uued = self.kaardid.copy()
                    
            if not self.mängijad:
                self.mängijad = self.loo_mängijad()
                print("mängijad",self.mängijad)
            
            if not self.laud:
                self.laud = self.lauaKaardid()

            self.joonista_kaardid()
            if not self.tugevused:
                self.tugevused = self.leia_tugevused()
                self.leia_võitja()
            if not self.flop and self.kk:
                self.flop = True
                self.kk = False
                self.kellekäik = 0
            elif self.flop and not self.turn and self.kk:
                self.turn = True
                self.kk = False
                self.kellekäik = 0
            elif self.flop and self.turn and not self.river and self.kk:
                self.river = True
                jagatudpot = self.pot/len(self.võitja[0])
                for võit in self.võitja[0]:
                    self.chipid[võit-1] += round(jagatudpot)
                self.läbi = True





            self.joonista_tekst()
            pygame.display.update()
            self.fpsKell.tick(30)

põhiaken = pokkeriPõhi()
põhiaken.pokkeriKordus()
