def tee_numbriks(kaart):
    if kaart[:-1] == "J":
        return 11
    elif kaart[:-1] == "Q":
        return 12
    elif kaart[:-1] == "K":
        return 13
    elif kaart[:-1] == "A":
        return 14
    else:
        return int(kaart[:-1])
    
def yks_paar(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1]:
        return tee_numbriks(k1)
    if k2[:-1] in k3[:-1]:
        return tee_numbriks(k2)
    if k3[:-1] in k4[:-1]:
        return tee_numbriks(k3)
    if k4[:-1] in k5[:-1]:
        return tee_numbriks(k4)
    
def kaks_paari(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k3[:-1] in k4[:-1]:
        return tee_numbriks(k3)
    if k1[:-1] in k2[:-1] and k4[:-1] in k5[:-1]:
        return tee_numbriks(k4)
    if k2[:-1] in k3[:-1] and k4[:-1] in k5[:-1]:
        return tee_numbriks(k4)
    
def kolmik(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k1[:-1] in k3[:-1]:
        return tee_numbriks(k1)
    if k2[:-1] in k3[:-1] and k2[:-1] in k4[:-1]:
        return tee_numbriks(k2)
    if k3[:-1] in k4[:-1] and k3[:-1] in k5[:-1]:
        return tee_numbriks(k3)
    
def rida(k1, k2, k3, k4, k5):
    k1 = int(tee_numbriks(k1))
    k2 = int(tee_numbriks(k2))
    k3 = int(tee_numbriks(k3))
    k4 = int(tee_numbriks(k4))
    k5 = int(tee_numbriks(k5))
    if k1 == k2-1 == k3-2 == k4-3 == k5-4:
        return k1
    if k5 == 14 and k1 == 2 and k2 == 3 and k3 == 4 and k4 == 5:
        return 1
        
def mast(k1, k2, k3, k4, k5):
    if k1[-1] == k2[-1] == k3[-1] == k4[-1] == k5[-1]:

        return tee_numbriks(k5)
    
def maja(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k1[:-1] in k3[:-1]:
        if k4[:-1] in k5[:-1]:
            return True
    if k3[:-1] in k4[:-1] and k3[:-1] in k5[:-1]:
        if k1[:-1] in k2[:-1]:
            return True
        
def nelik(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k1[:-1] in k3[:-1] and k1[:-1] in k4[:-1]:
        return True
    if k2[:-1] in k3[:-1] and k2[:-1] in k4[:-1] and k2[:-1] in k5[:-1]:
        return True
    
def kmastirida(k1, k2, k3, k4, k5):
    k1 = int(tee_numbriks(k1))
    k2 = int(tee_numbriks(k2))
    k3 = int(tee_numbriks(k3))
    k4 = int(tee_numbriks(k4))
    k5 = int(tee_numbriks(k5))
    if k1 == 10 and k2 == 11 and k3 == 12 and k4 == 13 and k5 == 14:
        return True

def sorteeri(k1, k2, k3, k4, k5):
    sorteeritud = []
    sorteeritud.append((tee_numbriks(k1), k1))
    sorteeritud.append((tee_numbriks(k2), k2))
    sorteeritud.append((tee_numbriks(k3), k3))
    sorteeritud.append((tee_numbriks(k4), k4))
    sorteeritud.append((tee_numbriks(k5), k5))
    sorteeritud.sort()
    
    return sorteeritud

def käsi(k1, k2, k3, k4, k5):
    s = sorteeri(k1, k2, k3, k4, k5)
    k1 = s[0][1]
    k2 = s[1][1]
    k3 = s[2][1]
    k4 = s[3][1]
    k5 = s[4][1]
    
    parim = "Kõrge kaart"
    tugevus = 0
    if yks_paar(k1, k2, k3, k4, k5):
        parim = "Üks paar"
        tugevus = 1 + (float(yks_paar(k1, k2, k3, k4, k5)))/100
    if kaks_paari(k1, k2, k3, k4, k5):
        parim = "Kaks paari"
        tugevus = 2 + (float(kaks_paari(k1, k2, k3, k4, k5)))/100
    if kolmik(k1, k2, k3, k4, k5):
        parim = "Kolmik"
        tugevus = 3 + (float(kolmik(k1, k2, k3, k4, k5)))/100
    if rida(k1, k2, k3, k4, k5):
        parim = "Rida"
        tugevus = 4.0 + (float(rida(k1, k2, k3, k4, k5)))/100
    if mast(k1, k2, k3, k4, k5):
        parim = "Mast"
        tugevus = 5.0 + (float(mast(k1, k2, k3, k4, k5)))/100
    if maja(k1, k2, k3, k4, k5):
        parim = "Maja"
        tugevus = 6.0
    if nelik(k1, k2, k3, k4, k5):
        parim = "Nelik"
        tugevus = 7.0
    if rida(k1, k2, k3, k4, k5) and mast(k1, k2, k3, k4, k5):
        parim = "Mastirida"
        tugevus = 8.0
        if kmastirida(k1, k2, k3, k4, k5):
            parim = "Kuninglik mastirida"
            tugevus = 9.0
        
        
    return (parim, tugevus)


print(käsi("A♣", "5♦", "4♣", "3♣", "2♦"))