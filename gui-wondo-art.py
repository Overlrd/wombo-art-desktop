#### import gui utils
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import customtkinter as ctk
from PIL import ImageTk, Image
#Import third part modules
import os
import threading
import time
import requests
from io import BytesIO
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



class App(tk.Tk):
  def __init__(self):
    super().__init__()

    # configure the root window
    self.title('Wombo Art Gui')
    self.geometry('410x700')
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme("blue")
    #test vars
    self.status_text = 'STATUS : Not active'
    self.img_path = '/home/s8doo/Overlrd/wombo_art_app/wombo-ai-scraper-main/0FlowersHD.png'
    self.loading_path = '/home/s8doo/Overlrd/wombo_art_app/wombo-ai-scraper-main/0SunHD.png'
    self.default_dir = 'wombo_ai'

    #########################
    #SETUP VIRTUAL DISPLAY
    self.display = Display(visible=0, size=(1200,900))
    self.display.start()
    # DRIVER PATH AND XPATHS
    self.CHROME_DRIVER_PATH = "chromedriver"
    self.XPATH_TEXT_FIELD = '//*[@id="blur-overlay"]/div/div/div[1]/div[1]/div[1]/div[1]/div[1]/input'
    self.XPATH_IMG_TYPE = '//img[@class="Thumbnail__StyledThumbnail-sc-p7nt3c-0 hxvLKC"'
    self.XPATH_BTN_GENERATE = '//*[@id="blur-overlay"]/div/div/div/div[2]/button'
    self.XPATH_RESULT_IMG = '//img[@class="ArtCard__CardImage-sc-67t09v-2 dOXnUm"]'
    self.driverThreads = []
    self.CATEGORIES = []

    # label
    prompt_label   = ctk.CTkLabel(self, height=15, width=120, text_font=('Arial', 15), text_color='black')
    prompt_label.place(x=1, y =1)
    prompt_label.configure(text='PROMPT')

    self.Prompt_input = ctk.CTkEntry(self, height = 45,width = 180,placeholder_text="Enter prompt")
    self.Prompt_input.place(x=10, y=35)

    self.x = ["Etching","Baroque","Mystical","Festive","Dark Fantasy","Psychic","Pastel","HD","Vibrant","Fantasy Art","Steampunk","Ukiyoe","Synthwave","No Style"]

    ###combo list & label
    Combo_label = ctk.CTkLabel(self, height=15, width=120, text_font=('Arial', 15), text_color='black')
    Combo_label.place(x=200, y =1)
    Combo_label.configure(text='SELECT STYLE')
    self.Combo_list = ctk.CTkComboBox(self, values= self.x, height = 45,width = 180, text_font=('Arial', 15))
    self.Combo_list.place(x=200, y=35)
    self.Combo_list.set(self.x[0])


    self.Status_label = ctk.CTkLabel(self, height=15, width=80, text_font=('Arial', 10), text_color='black')
    self.Status_label.place(x=1, y =120)
    self.Status_label.configure(text=self.status_text)

    ###############
    #####  Image Frame
    ################
    ## open image
    self.img = Image.open(self.img_path)
    self.img = self.img.resize((400, 500), Image.ANTIALIAS)
    self.img = ImageTk.PhotoImage(self.img)
    ## configure frame
    self.frame = ctk.CTkFrame(self,width=400,height=500,corner_radius=10)
    self.frame.place(x=1, y = 150)
    self.lmain = tk.Label(self.frame) 
    self.lmain.place(x=0, y=0) 
    self.lmain.configure(image=self.img)
    self.lmain.image = self.img

    button = ctk.CTkButton(self,width=100,height=45,border_width=0,corner_radius=8,text="Generate", command=self.thread_and_start)
    button.place(x=300, y=650)


    ##############
    ##### Progress Bar
    ##############
    self.progressbar = ctk.CTkProgressBar(master=self,  width=370, height=30)
    self.progressbar.place(x=10, y=80)
    self.progressbar.configure()



  def show(self, path):
    succes_status = f' SUCCES :Image saved to {path}'
    text = str(self.Prompt_input.get())
    categ = str(self.Combo_list.get())
    print(f'prompt is {text} and categ is {categ} ')
    self.Status_label.configure(text=succes_status)
    self.img = Image.open(path)
    self.img = self.img.resize((400, 500), Image.ANTIALIAS)
    self.img = ImageTk.PhotoImage(self.img)
    ## configure frame
    self.frame = ctk.CTkFrame(self,width=400,height=500,corner_radius=10)
    self.frame.place(x=1, y = 150)
    self.lmain = tk.Label(self.frame) 
    self.lmain.place(x=0, y=0) 
    self.lmain.configure(image=self.img)
    self.lmain.image = self.img

    #self.progressbar.stop()
  def downloadImage(self, imgType,inputText,iteration):
    #Add headless option
    browserOptions = Options()
    #browserOptions.add_argument("--headless")

    #Create driver
    driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER_PATH,options=browserOptions)
    driver.get("https://app.wombo.art/")

    #Type the text
    textfield = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH ,self.XPATH_TEXT_FIELD)))
    textfield.send_keys(inputText)

    #Select the img type to generate
    imgTypeBox = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,f'{self.XPATH_IMG_TYPE} and @alt="{imgType}"]')))
    imgTypeBox.click()
    #Checking img_type
    print(imgType)


    time.sleep(1)

    #Click on the "Create" button
    btnGenerate = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH,self.XPATH_BTN_GENERATE)))
    btnGenerate.click()

    #Get the generated image
    resultImg = WebDriverWait(driver,100).until(EC.element_to_be_clickable((By.XPATH,self.XPATH_RESULT_IMG)))
    resultImgSrc = resultImg.get_attribute('src')

    time.sleep(1)

    #Get the image from URL
    im = Image.open(BytesIO(requests.get(resultImgSrc).content))
    #Crop the image to remove the "Watermark"
    im = im.crop((81, 232, 999, 1756))
    #Save image localy
    self.local_img_path = f"{self.default_dir}/{str(iteration)+inputText+imgType}.png"
    im.save(self.local_img_path)
    #Close virtual disply
    #display.stop() 

  def thread_and_start(self):
    def start(self):
        print('should start here')
        running_status = f' STATUS : Running ...'
        self.Status_label.configure(text=running_status)
        self.progressbar = ctk.CTkProgressBar(master=self,  width=370, height=30)
        self.progressbar.place(x=10, y=80)
        self.progressbar.configure()
        self.progressbar.start()
    def thread(self):
    
        self.inputText = str(self.Prompt_input.get())
        self.inputText = "".join([x.capitalize() for x in self.inputText.split(" ")])
        self.iterations = 1
        #CATEGORIES = str(self.Combo_list.get())
        categ = str(self.Combo_list.get())
        self.CATEGORIES.append(categ)
        #Create directory
        if not os.path.exists(self.default_dir):
            os.mkdir(self.default_dir)

        for i in self.CATEGORIES:
            for j in range(self.iterations):
                #Add thread to the list
                self.driverThreads.append(threading.Thread(target=self.downloadImage, kwargs={'imgType':i.replace(" ",""),'inputText':self.inputText,'iteration':j}))

        #Start all threads
        for i in self.driverThreads:
            try:
                self.imgType = i._kwargs.get("imgType")
                self.iteration = i._kwargs.get("iteration")+1
                print(f"Starting Thread, Type {self.imgType}, Iteration {self.iteration}")
                i.start()
            except:
                pass

        #Wait for the end of all threads
        for i in self.driverThreads:
            i.join()
            print('here')
        self.show(self.local_img_path)
        self.CATEGORIES.clear()
        self.progressbar.stop()
    start(self)
    thread(self)






if __name__ == "__main__":
  app = App()
  app.mainloop()