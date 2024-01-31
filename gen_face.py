import datetime
import os
import requests
import cv2
import numpy as np
import rembg
from PIL import Image

OUTPUT_DIR = "output/pfps/"


def generate_person_img(sex, age: int):
    url = "https://this-person-does-not-exist.com"
    time = datetime.datetime.now()
    #convert time to epoch
    time = str(int(time.timestamp()))
    # print(time)
    age=int(round(age.days/365))
    age_range = "all"
    # Switch statement based on the selected age range
    if age >= 12 and age <= 18:
        age_range = "12-18"
    elif age >= 19 and age <= 25:
        age_range = "19-25"
    elif age >= 26 and age <= 35:
        age_range = "26-35"
    elif age >= 35 and age <= 50:
        age_range = "35-50"
    elif age >= 50:
        age_range = "50"
    else:
        age_range = "all"
    print(f"Selected age range: {age_range}")


    response = requests.get(url+"/new?time="+time+"&gender="+sex+"&age="+age_range+"&etnic=white")

    # print(response.status_code)
    # print(response.headers)
    if response.status_code == 200:
        print(response.content)
        data = response.json()
        sub_url = data['src']
        res = requests.get(url+sub_url)
        print(res.status_code)
        if res.status_code == 200:
            with open(OUTPUT_DIR+"image.jpg", "wb") as file:
                file.write(res.content)
                print("Image saved successfully")
        else:
            print("Error saving image")
        img_path = remove_background(OUTPUT_DIR+"image.jpg")
        os.remove(OUTPUT_DIR+"image.jpg")
        return img_path

    

        
        
        

def remove_background(imgpath):
    input_image = Image.open(imgpath)
    input_array = np.array(input_image)
    output_array = rembg.remove(input_array)
    output_image = Image.fromarray(output_array)
    randomimgname = OUTPUT_DIR+"noBG_result_"+str(np.random.randint(999999))+".png"
    output_image.save(randomimgname)
    return randomimgname


def remove_pfp_eatermark(imgpath):
    #TODO: Daniil task
    pass


# Example usage:

# birth_date = datetime.datetime(1940, 10, 1)
# age = datetime.datetime.now() - birth_date
# print(round(age.days/365))

# clean_person_img("image.jpg")
# generate_person_img("female", age)
