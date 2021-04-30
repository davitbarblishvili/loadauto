from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
import json

class acv(unittest.TestCase):
    url = ""

    def setUp(self):
        self.webdriver = webdriver.Chrome(executable_path=r"/Users/davitbarblishvili/Desktop/acv/chromedriver")
        self.webdriver.get("https://transport.acvauctions.com/jobs/available.php")

    def login(self):
               
        time.sleep(3)
        username = self.webdriver.find_element_by_xpath("//input[@name='email']")
        self.webdriver.execute_script("arguments[0].click();", username)
        username.send_keys("righttimenyc@yahoo.com")

        password = self.webdriver.find_element_by_xpath("//input[@name='password']")
        self.webdriver.execute_script("arguments[0].click();", password)
        password.send_keys("Tsikara95#")
        password.send_keys(Keys.ENTER)

       
    def tearDown(self):
        self.webdriver.close()
        
    def getUrl(self):
        time.sleep(2)
        self.webdriver.find_element_by_xpath("//input[@name='Submit3']").click()
    
    def refreshPage(self):
        time.sleep(1)
        self.webdriver.find_element_by_xpath("//div[@class='arial14']/a[1]").click()

    def iterateTr(self):
        time.sleep(1)
        acv.refreshPage()
        keys = ["order_id","date","vehicle","inop?","P_address","P_city","P_state","P_zip","Daddress",
        "D_city","D_state","D_zip","Distance","Mayuti"]
        load_dict = {}
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        test = 0
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            idx = 0
            temp_dict = {}
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                if td.text and idx >= 1:
                    temp_dict[keys[idx]] = td.text
                    idx += 1
                   
                if td.text and idx == 0:
                    load_dict[td.text] = temp_dict
                    idx += 1
                

        with open('loads.json', 'w') as fp:
            json.dump(load_dict, fp)




if __name__ == "__main__":
    acv = acv() 
    acv.setUp()
    acv.login()
    acv.iterateTr()
   
    



 



