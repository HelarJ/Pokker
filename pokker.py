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
        return tee_numbriks(k1)/100 + tee_numbriks(k5)/10000 + tee_numbriks(k4)/1000000 + tee_numbriks(k3)/100000000
    if k2[:-1] in k3[:-1]:
        return tee_numbriks(k2)/100 + tee_numbriks(k5)/10000 + tee_numbriks(k4)/1000000 + tee_numbriks(k1)/100000000
    if k3[:-1] in k4[:-1]:
        return tee_numbriks(k3)/100 + tee_numbriks(k5)/10000 + tee_numbriks(k2)/1000000 + tee_numbriks(k1)/100000000
    if k4[:-1] in k5[:-1]:
        return tee_numbriks(k4)/100 + tee_numbriks(k3)/10000 + tee_numbriks(k2)/1000000 + tee_numbriks(k1)/100000000
    
def kaks_paari(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k3[:-1] in k4[:-1]:
        return tee_numbriks(k3)/100 + tee_numbriks(k1)/10000 + tee_numbriks(k5)/1000000
    if k1[:-1] in k2[:-1] and k4[:-1] in k5[:-1]:
        return tee_numbriks(k4)/100 + tee_numbriks(k1)/10000 + tee_numbriks(k3)/1000000
    if k2[:-1] in k3[:-1] and k4[:-1] in k5[:-1]:
        return tee_numbriks(k4)/100 + tee_numbriks(k1)/10000 + tee_numbriks(k4)/1000000
    
def kolmik(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k1[:-1] in k3[:-1]:
        return tee_numbriks(k1)/100 + tee_numbriks(k5)/10000 + tee_numbriks(k4)/1000000
    if k2[:-1] in k3[:-1] and k2[:-1] in k4[:-1]:
        return tee_numbriks(k2)/100 + tee_numbriks(k5)/10000 + tee_numbriks(k1)/1000000
    if k3[:-1] in k4[:-1] and k3[:-1] in k5[:-1]:
        return tee_numbriks(k3)/100 + tee_numbriks(k2)/10000 + tee_numbriks(k1)/1000000
    
def rida(k1, k2, k3, k4, k5):
    k1 = int(tee_numbriks(k1))
    k2 = int(tee_numbriks(k2))
    k3 = int(tee_numbriks(k3))
    k4 = int(tee_numbriks(k4))
    k5 = int(tee_numbriks(k5))
    if k1 == k2-1 == k3-2 == k4-3 == k5-4:
        return k5
    if k5 == 14 and k1 == 2 and k2 == 3 and k3 == 4 and k4 == 5:
        return 1
        
def mast(k1, k2, k3, k4, k5):
    if k1[-1] == k2[-1] == k3[-1] == k4[-1] == k5[-1]:
        return tee_numbriks(k5)/100 + tee_numbriks(k4)/10000 + tee_numbriks(k3)/1000000 + tee_numbriks(k2)/100000000 + tee_numbriks(k1)/10000000000
    
def maja(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k1[:-1] in k3[:-1]:
        if k4[:-1] in k5[:-1]:
            return tee_numbriks(k1)/100 + tee_numbriks(k4)/10000
    if k3[:-1] in k4[:-1] and k3[:-1] in k5[:-1]:
        if k1[:-1] in k2[:-1]:
            return tee_numbriks(k3)/100 + tee_numbriks(k1)/10000
        
def nelik(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k1[:-1] in k3[:-1] and k1[:-1] in k4[:-1]:
        return tee_numbriks(k1)/100 + tee_numbriks(k5)/10000
    if k2[:-1] in k3[:-1] and k2[:-1] in k4[:-1] and k2[:-1] in k5[:-1]:
        return tee_numbriks(k2)/100 + tee_numbriks(k1)/10000
    
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
    tugevus = tee_numbriks(k5)/100 + tee_numbriks(k4)/10000 + tee_numbriks(k3)/1000000 + tee_numbriks(k2)/100000000 + tee_numbriks(k1)/10000000000
    
    if yks_paar(k1, k2, k3, k4, k5):
        parim = "Üks paar"
        tugevus = 1 + yks_paar(k1, k2, k3, k4, k5)
    if kaks_paari(k1, k2, k3, k4, k5):
        parim = "Kaks paari"
        tugevus = 2 + kaks_paari(k1, k2, k3, k4, k5)
    if kolmik(k1, k2, k3, k4, k5):
        parim = "Kolmik"
        tugevus = 3 + kolmik(k1, k2, k3, k4, k5)
    if rida(k1, k2, k3, k4, k5):
        parim = "Rida"
        tugevus = 4.0 + rida(k1, k2, k3, k4, k5)/100
    if mast(k1, k2, k3, k4, k5):
        parim = "Mast"
        tugevus = 5.0 + mast(k1, k2, k3, k4, k5)
    if maja(k1, k2, k3, k4, k5):
        parim = "Maja"
        tugevus = 6.0 + maja(k1, k2, k3, k4, k5)
    if nelik(k1, k2, k3, k4, k5):
        parim = "Nelik"
        tugevus = 7.0 + nelik(k1, k2, k3, k4, k5)
    if rida(k1, k2, k3, k4, k5) and mast(k1, k2, k3, k4, k5):
        parim = "Mastirida"
        tugevus = 8.0 + rida(k1, k2, k3, k4, k5)/100
        if kmastirida(k1, k2, k3, k4, k5):
            parim = "Kuninglik mastirida"
            tugevus = 9.0
        
    return (parim, tugevus)