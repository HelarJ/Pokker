import pygame
import random
import pokker
import itertools
import math
import asyncio
import websockets
import threading
import json
from sys import exit

class pokkeriPõhi:
    def __init__(self):
        pygame.init()
        ekraani_laius = 1280
        self.lü = ekraani_laius/100 #laiuseühik
        ekraani_kõrgus = 680
        self.kü = (ekraani_laius/1.87)/100
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
        self.chipid = [5000]*23
       
        self.tühi_plats()
        self.esialgne = True
        
        self.font = pygame.font.SysFont('arial', int(self.lü * 2.1))

    def tühi_plats(self): #teeb tühjad järjendid, väärtused et saaks alustada uut mängu.
        if len(connected.keys()) >= 1:
            self.mängijatearv = len(connected.keys())
            i = 0
            for mängija in connected.keys():
                connected[mängija]["number"] = i
                self.chipid[i] == connected[mängija]["chipid"]
                i+=1

        self.mängijad, self.laud, self.tugevused, self.võitja = [],[],[],[]
        self.flop, self.turn, self.river, self.kk, self.läbi, self.aktiivne, = False,False,False,False,False,False
        self.liigamadal = False
        self.esialgne = False
        self.interneti_käik = ""
        
        self.bet = ''
        self.bet_int = 0
        self.uued_käigud = []
        self.panused = [0] * self.mängijatearv
        self.kellekäik = 0
        self.pot = 0
        self.sidepotid = []
        self.folditud = []
        self.allin = []
        self.uued = self.kaardid.copy()
        for i in range(len(self.chipid)):
            if self.chipid[i] == 0:
                self.folditud.append(i)
        self.interneti_andmed = {"laud":[], "panused":self.panused, "pot":self.pot, "folditud":self.folditud, 
                                 "kellek2ik":self.kellekäik, "chipid":self.chipid}
        try:
            self.interneti_andmed.pop("v6itja")
        except Exception:
            pass

        self.algasukohad, self.chipikohad, self.panusekohad = [(0, 0)]*self.mängijatearv,[(0, 0)]*self.mängijatearv,[(0, 0)]*self.mängijatearv
        self.arvuta_koordinaadid()
        if len(connected.keys()) >= 1:
            for element in connected.keys():
                täielikudandmed = põhiaken.interneti_andmed.copy()
                try:
                    täielikudandmed["k2si"] = connected[element]["k2si"]
                    täielikudandmed["number"] = connected[element]["number"]
                except:
                    continue
                asyncio.ensure_future(connected[element]["socket"].send(json.dumps(täielikudandmed)))


    def arvuta_koordinaadid(self):
        r = self.lü*19
        x0 = self.lü*44
        y0 = self.kü*39
        nurk = 360/self.mängijatearv
        for i in range(self.mängijatearv):
            x = r * 2.25* math.cos((i * nurk +90) * math.pi/180)
            y = r * math.sin((i * nurk +90) * math.pi/180)
            self.algasukohad[i]= (x0+x, y0+y)
            self.chipikohad[i]= (x0+x, y0+y+self.kü*18)
            self.panusekohad[i]= (x0+x +self.lü*4, y0+y+self.kü*18)


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
        self.interneti_andmed["laud"] = self.laud[:3]
        kaardid = self.laud[:3]
        i = 0
        for knimi in kaardid:
            kaart = self.kaardipildid[knimi]
            kaart = pygame.transform.rotozoom(kaart, 0, self.lü / 135)
            self.aken.blit(kaart, (i+(self.lü * 28), self.kü * 37))
            i += self.lü*9
    
    def joonista_turn(self):
        self.interneti_andmed["laud"] = self.laud[:4]
        kaart = self.kaardipildid[self.laud[3]]
        kaart = pygame.transform.rotozoom(kaart, 0, self.lü / 135)
        self.aken.blit(kaart, (self.lü*9*3 + self.lü * 28, self.kü * 37))
    
    def joonista_river(self):
        self.interneti_andmed["laud"] = self.laud
        kaart = self.kaardipildid[self.laud[4]]
        kaart = pygame.transform.rotozoom(kaart, 0, self.lü / 135)
        self.aken.blit(kaart, (self.lü*9*4 + self.lü * 28, self.kü * 37))

    def joonista_tekst(self):
        self.font = pygame.font.SysFont('arial', int(self.lü * 2.1))
        for i in range(self.mängijatearv): #joonistab numbrid kaartide peale
            self.aken.blit(pygame.font.SysFont('arial', int(self.lü *3)).render(str(i+1), True, (10, 10, 10), (200,200,200)), (self.algasukohad[i][0]+self.lü*4,self.algasukohad[i][1]+self.lü*3))
        
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
            if max(self.panused) > self.chipid[self.kellekäik]:
                mängijastr = "Mängija " + str(self.kellekäik+1) + " [F] Fold, [C] All In"
            else:
                mängijastr = "Mängija " + str(self.kellekäik+1) + " [R] " + panuseSumma + ", [F] Fold, [C] Check/Call"
            self.aken.blit(self.font.render(mängijastr, True, (255, 255, 255), (25,100,0)), (self.lü * 31, self.kü * 69))
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
            uuskäsi = self.käsi()
            uuedmängijad.append(uuskäsi)
            for mängija, sisu in connected.items():
                if sisu["number"] == i:
                    sisu["k2si"] = uuskäsi
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
        self.interneti_andmed["v6itja"] = self.võitja
    
    def kontrolli_lõppu(self): #false kui veel vaja käia, true kui kõikide panused on võrdsed
        self.uued_käigud = []
        for i in range(len(self.panused)):
            if self.panused[i] != max(self.panused) and i not in self.folditud and i not in self.allin and self.chipid[i] != 0: #kui panus pole piisavalt kõrge ja mängija pole foldinud
                self.uued_käigud.append(i)
        print(self.panused)
        #print(self.uued_käigud)
        if len(self.uued_käigud) > 0:
            self.kellekäik = 0
            self.interneti_andmed["kellek2ik"] = self.kellekäik
            return False
        else:
            for i in range(len(self.mängijad)):
                self.chipid[i] -= self.panused[i]
            self.pot += sum(self.panused)
            self.panused = [0] * self.mängijatearv
            self.interneti_andmed["pot"] = self.pot
            self.interneti_andmed["panused"] = self.panused
            self.interneti_andmed["chipid"] = self.chipid
            return True

    def tee_interneti_käik(self, käik):
        print(käik)
        self.interneti_käik = käik
        try: 
            connected[self.interneti_käik[0]]["number"]
        except:
            return
        if not self.esialgne and self.interneti_käik and self.kellekäik == connected[self.interneti_käik[0]]["number"]:
            print("jõudis kontrolli", self.interneti_käik)
            if self.interneti_käik[1] == "C":
                self.kontrolli_check()
            elif self.interneti_käik[1] == "F":
                self.kontrolli_fold()
            elif self.interneti_käik[1][0] == "R":
                self.bet = self.interneti_käik[1][1:]
                self.bet_int = int(self.bet)
                self.kontrolli_raise()

    def kontrolli_raise(self):
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
        self.interneti_andmed["kellek2ik"] = self.kellekäik
        self.interneti_andmed["panused"] = self.panused
    
    def kontrolli_fold(self):
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
        self.interneti_andmed["kellek2ik"] = self.kellekäik
        self.interneti_andmed["folditud"] = self.folditud

    def kontrolli_check(self):
        if not self.läbi and self.kellekäik not in self.folditud and max(self.panused) == 0:
            self.kellekäik += 1
        if not self.läbi and self.kellekäik not in self.folditud and max(self.panused) > 0:
            self.panused[self.kellekäik] = min(max(self.panused), self.chipid[self.kellekäik])
            if self.chipid[self.kellekäik] < max(self.panused):
                self.allin.append(self.kellekäik)
            self.liigamadal = False
            self.kellekäik += 1
        if self.kellekäik >= len(self.mängijad): #kui kõik on ära käinud                            
            if self.kontrolli_lõppu():
                self.kk = True
                self.panused = [0] * self.mängijatearv #tühjendab panustelisti

            self.kellekäik = 0
            self.bet_int = 0
        self.interneti_andmed["kellek2ik"] = self.kellekäik


            
    def pokkeriKordus(self):
        while True:
            self.aken.fill((25,100,0))
            värv = (255, 255, 255) if self.aktiivne else (0, 0, 0)

            if self.kellekäik in self.folditud or self.kellekäik in self.allin or(self.kellekäik not in self.uued_käigud and len(self.uued_käigud) > 0) or self.chipid[self.kellekäik] == 0: #kui mängija on foldinud või ei pea uuesti käima
                    self.kellekäik += 1
                    if self.kellekäik == self.mängijatearv:
                        if self.kontrolli_lõppu():
                            self.kk = True
                        self.kellekäik = 0
                    self.interneti_andmed["kellek2ik"] = self.kellekäik

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    suletud[0] = True
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


                    if event.key == pygame.K_r and not self.aktiivne and self.chipid[self.kellekäik] >= max(self.panused):
                        self.kontrolli_raise()
                                 
                    if event.key == pygame.K_f and not self.aktiivne:
                        self.kontrolli_fold()
                        
                    if event.key == pygame.K_c and not self.aktiivne:
                        self.kontrolli_check()
                    
                    if event.key == pygame.K_p:
                        for element in connected.keys():
                            asyncio.ensure_future(connected[element]["socket"].send(json.dumps(self.interneti_andmed)))
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if pygame.mouse.get_pos()[0] in range(0, 130) and pygame.mouse.get_pos()[1] in range(0,40):
                        self.tühi_plats()
                    if pygame.mouse.get_pos()[0] in range(int(self.lü * 40), int(self.lü * 65)) and pygame.mouse.get_pos()[1] in range(int(self.kü * 60), int(self.kü * 67)):
                        self.aktiivne = True

                elif event.type == pygame.VIDEORESIZE:
                    ekraani_laius, ekraani_kõrgus = event.size[0], event.size[1]
                    self.aken = pygame.display.set_mode((ekraani_laius, ekraani_kõrgus), pygame.RESIZABLE)
                    self.lü = ekraani_laius / 100
                    self.kü = (ekraani_laius/1.87)/ 100
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


connected = {}
põhiaken = pokkeriPõhi()

suletud = [False]




async def handler(websocket, path):
    sõnum = await websocket.recv()
    print("recv:", sõnum)
    connected[sõnum[:6]] = {"socket":websocket}
    connected[sõnum[:6]]["chipid"] = 5000
    vastus = "Tere " +  sõnum[:6]
    await websocket.send(vastus)
    sõnum = await websocket.recv()
    connected[sõnum[:6]]["nimi"] = sõnum[12:]
    vastus = "Registreeritud"
    await websocket.send(vastus)
    
    while True:
        try:
            sõnum = await websocket.recv()
            if sõnum[7:11] == "k2ik":
                põhiaken.tee_interneti_käik((sõnum[:6],sõnum[12:]))
                await asyncio.sleep(1)
                käigustr = ""
                try:
                    if sõnum[12] == "R":
                        käigustr = "chat:"+connected[sõnum[:6]]["nimi"]+"("+str(connected[sõnum[:6]]["number"]+1)+") tõstis panust "+ sõnum[13:] + "-ni"
                    elif sõnum[12] == "C":
                        käigustr = "chat:"+connected[sõnum[:6]]["nimi"]+"("+str(connected[sõnum[:6]]["number"]+1)+") checkis/callis"
                    elif sõnum[12] == "F":
                        käigustr = "chat:"+connected[sõnum[:6]]["nimi"]+"("+str(connected[sõnum[:6]]["number"]+1)+") foldis"
                except Exception:
                    pass
                for element in connected.keys():
                    #print(element)
                    await connected[element]["socket"].send(käigustr)
                    täielikudandmed = põhiaken.interneti_andmed.copy()
                    try:
                        täielikudandmed["k2si"] = connected[element]["k2si"]
                        täielikudandmed["number"] = connected[element]["number"]
                    except:
                        continue
                    
                    await connected[element]["socket"].send(json.dumps(täielikudandmed))
            if sõnum[7:11] == "chat":
                for element in connected.keys():
                    try:
                        await connected[element]["socket"].send("chat:"+connected[sõnum[:6]]["nimi"]+"("+str(connected[sõnum[:6]]["number"]+1)+"): "+ sõnum[12:])
                    except:
                        await connected[element]["socket"].send("chat:"+connected[sõnum[:6]]["nimi"]+": "+ sõnum[12:])

            print("recv:", sõnum)
            
            print(connected)
            
        except websockets.ConnectionClosed:
            for mängija, element in connected.items():
                if element["socket"] == websocket:
                    põhiaken.tee_interneti_käik((mängija,"F"))
                    try:
                        if element["number"] not in põhiaken.folditud:
                            põhiaken.folditud.append(element["number"])
                    except Exception:
                        pass
                    

                    connected.pop(mängija)
                    break
            print("Ühendus suletud")
            break
        if suletud[0]:
            asyncio.get_event_loop().stop()
            break
        
        



start_server = websockets.serve(handler, "127.0.0.1", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("Server started")
serverithread = threading.Thread(target=asyncio.get_event_loop().run_forever)


serverithread.start()


põhiaken.pokkeriKordus()

