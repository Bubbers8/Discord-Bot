
import time
from random import seed
from random import randint



def Santa(list):
    assign = list.copy()
    seed(int(time.time()))
    toReturn  = [[]]
    for name in list:
        num = randint(0,len(assign)-1)
        while(assign[num] == name):#if you randomly selected the same person twice, select again
            num = randint(0,len(assign)-1)
        toReturn.append([name, assign[num]])
        del assign[num]
