import pygame
import random
import pokker
import itertools
import math
from sys import exit

class pokkeriPõhi:
    def __init__(self):
        pygame.init()
        ekraani_laius = 1200
        self.lü = ekraani_laius/100 #laiuseühik
        ekraani_kõrgus = 600
        #16:9
        self.kü = 16*self.lü/9
        self.aken = pygame.display.set_mode((ekraani_laius,ekraani_kõrgus), pygame.RESIZABLE)
        self.fpsKell = pygame.time.Clock()
        self.kaardid = ['2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣','A♣',
                        '2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦','A♦',
                        '2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥','A♥',
                        '2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠','A♠']
        self.kaardipildid = {}
        for knimi in self.kaardid:
            kaart = pygame.image.load("Kaardid/"+knimi+".png")
            self.kaardipildid[knimi] = kaart #Laeb kõik pildid juba mällu et mäng toimuks kiiremini ja programm kasutaks vähem resursse
        kaart = pygame.image.load("Kaardid/T.png")
        self.kaardipildid["T"] = kaart



        self.mängijatearv = 8
        self.algasukohad, self.chipikohad, self.panusekohad = [(0, 0)]*self.mängijatearv,[(0, 0)]*self.mängijatearv,[(0, 0)]*self.mängijatearv
        self.arvuta_koordinaadid()
        self.chipid = [5000]*self.mängijatearv
        self.pot = 0
       
        self.tühi_plats()
        
        
        self.font = pygame.font.SysFont('arial', int(self.lü * 2.2))

    def tühi_plats(self): #teeb tühjad järjendid, väärtused et saaks alustada uut mängu.
        self.mängijad, self.laud, self.tugevused, self.võitja = [],[],[],[]
        self.flop, self.turn, self.river, self.kk, self.läbi, self.aktiivne, = False,False,False,False,False,False
        self.liigamadal = False
        self.bet = ''
        self.bet_int = 0
        self.uued_käigud = []
        self.panused = [0] * self.mängijatearv
        self.kellekäik = 0
        self.pot = 0
        self.folditud = []
        self.uued = self.kaardid.copy()
        for i in range(len(self.chipid)):
            if self.chipid[i] == 0:
                self.folditud.append(i)

    def arvuta_koordinaadid(self):
        r = self.lü*19
        x0 = self.lü*45
        y0 = self.kü*39
        nurk = 360/self.mängijatearv
        for i in range(self.mängijatearv):
            x = r * 2.3* math.cos((i * nurk +90) * math.pi/180)
            y = r * math.sin((i * nurk +90) * math.pi/180)
            self.algasukohad[i]= (x0+x, y0+y)
            self.chipikohad[i]= (x0+x, y0+y+self.kü*19)
            self.panusekohad[i]= (x0+x +self.lü*4, y0+y+self.kü*19)


    def joonista_kaardid(self):
        for i in range(len(self.mängijad)):
            j = 0
            for knimi in self.mängijad[i]:
                kaart = self.kaardipildid[knimi]
                kaart = pygame.transform.rotozoom(kaart, 0, self.lü / 135)
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
            kaart = pygame.transform.rotozoom(kaart, 0, self.lü / 135)
            self.aken.blit(kaart, (i+(self.lü * 28), self.kü * 37))
            i += self.lü*9
    
    def joonista_turn(self):
        kaart = self.kaardipildid[self.laud[3]]
        kaart = pygame.transform.rotozoom(kaart, 0, self.lü / 135)
        self.aken.blit(kaart, (self.lü*9*3 + self.lü * 28, self.kü * 37))
    
    def joonista_river(self):
        kaart = self.kaardipildid[self.laud[4]]
        kaart = pygame.transform.rotozoom(kaart, 0, self.lü / 135)
        self.aken.blit(kaart, (self.lü*9*4 + self.lü * 28, self.kü * 37))

    def joonista_tekst(self):
        for i in range(self.mängijatearv): #joonistab numbrid kaartide peale
            self.aken.blit(pygame.font.SysFont('arial', int(self.lü *3)).render(str(i+1), True, (10, 10, 10), (200,200,200)), (self.algasukohad[i][0]+50,self.algasukohad[i][1]+30))
        
        for i in range(self.mängijatearv): #joonistab mängija kaartide alla chippide arvu ning info selle kohta kas nad on foldinud
            if i in self.folditud:
                chipistr = str(self.chipid[i]) + "[F]"
            else:
                chipistr = str(self.chipid[i])
            if self.panused[i] != 0:
                panusestr = str(self.panused[i])
                self.aken.blit(pygame.font.SysFont('arial', int(self.lü * 1.9)).render(panusestr, True, (10, 10, 10), (200, 200, 200)),self.panusekohad[i])
            self.aken.blit(pygame.font.SysFont('arial', int(self.lü * 1.9)).render(chipistr, True, (10, 10, 10), (200,200,200)), self.chipikohad[i])

        if self.pot != 0:
            potStr = "Pot " + str(self.pot)
            self.aken.blit(pygame.font.SysFont('arial', 25).render(potStr, True, (10, 10, 10), (200, 200, 200)), (200, 360))

        if self.läbi:
            võitjastr = "Mängija " + str(self.võitja[0]) + " on võitja | "+ self.võitja[1][0]
            self.aken.blit(self.font.render(võitjastr, True, (255, 255, 255)), (self.lü * 20, self.kü *60))
        
        if not self.läbi: #joonistab ainult siis kui mäng veel lõppenud pole
            if self.bet_int > max(self.panused):
                panuseSumma = "Panusta " + str(self.bet_int)
            else:
                panuseSumma = "Panusta " + str(max(self.panused))
                self.bet_int = int(max(self.panused))

            if panuseSumma[-2:] == " 0":
                panuseSumma = "Määra panus [Enter]"
            mängijastr = "Mängija " + str(self.kellekäik+1) + " [R] " + panuseSumma + ", [F] Fold, [C] Check/Call"
            self.aken.blit(self.font.render(mängijastr, True, (255, 255, 255)), (self.lü * 26, self.kü * 67))
        if self.aktiivne:
            self.aken.blit(self.font.render(self.bet, True, (255, 255, 255), (25,100,0)), (self.lü*41,self.kü*61))
        if self.liigamadal:
            self.aken.blit(self.font.render("Panus on liiga madal.", True, (255, 255, 255), (25,100,0)), (self.lü*25,self.kü*52))
            
        self.aken.blit(self.font.render("Uus mäng", True, (255, 255, 255), (25,100,0)), (5, 5))
        

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
                käsi = uustugevus[2]
        print("Mängija", parim, tugevus, käsi)
        return (parim, tugevus)
    
    def loo_mängijad(self):
        uuedmängijad = []
        for i in range(self.mängijatearv):
            uuedmängijad.append(self.käsi())
        return uuedmängijad

    def leia_tugevused(self): #leiab kõikide käte parima tugevuse
        uuedtugevused = []
        for mängija in self.mängijad:
            uuedtugevused.append(self.tugevus(mängija + self.laud)) #self.tugevus leiab parima tugevuse käe + laua kaartidest (7 kaarti)
        print("tugevused", uuedtugevused)
        return uuedtugevused
    
    def leia_võitja(self):
        uusvõitja = [[0],(0,0)]
        for i in range(len(self.tugevused)):
            if i in self.folditud:
                continue
            if self.tugevused[i][1] > uusvõitja[1][1]:
                uusvõitja = ([i+1],self.tugevused[i])
            elif self.tugevused[i][1] == uusvõitja[1][1]:
                uusvõitja[0].append(i+1)

        print("võitja", uusvõitja)
        self.võitja = uusvõitja
    
    def kontrolli_lõppu(self): #false kui veel vaja käia, true kui kõikide panused on võrdsed
        self.uued_käigud = []
        for i in range(len(self.panused)):
            if self.panused[i] != max(self.panused) and i not in self.folditud and self.chipid[i] != 0: #kui panus pole piisavalt kõrge ja mängija pole foldinud
                self.uued_käigud.append(i)
        print(self.panused)
        #print(self.uued_käigud)
        if len(self.uued_käigud) > 0:
            self.kellekäik = 0
            return False
        else:
            for i in range(len(self.mängijad)):
                self.chipid[i] -= self.panused[i]
            self.pot += sum(self.panused)
            self.panused = [0] * self.mängijatearv
            return True
            
    def pokkeriKordus(self):
        while True:
            self.aken.fill((25,100,0))
            värv = (255, 255, 255) if self.aktiivne else (0, 0, 0)

            if self.kellekäik in self.folditud or (self.kellekäik not in self.uued_käigud and len(self.uued_käigud) > 0) or self.chipid[self.kellekäik] == 0: #kui mängija on foldinud või ei pea uuesti käima
                    self.kellekäik += 1
                    if self.kellekäik == self.mängijatearv:
                        if self.kontrolli_lõppu():
                            self.kk = True
                        self.kellekäik = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
                elif event.type == pygame.KEYDOWN:
                    
                    if self.aktiivne:
                        if event.key == pygame.K_RETURN:
                            self.aktiivne = False
                            try: 
                                self.bet_int = int(self.bet) #üritab sisestatud panust numbriks muuta
                                self.bet = ""
                            except:                          #kui see ei toiminud siis tühjendab panuse ning küsib panuse uuesti.        
                                self.bet = ""
                                continue 
                        elif event.key == pygame.K_BACKSPACE:
                            self.bet = self.bet[:-1]
                        else:
                            self.bet += event.unicode
                    else: #saab enterit vajutades panuse kasti aktiivseks teha
                        if event.key == pygame.K_RETURN:
                            self.aktiivne = True


                    if event.key == pygame.K_r and not self.aktiivne:
                        if not self.läbi and self.kellekäik not in self.folditud and self.bet_int >= max(self.panused):  #ainult siis kui panus on võrdne või kõrgem eelmisest kõrgeimast panusest
                            self.liigamadal = False
                            if self.chipid[self.kellekäik] >= self.bet_int:
                                self.panused[self.kellekäik] = self.bet_int
                            else:
                                self.panused[self.kellekäik] = self.chipid[self.kellekäik]
                            self.kellekäik += 1
                        elif self.bet_int < max(self.panused):
                            self.liigamadal = True #errori ekraanile näitamiseks

                        if self.kellekäik >= len(self.mängijad): #kui kõik on ära käinud
                                if self.kontrolli_lõppu():
                                    self.kk = True
                                    self.panused = [0] * self.mängijatearv #tühjendab panustelisti

                                self.kellekäik = 0
                                self.bet_int = 0
                                
                            
                    if event.key == pygame.K_f and not self.aktiivne:
                        if not self.läbi and self.kellekäik not in self.folditud:
                            self.folditud.append(self.kellekäik)
                            self.mängijad[self.kellekäik] = ["T", "T"]
                            self.liigamadal = False
                            self.kellekäik +=1
                        if self.kellekäik >= len(self.mängijad): #kui kõik on ära käinud
                            if self.kontrolli_lõppu():
                                self.kk = True
                                self.panused = [0] * self.mängijatearv #tühjendab panustelisti

                            self.kellekäik = 0
                            self.bet_int = 0
                            
                    
                    if event.key == pygame.K_c and not self.aktiivne:
                        if not self.läbi and self.kellekäik not in self.folditud and max(self.panused) == 0:
                            self.kellekäik += 1
                        if not self.läbi and self.kellekäik not in self.folditud and max(self.panused) > 0:

                            self.panused[self.kellekäik] = min(max(self.panused), self.chipid[self.kellekäik])
                            self.liigamadal = False
                            self.kellekäik += 1
                            
                        if self.kellekäik >= len(self.mängijad): #kui kõik on ära käinud                            
                            if self.kontrolli_lõppu():
                                self.kk = True
                                self.panused = [0] * self.mängijatearv #tühjendab panustelisti

                            self.kellekäik = 0
                            self.bet_int = 0
                            
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] in range(0, 130) and pygame.mouse.get_pos()[1] in range(0,40):
                        self.tühi_plats()
                    if pygame.mouse.get_pos()[0] in range(300,601) and pygame.mouse.get_pos()[1] in range(360,391):
                        self.aktiivne = True

                elif event.type == pygame.VIDEORESIZE:
                    ekraani_laius, ekraani_kõrgus = event.size[0], event.size[1]
                    self.aken = pygame.display.set_mode((ekraani_laius, ekraani_kõrgus), pygame.RESIZABLE)
                    self.lü = ekraani_laius / 100
                    self.kü = ekraani_kõrgus / 100
                    self.arvuta_koordinaadid()

            
            if not self.mängijad:
                self.mängijad = self.loo_mängijad()
                print("mängijad",self.mängijad)

            if not self.laud:
                self.laud = self.lauaKaardid()

            self.joonista_kaardid()

            if not self.tugevused:
                self.tugevused = self.leia_tugevused()

            if not self.flop and self.kk:
                self.flop = True
                self.kk = False
                self.uued_käigud = []
                self.kellekäik = 0
            elif self.flop and not self.turn and self.kk:
                self.turn = True
                self.kk = False
                self.uued_käigud = []
                self.kellekäik = 0
                
            elif self.flop and self.turn and not self.river and self.kk:
                self.river = True
                self.kk = False
                self.uued_käigud = []
                self.kellekäik = 0
                
            elif self.flop and self.turn and self.river and self.kk and not self.läbi:
                self.uued_käigud = []
                self.leia_võitja()
                
                jagatudpot = self.pot/len(self.võitja[0]) #pot jagatud võitjate vahel
                print(jagatudpot)                    
                for võit in self.võitja[0]:
                    self.chipid[võit-1] += round(jagatudpot)
                self.läbi = True

            if len(self.mängijad)-1 <= len(self.folditud): #kui foldinud on kõik peale ühe, siis see viimane võidab
                self.flop = True
                self.turn = True
                self.kk = True
                
            if self.mängijad:
                pygame.draw.rect(self.aken, värv, (self.lü * 40, self.kü * 60, self.lü* 25, self.kü*7), 2)
                
            self.joonista_tekst()
            pygame.display.update()
            self.fpsKell.tick(30)

põhiaken = pokkeriPõhi()
põhiaken.pokkeriKordus()
