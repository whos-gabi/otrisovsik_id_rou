import os
from PIL import Image, ImageFont, ImageDraw
import datetime
from user_id import UserID
from gen_face import generate_person_img

CHAR_HEIGHT = 90

def getPersonImage(person: UserID):
    date = datetime.datetime.strptime(person.birth_date, '%d.%m.%y')
    age = datetime.datetime.now() - date 
    sex = person.sex
    if sex == "M":
        sex = "male"
    else:
        sex = "female"
    return generate_person_img(sex, age) 
    # return "src/face/danut.png" 

def draw_text_with_spacing(image: ImageDraw, text, coordinates, letter_spacing=-20, font: ImageFont = None, text_color="black", line_spacing=5):
    x, y = coordinates
    for char in text:
        
        if char == '\n':
            y = y+line_spacing+CHAR_HEIGHT
            x = coordinates[0]
        else:
            char_width = font.getlength(char)
            image.text((x, y), char, fill=text_color, font=font)
            x += char_width + letter_spacing

def printID(person: UserID):
    try:
        pfp_path = getPersonImage(person)
        canvas = Image.open("src/canvasID_blank.png")
        pfp = Image.open(pfp_path)
        pfpWidth, pfpHeight = pfp.size
        pfp = pfp.resize((830+15,1040+20))
        canvas.paste(pfp, (284, 376), mask=pfp)
        
        draw = ImageDraw.Draw(canvas)
        ocrbmt = ImageFont.truetype("Fonts/OCRBPro.ttf", CHAR_HEIGHT)
        
        # fontBold = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 38)
        draw_text_with_spacing(draw, person.last_name, (1140, 702), font=ocrbmt)
        draw_text_with_spacing(draw, person.first_name, (1140, 858), font=ocrbmt)
        draw_text_with_spacing(draw, "Română / ROU",(1140,1020), font=ocrbmt)
        draw_text_with_spacing(draw, person.birth_place, (1140, 1175), font=ocrbmt)
        draw_text_with_spacing(draw, person.residence_address, (1140, 1340), font=ocrbmt)
        draw_text_with_spacing(draw, person.spclep, (1140, 1605), font=ocrbmt)
        draw_text_with_spacing(draw, person.validity_interval, (2360, 1605), font=ocrbmt)
        draw_text_with_spacing(draw, person.dig3, (400, 1530), font=ocrbmt)
        draw_text_with_spacing(draw, person.county_abbr, (915, 1530), font=ocrbmt)

        #draw cnp
        draw_text_with_spacing(draw, str(person.cnp)[0], (1290, 525), font=ocrbmt, text_color=(153,53,54))
        draw_text_with_spacing(draw, str(person.cnp)[1:7], (1335, 525), font=ocrbmt, text_color=(17,44,86))
        draw_text_with_spacing(draw, str(person.cnp)[7:13], (1610, 525), font=ocrbmt, text_color=(153,53,54))

        draw_text_with_spacing(draw, person.seria, (2015, 450), font=ocrbmt)
        draw_text_with_spacing(draw, person.seria_nr, (2278, 450), font=ocrbmt)
        draw_text_with_spacing(draw, person.sex, (2940, 1020), font=ocrbmt)

        pfp = pfp.resize((412,550))
        pfp2=pfp.copy()
        pfp2 = pfp.convert("L")
        pfp2.putalpha(60)
        pfp.paste(pfp2, pfp)
        del pfp2
        canvas.paste(pfp, (2800, 400), mask=pfp)


        draw_text_with_spacing(draw, person.short_code, (2573, 560), font=ocrbmt)
        footer_scan_code = person.footer_scan_code.split('\n')
        draw_text_with_spacing(draw, footer_scan_code[0], (425, 1770), font=ocrbmt, letter_spacing=10)
        draw_text_with_spacing(draw, footer_scan_code[1], (425, 1955), font=ocrbmt, letter_spacing=18)


        print("Saving: "+str(person.cnp)+"_ID.png")
        canvas.save("output/"+str(person.cnp)+"_ID.png")
        os.remove(pfp_path)
    except Exception as e:
        print("Error: "+str(e))
        return None
    finally:
        return "output/"+str(person.cnp)+"_ID.png"        
