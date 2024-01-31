import datetime
from cnp import generateCNP, generateSex, readSexOption
from fakedraw import printID

import json
from faker import Faker
fake = Faker('ro_RO')

from user_id import UserID
import asyncio


async def generateUsersJSON(nr):
    users = []
    for i in range(nr):
        usr  = await generateUser()
        users.insert(i, usr)
        print("Generating ID: ",i+1,"/",nr)
    return users

async def generateUser():
    birthdate = fake.date_time_between(start_date='-30y', end_date='-14y')
    sex=generateSex(birthdate.year)
    if(sex%2==0):
        first_name = fake.first_name_female()
    else:
        first_name = fake.first_name_male()
    last_name = fake.last_name()
    birthplace = fake.city()
    spclep = fake.city() 
    #cnp
    county_abbr=fake.state_abbr()
    #fake a city from the county
    residence_address = "Jud."+county_abbr+" "+spclep+'\n'+fake.street_address().replace(". ", ".")
    countiID = getCountiObj(county_abbr)["id"]
    cnp = generateCNP(birthdate, sex, countiID)
    print("Generated user with cnp: "+cnp)
    return UserID(first_name, last_name, sex, cnp, birthdate, birthplace, county_abbr, residence_address, spclep)



def getCountiObj(abbr):
    f = open("src/counties.json")
    counties = json.load(f)
    f.close()
    for county in counties:
        if county["abbr"] == abbr:
            return county
    return None


# def generateID():
#     return "output/"+str(printID(generateUser()))+".png"

def customID():
    print("Custom ID\n Enter the following information to generate a custom ID:\n")
    fullname = input("Nume Prenume: ")
    first_name = fullname.split(" ")[0]
    last_name = fullname.split(" ")[1]
    
    sex = readSexOption(digits = True)
    # sex = "5"
    
    birthdate = fake.date_time_between(start_date='-24y', end_date='-16y')
    birthplace = fake.city()
    spclep = fake.city()
    county_abbr=fake.state_abbr()
    residence_address = "Jud."+county_abbr+" "+spclep+'\n'+fake.street_address().replace(". ", ".")
    countiID = getCountiObj(county_abbr)["id"]

    cnp  = generateCNP(birthdate, sex, countiID)


    printID(UserID(first_name, last_name, sex, cnp, birthdate, birthplace, county_abbr, residence_address, spclep))




async def randomID():
     #read a number
    n = int(input("Numarul de Fake ID-s: "))
    users = await generateUsersJSON(n)
    # lopp users 
    for user in users:
        printID(user)

    #createa a file named users.json and write the users list to it
    with open('output/users.json', 'w') as outfile:
        json.dump(users, outfile, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    print("DONE: users.json created")


def readStartSettings():
    global genType
    genType = input("Generate custom photo (1), generate random (2): ")
    try:
        genType = int(genType)
        if genType != 1 and genType != 2:
            raise ValueError
        if isinstance(genType, str):
            raise TypeError

    except ValueError:
        print("Invalid input. Please enter 1 or 2.")
        readStartSettings()   
    except TypeError:
        print("Invalid input. Please enter A NUMBER 1 or 2.")
        readStartSettings()     


global genType 
async def main():
    readStartSettings()     

    if genType == 1:
        customID()
    elif genType == 2:
        await randomID()

if __name__ == "__main__":
    asyncio.run(main())

