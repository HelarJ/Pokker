def tee_numbriks(kaart):
    if kaart[:-1] == "J":
        return "11"
    elif kaart[:-1] == "Q":
        return "12"
    elif kaart[:-1] == "K":
        return 13
    elif kaart[:-1] == "A":
        return 14
    else:
        return kaart[:-1]
    
def yks_paar(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] or k1[:-1] in k3[:-1] or k1[:-1] in k4[:-1] or k1[:-1] in k5[:-1]:
        return True
    elif k2[:-1] in k3[:-1] or k2[:-1] in k4[:-1] or k2[:-1] in k5[:-1]:
        return True
    elif k3[:-1] in k4[:-1] or k3[:-1] in k5[:-1]:
        return True
    elif k4[:-1] in k5[:-1]:
        return True
    
def kaks_paari(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k3[:-1] in k4[:-1] or k1[:-1] in k2[:-1] and k4[:-1] in k5[:-1]:
        return True
    if k2[:-1] in k3[:-1] and k4[:-1] in k5[:-1]:
        return True
    
def kolmik(k1, k2, k3, k4, k5):
    if k1[:-1] in k2[:-1] and k1[:-1] in k3[:-1]:
        return True
    if k2[:-1] in k3[:-1] and k2[:-1] in k4[:-1]:
        return True
    if k3[:-1] in k4[:-1] and k3[:-1] in k5[:-1]:
        return True
    
def rida(k1, k2, k3, k4, k5):
    k1 = int(tee_numbriks(k1))
    k2 = int(tee_numbriks(k2))
    k3 = int(tee_numbriks(k3))
    k4 = int(tee_numbriks(k4))
    k5 = int(tee_numbriks(k5))
    if k1 == k2-1 == k3-2 == k4-3 == k5-4:
        return True
    if k5 == 14 and k1 == 2 and k2 == 3 and k3 == 4 and k4 == 5:
        return True
        
def mast(k1, k2, k3, k4, k5):
    if k1[-1] == k2[-1] == k3[-1] == k4[-1] == k5[-1]:
        return True
    
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
    

def käsi(k1, k2, k3, k4, k5):
    parim = "Kõrge kaart"
    if yks_paar(k1, k2, k3, k4, k5):
        parim = "Üks paar"
    if kaks_paari(k1, k2, k3, k4, k5):
        parim = "Kaks paari"
    if kolmik(k1, k2, k3, k4, k5):
        parim = "Kolmik"
    if rida(k1, k2, k3, k4, k5):
        parim = "Rida"
    if mast(k1, k2, k3, k4, k5):
        parim = "Mast"
    if maja(k1, k2, k3, k4, k5):
        parim = "Maja"
    if nelik(k1, k2, k3, k4, k5):
        parim = "Nelik"
    if rida(k1, k2, k3, k4, k5) and mast(k1, k2, k3, k4, k5):
        parim = "Mastirida"
        if kmastirida(k1, k2, k3, k4, k5):
            parim = "Kuninglik mastirida"
        
        
    print(parim)
    return(parim)



#print(tee_numbriks('K♥'))
#käsi("2♣", "3♦", "4♣", "5♣", "A♦")