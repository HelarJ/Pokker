import random

kaardid = ['2♣','3♣','4♣','5♣','6♣','7♣','8♣','9♣','10♣','J♣','Q♣','K♣','A♣',
           '2♦','3♦','4♦','5♦','6♦','7♦','8♦','9♦','10♦','J♦','Q♦','K♦','A♦',
           '2♥','3♥','4♥','5♥','6♥','7♥','8♥','9♥','10♥','J♥','Q♥','K♥','A♥',
           '2♠','3♠','4♠','5♠','6♠','7♠','8♠','9♠','10♠','J♠','Q♠','K♠','A♠',]

def käsi():
    uued = kaardid.copy()
    käsi = []
    for i in range(5):
        k1 = random.choice(uued)
        uued.pop(uued.index(k1))
        käsi.append(k1)
    print(len(uued))
    print(len(kaardid))
    
    
    return käsi


    

print(käsi())