import random

def generateSex(year):
    if year >= 1900 and year <= 1999:
        return random.randint(1,2)
    elif year >= 1800 and year <= 1899:
        return random.randint(3,4)
    elif year >= 2000 and year <= 2099:
        return random.randint(5,6)
    else:
        return random.randint(7,8)
def addControlNr(cnp12):
    const = "279146358279"
    cnp12 = str(cnp12)
    nrSum = 0
    for i in range(len(cnp12)):
        nrSum += int(cnp12[i]) * int(const[i])
    controlNr = nrSum % 11
    if controlNr == 10:
        controlNr = 1
    return cnp12 + str(controlNr)

def generateCNP(date, sex, countyIndex):
    randomNr = random.randint(1,999)
    cnp12 = str(sex) + str(date.year)[2:] + str(date.month).zfill(2) + str(date.day).zfill(2) + str(countyIndex).zfill(2) + str(randomNr).zfill(3) 
    cnp = addControlNr(cnp12)
    
    return cnp
    
