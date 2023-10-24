from faker import Faker
fake = Faker('ro_RO')
import json

class UserID:
    def __init__(self, first_name, last_name, sex, cnp, birth_date, birth_place,county_abbr, residence_address, spclep):
        self.first_name = first_name.upper()
        self.last_name = last_name.upper()
        if int(sex) % 2 == 0: 
            self.sex ="F"
        else:
            self.sex = "M" 
        self.seria = fake.random_uppercase_letter() + fake.random_uppercase_letter()
        self.seria_nr = str(fake.random_number(digits=6))
        self.short_code = str(fake.random_number(digits=2)) + fake.random_uppercase_letter() +str(fake.random_number(digits=1))+ fake.random_uppercase_letter()
        self.dig3 = str(fake.random_number(digits=3)) 
        self.cnp = int(cnp)
        self.county_abbr = county_abbr
        self.birth_date = birth_date.strftime("%d.%m.%y")
        self.birth_place = birth_place
        self.residence_address = residence_address
        self.spclep = "SPCLEP " + spclep 
        self.validity_interval = self.genValidityInterval()
        scan_code1 = "IDROU"+self.first_name+"<<"+self.last_name
        scan_code1 = scan_code1 + '<'*(36-len(scan_code1))
        scan_code2 = self.seria+self.seria_nr+"<"+str(fake.random_number(digits=1))+"ROU"+str(self.cnp)[1:6]+str(fake.random_number(digits=1))+self.sex
        scan_code2 = scan_code2 + self.validity_interval[17:18]+str(self.cnp)[3:6]+str(fake.random_number(digits=9))

        self.footer_scan_code = scan_code1+'\n'+scan_code2
        del scan_code1, scan_code2
    def genValidityInterval(self):
        date = fake.date_time_between(start_date='-6y', end_date='now')
        return date.strftime("%d.%m.%y") + "-" + self.birth_date[0:6] + str(int(date.strftime("%Y"))+7)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    def __str__(self):
        return json.dumps(self.__dict__)
