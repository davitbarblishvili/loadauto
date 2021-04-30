from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class acv(unittest.TestCase):
    """A sample test class to show how page object works"""

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

if __name__ == "__main__":
    acv = acv() 
    acv.setUp()
    acv.login()
    



 



