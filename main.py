import requests
from flask import Flask, render_template, request, jsonify
#from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as soup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
import urllib.request
import os
import time
IMG_FOLDER =os.path.join('static', 'images')

app=Flask(__name__)
app.config['IMG_FOLDER']=IMG_FOLDER
path = "C:\Program Files (x86)\chromedriver.exe"

class ImageScrapper:
    def __init__(self):
        self.imageList=[]
    def get_image_list(self, base_URL=None, searchString=None,imageCount=None):
        try:

            driver = webdriver.Chrome(path)
            search_url = f"{base_URL}/search?q={searchString}&safe=active&rlz=1C1CHBD_enIN802IN802&sxsrf=ALeKk00VseOsB3TQfPJKpLpyz2Y27AeP-A:1603546789380&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiarIumrc3sAhVd4XMBHaNXDJUQ_AUoA3oECAwQBQ&biw=1366&bih=600"
            # print(search_url)
            driver.get(search_url)
            #driver.maximize_window()
           # scheight = .1
           # while scheight < 9.9:
            #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/%s);" % scheight)
              #  scheight += .01
             #   time.sleep(0.2)
            page = driver.page_source
            google_html = soup(page, "html.parser")
            image_loads = google_html.find_all("img", class_="rg_i Q4LuWd",limit=imageCount)
            return image_loads
        except:
            pass

    def save_as_image(self, image_loads):

        CleanCache(directory=app.config['IMG_FOLDER'])
        for image in image_loads:
            pdt_src = image.get("src")

            if  pdt_src != None :

                try :

                    img_name = random.randrange(1, 500)
                    full_name = str(img_name) + '.jpg'
                    self.imageList.append(full_name)
                    urllib.request.urlretrieve(pdt_src,os.path.join(app.config['IMG_FOLDER'], full_name))

                    print(f"SUccess-saved {full_name}in folder {IMG_FOLDER}")
                except :
                    pass
            else :
                pdt_src= image.get("data-src")
                try:

                    img_name = random.randrange(1, 500)
                    full_name = str(img_name) + '.jpg'
                    self.imageList.append(full_name)
                    urllib.request.urlretrieve(pdt_src, os.path.join(app.config['IMG_FOLDER'], full_name))

                    print(f"SUccess-saved {full_name}in folder {IMG_FOLDER}")
                except:
                    pass

    def get_showimage_list(self):
        return self.imageList
class CleanCache:
	'''
	this class is responsible to clear any residual csv and image files
	present due to the past searches made.
	'''
	def __init__(self, directory=None):
		self.clean_path = directory
		# only proceed if directory is not empty
		if os.listdir(self.clean_path) != list():
			# iterate over the files and remove each file
			files = os.listdir(self.clean_path)
			for fileName in files:
				print(fileName)
				os.remove(os.path.join(self.clean_path,fileName))
		print("cleaned!")

@app.route("/",methods=['GET'])
def home():
    return render_template("index.html")
@app.route("/result",methods=['GET','POST'])
def result():
    if request.method == 'POST' :
        base_URL = "https://www.google.com"
        searchString = request.form['searchString']
        imageCount= int(request.form['count'])
        scrapper = ImageScrapper()
        image_loads = scrapper.get_image_list(base_URL, searchString,imageCount)
        scrapper.save_as_image(image_loads)
        image_list=scrapper.get_showimage_list()
        return render_template("result.html",images=image_list)



if __name__ == "__main__" :
    app.run(debug=True)
