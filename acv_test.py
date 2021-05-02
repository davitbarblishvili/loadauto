from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
import json

class acv(unittest.TestCase):

    def setUp(self):
        self.webdriver = webdriver.Chrome(executable_path=r"/Users/davitbarblishvili/Desktop/acv/chromedriver")
        self.webdriver.get("https://transport.acvauctions.com/jobs/available.php")
    
    def close(self):
        self.webdriver.close()

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
    
    def stage_load(self,load):
        acv.setUp()
        acv.login()
        time.sleep(1)
        search_tab = self.webdriver.find_element_by_xpath("//input[@name='search_txt']")
        self.webdriver.execute_script("arguments[0].click();", search_tab)
        search_tab.send_keys(load)

        filter_tab = self.webdriver.find_element_by_xpath("//input[@name='Filter']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)


        time.sleep(1)
        check_button = self.webdriver.find_element_by_xpath("(//input[@type= 'checkbox'])[2]")
        self.webdriver.execute_script("arguments[0].click();", check_button)

        if self.webdriver.find_element_by_xpath("(//input[@type= 'checkbox'])[2]").is_selected():
            select_button = self.webdriver.find_element_by_xpath("//input[@name='Submit']")
            self.webdriver.execute_script("arguments[0].click();", select_button)
        
        acv.close()
        return

        


    def iterateTr(self):
        time.sleep(1)
        acv.refreshPage()
        keys = ["order_id","date","vehicle","inop?","P_address","P_city","P_state","P_zip","Daddress",
        "D_city","D_state","D_zip","Distance","Mayuti"]
        load_dict = {}
        self.webdriver.find_element_by_xpath("//select[@name='perpage']/option[text()='All']").click()
        table = self.webdriver.find_element_by_xpath("//table[2]")
        for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
            info_array = []
            for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                if td.text:
                    info_array.append(td.text)

            if 10000 <= int(info_array[7]) <= 12000 and info_array[3] == "Good":
                        acv.stage_load(info_array[0])

        acv.close()
        return
           
               
if __name__ == "__main__":
    acv = acv() 
    acv.setUp()
    acv.login()
    acv.iterateTr()
   
    



 



