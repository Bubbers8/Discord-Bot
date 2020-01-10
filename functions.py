
import time
from random import seed
from random import randint



def Santa(list):
    assign = list.copy()
    seed(int(time.time()))
    toReturn  = [[]]
    count = len(list)
    for name in list:
        if(count != 2):
            num = randint(0,len(assign)-1)
            while(assign[num] == name):#if you randomly selected the same person twice, select again
                num = randint(0,len(assign)-1)
            toReturn.append([name, assign[num]])
            del assign[num]
            count = count - 1
        elif(count == 2):
            if(assign[0] != name & list[len(list)-1] != assign[1]):
                toReturn.append([name,assign[0]])
                del assign[0]
            else:
                toReturn.append([name,assign[1]])
                del assign[1]
        else:
            toReturn.append([name,assign[0]])
    return toReturn
