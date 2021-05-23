from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import firebase_admin
from selenium.webdriver.chrome.options import Options
from firebase_admin import credentials
from firebase_admin import firestore
import time
import unittest
from twilio.rest import Client
from flask import Flask, render_template, request





class acv(unittest.TestCase):
   
    def sendMessage(self,textMessage):
        account_sid = 'ACfdaf54ef106ea4f48fae9e78588cd69e'
        auth_token = 'fb15a4c98079021641376ca358215f79'
        client = Client(account_sid, auth_token)

        numbers_to_message = ['+19294997605']
        for number in numbers_to_message:
            message = client.messages \
                .create(
            body= textMessage,
            from_= '+13016793819',
            to= number
            ) 

    def initDatabase(self):
        cred = credentials.Certificate("./acvdatabase-firebase-adminsdk-er7dp-d4bdc9c2cf.json")
        firebase_admin.initialize_app(cred)
    
    def addData(self, load):
        data = {
            u'staged': True
        }
        db = firestore.client()
        db.collection(u'loadIds').document(load).set(data)

    def checkData(self, load):
        db = firestore.client()
        doc_ref = db.collection('loadIds').document(load)
        doc = doc_ref.get()
        return True if doc.exists else False
      
    def setUp(self):
        option = webdriver.ChromeOptions()
        GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google-chrome'
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
        option.add_argument('--no-sandbox')
        option.add_argument('headless')
        option.add_argument('--disable-gpu')
        option.add_argument('--disable-dev-shm-usage')
        option.binary_location = GOOGLE_CHROME_PATH
        self.webdriver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,options=option)
        self.webdriver.get("https://transport.acvauctions.com/jobs/available.php")
    
    def close(self):
        self.webdriver.close()

    def login(self):
        time.sleep(2)
        username = self.webdriver.find_element_by_xpath("//input[@name='email']")
        self.webdriver.execute_script("arguments[0].click();", username)
        username.send_keys("righttimenyc@yahoo.com")
        password = self.webdriver.find_element_by_xpath("//input[@name='password']")
        self.webdriver.execute_script("arguments[0].click();", password)
        password.send_keys("Tsikara95#")
        password.send_keys(Keys.ENTER)

    def refreshPage(self):
        self.webdriver.find_element_by_xpath("(//input[@class='btnstyle'])[1]").click()

    def mainPage(self):
        self.webdriver.find_element_by_xpath("(//a[@href='available.php'])[1]").click()
    
    
    def one_way(self,pick_up,dollar,minDollar, dist, condition):
        time.sleep(1)
        acv.mainPage()
        self.webdriver.find_element_by_xpath("//select[@name='p_filter']/option[text()='"+ pick_up + "']").click()
        filter_tab = self.webdriver.find_element_by_xpath("//input[@name='Filter']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        return acv.iterateStatesOneWay(pick_up, dollar, minDollar, dist, condition)

    def two_way(self, pick_up, delivery, dollar, minDollar,  dist, condition):
        time.sleep(1)
        acv.mainPage()
        self.webdriver.find_element_by_xpath("//select[@name='p_filter']/option[text()='"+ pick_up + "']").click()
        self.webdriver.find_element_by_xpath("//select[@name='d_filter']/option[text()='"+ delivery + "']").click()
        filter_tab = self.webdriver.find_element_by_xpath("//input[@name='Filter']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        acv.iterateStatesTwoWay(pick_up, delivery, dollar, minDollar, dist, condition)

   
    def iterateStatesTwoWay(self,pick_up,delivery,dollar,minDollar,  dist, condition):
        if condition == 'Both' or condition == '':
            return acv.iterateStatesTwoWayHelper(pick_up, delivery, dollar, minDollar, dist, condition)

        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist:
                    if info_array[3] == condition and minDollar <= float(pay):  
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        return acv.two_way(pick_up,delivery, dollar,minDollar,  dist, condition)
                        
        acv.refreshPage()
        return acv.iterateStatesTwoWay(pick_up,delivery, dollar, minDollar, dist, condition)
        
                       

    def iterateStatesTwoWayHelper(self,pick_up,delivery, dollar, minDollar,  dist, condition):
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist:
                    if minDollar <= float(pay):
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        return acv.two_way(pick_up,delivery, dollar, minDollar, dist, condition)
                        
        acv.refreshPage()
        return acv.iterateStatesTwoWayHelper(pick_up,delivery, dollar, minDollar,  dist, condition)
                                
        
    def iterateStatesOneWay(self,pick_up, dollar,minDollar,  dist, condition):
        if condition == 'Both' or condition == '':
            return acv.iterateStatesOneWayHelper(pick_up, dollar, minDollar,  dist, condition)
               
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist: 
                    if info_array[3] == condition and minDollar <= float(pay):
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13]
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        return acv.one_way(pick_up,dollar,minDollar, dist,condition)
                        
        acv.refreshPage()
        return acv.iterateStaesOneWay(pick_up, dollar, minDollar, dist, condition)
                            
    def iterateStatesOneWayHelper(self,pick_up, dollar,minDollar,  dist, condition):
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = [] 
            check_box = row.find_elements_by_xpath(".//input[@type='checkbox']")
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):      
                if td.text:
                    info_array.append(td.text)
            if acv.checkData(info_array[0]) == False:
                distance = info_array[12]
                if distance == '---':
                    continue
                pay = info_array[13][1:]
                if float(pay)/float(distance) >= dollar and float(distance) < dist: 
                    if minDollar <= float(pay):
                        self.webdriver.execute_script("arguments[0].click();", check_box[1])
                        select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
                        self.webdriver.execute_script("arguments[0].click();", select_button)
                        message = "Load ID: " + info_array[0] + "\nPick up: " + info_array[4] + " " + info_array[5] + "\n"
                        message += "Delivery: " + info_array[8] + " " + info_array[9] + "\n" + "Pay: " + info_array[13] 
                        acv.sendMessage(message)
                        acv.addData(info_array[0])
                        return acv.one_way(pick_up,dollar,minDollar,  dist, condition)
        acv.refreshPage()
        return acv.iterateStaesOneWayHelper(pick_up, dollar, minDollar, dist, condition)