from cnp import generateCNP, generateSex
from fakedraw import printID

import json
from faker import Faker
fake = Faker('ro_RO')

from user_id import UserID


def generateUsersJSON(nr):
    users = []
    for i in range(nr):
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

        users.insert(i, UserID(first_name, last_name, sex, cnp, birthdate, birthplace, county_abbr, residence_address, spclep))
        # print(users[i])
        print("Generating ID: ",i+1,"/",nr)
    return users

def getCountiObj(abbr):
    f = open("src/counties.json")
    counties = json.load(f)
    f.close()
    for county in counties:
        if county["abbr"] == abbr:
            return county
    return None


def main():
    #read a number
    n = int(input("Numarul de Fake ID-s: "))
    users = generateUsersJSON(n)
    # lopp users 
    for user in users:
        printID(user)

    #createa a file named users.json and write the users list to it
    with open('output/users.json', 'w') as outfile:
        json.dump(users, outfile, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    print("DONE: users.json created")
    #
    

if __name__ == "__main__":
    main()

