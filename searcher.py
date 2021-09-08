from re import M
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import yagmail
from multiprocessing import Process


class acv():

    checked_ids = []
    yag = yagmail.SMTP('davidbarblishvili@gmail.com', 'D1a9t9o70101')

    def __init__(self):
        print("acv instantiated")
        self.checked_ids = []
        print("array size is " + str(len(self.checked_ids)))

    def sendMessage(self, textMessage):
        process = Process(target=self.send, args=(textMessage,))
        process.start()
        process.join()

    def send(self, message):
        contents = [message]
        self.yag.send('kataloads@gmail.com', 'New Load Alert', contents)

    def checkData(self, load):
        db = firestore.client()
        doc_ref = db.collection('loadIds').document(load)
        doc = doc_ref.get()
        return True if doc.exists else False

    def check_order_id(self, load):
        db = firestore.client()
        doc_ref = db.collection('checkIds').document(load)
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
        self.webdriver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, options=option)
      # self.webdriver = webdriver.Chrome('./chromedriver',options=option)
        self.webdriver.get(
            "https://transport.acvauctions.com/jobs/available.php")

    def close(self):
        self.webdriver.close()

    def login(self):
        time.sleep(2)
        username = self.webdriver.find_element_by_xpath(
            "//input[@name='email']")
        self.webdriver.execute_script("arguments[0].click();", username)
        username.send_keys("righttimenyc@yahoo.com")
        password = self.webdriver.find_element_by_xpath(
            "//input[@name='password']")
        self.webdriver.execute_script("arguments[0].click();", password)
        password.send_keys("Tsikara95#")
        password.send_keys(Keys.ENTER)

    def refreshPage(self):
        self.webdriver.find_element_by_xpath(
            "(//input[@class='btnstyle'])[3]").click()

    def mainPage(self):
        self.webdriver.find_element_by_xpath(
            "(//a[@href='available.php'])[1]").click()

    def one_way(self, pick_up, dollar, minDollar, dist, condition):
        time.sleep(2)
        self.mainPage()
        self.webdriver.find_element_by_xpath(
            "//select[@name='p_filter']/option[text()='" + pick_up + "']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='sort']/option[text()='Order ID']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='dir']/option[text()='DESC']").click()
        filter_tab = self.webdriver.find_element_by_xpath(
            "//input[@name='Sort']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        return self.iterateStatesOneWay(pick_up, dollar, minDollar, dist, condition)

    def two_way(self, pick_up, delivery, dollar, minDollar,  dist, condition):
        time.sleep(2)
        self.mainPage()
        self.webdriver.find_element_by_xpath(
            "//select[@name='p_filter']/option[text()='" + pick_up + "']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='d_filter']/option[text()='" + delivery + "']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='sort']/option[text()='Order ID']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='dir']/option[text()='DESC']").click()
        filter_tab = self.webdriver.find_element_by_xpath(
            "//input[@name='Sort']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        return self.iterateStatesTwoWay(pick_up, delivery, dollar, minDollar, dist, condition)

    def one_way_no_filter(self, pick_up):
        time.sleep(2)
        self.mainPage()
        self.webdriver.find_element_by_xpath(
            "//select[@name='p_filter']/option[text()='" + pick_up[0] + "']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='sort']/option[text()='Order ID']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='dir']/option[text()='DESC']").click()
        filter_tab = self.webdriver.find_element_by_xpath(
            "//input[@name='Sort']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        return self.iterateStatesOneWayNoFilter(pick_up)

    def two_way_no_filter(self, pick_up, delivery):
        time.sleep(2)
        self.mainPage()
        self.webdriver.find_element_by_xpath(
            "//select[@name='p_filter']/option[text()='" + pick_up[0] + "']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='d_filter']/option[text()='" + delivery[0] + "']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='sort']/option[text()='Order ID']").click()
        self.webdriver.find_element_by_xpath(
            "//select[@name='dir']/option[text()='DESC']").click()
        filter_tab = self.webdriver.find_element_by_xpath(
            "//input[@name='Sort']")
        self.webdriver.execute_script("arguments[0].click();", filter_tab)
        return self.iterateStatesTwoWayNoFilter(pick_up, delivery)

    def iterateStatesTwoWayNoFilter(self, pick_up, delivery):
        while True:
            print("function call two way no filter")
            print("searching " + pick_up[0] + "to " + delivery[0])

            self.webdriver.find_element_by_xpath(
                "//select[@name='perpage']/option[text()='All']").click()
            table = self.webdriver.find_element_by_xpath("//table[2]")
            for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
                order_id = row.find_elements_by_xpath(
                    "(.//td[@class='arial14'])[2]")[0].text
                if(order_id in self.checked_ids):
                    print("already checked")
                    continue
                self.checked_ids.append(order_id)
                info_array = []
                check_box = row.find_elements_by_xpath(
                    ".//input[@type='checkbox']")
                for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                    if td.text:
                        info_array.append(td.text)

                self.webdriver.execute_script(
                    "arguments[0].click();", check_box[1])
                select_button = self.webdriver.find_element_by_xpath(
                    "//input[@name='Submit']")
                self.webdriver.execute_script(
                    "arguments[0].click();", select_button)
                message = "Load ID: " + \
                    info_array[0] + "\nPick up: " + \
                    info_array[5] + " " + info_array[6] + "\n"
                message += "Delivery: " + \
                    info_array[9] + " " + info_array[10] + \
                    "\n" + "Pay: " + info_array[13]
                print("staged " + order_id)
                self.sendMessage(message)
                return self.two_way_no_filter(pick_up, delivery)

            self.refreshPage()

    def iterateStatesTwoWay(self, pick_up, delivery, dollar, minDollar,  dist, condition):
        if condition == 'Both' or condition == '':
            return self.iterateStatesTwoWayHelper(pick_up, delivery, dollar, minDollar, dist, condition)

        while True:
            print("function call two way filter")
            print("searching " + pick_up)
            self.webdriver.find_element_by_xpath(
                "//select[@name='perpage']/option[text()='All']").click()
            table = self.webdriver.find_element_by_xpath("//table[2]")
            for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
                order_id = row.find_elements_by_xpath(
                    "(.//td[@class='arial14'])[2]")[0].text
                if(order_id in self.checked_ids):
                    print("already checked")
                    continue
                self.checked_ids.append(order_id)

                info_array = []
                check_box = row.find_elements_by_xpath(
                    ".//input[@type='checkbox']")
                for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                    if td.text:
                        info_array.append(td.text)
                if self.checkData(info_array[0]) == False:
                    distance = info_array[12]
                    if distance == '---':
                        continue
                    pay = info_array[13][1:]
                    if float(pay)/float(distance) >= dollar and float(distance) < dist:
                        if info_array[3] == condition and minDollar <= float(pay):
                            self.webdriver.execute_script(
                                "arguments[0].click();", check_box[1])
                            select_button = self.webdriver.find_element_by_xpath(
                                "//input[@name='Submit']")
                            self.webdriver.execute_script(
                                "arguments[0].click();", select_button)
                            message = "Load ID: " + \
                                info_array[0] + "\nPick up: " + \
                                info_array[5] + " " + info_array[6] + "\n"
                            message += "Delivery: " + \
                                info_array[9] + " " + info_array[10] + \
                                "\n" + "Pay: " + info_array[13]
                            print("staged " + order_id)
                            self.sendMessage(message)
                            return self.two_way(pick_up, delivery, dollar, minDollar,  dist, condition)

            self.refreshPage()

    def iterateStatesTwoWayHelper(self, pick_up, delivery, dollar, minDollar,  dist, condition):
        while True:
            print("function call two way filter")
            print("searching " + pick_up)
            self.webdriver.find_element_by_xpath(
                "//select[@name='perpage']/option[text()='All']").click()
            table = self.webdriver.find_element_by_xpath("//table[2]")
            for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
                order_id = row.find_elements_by_xpath(
                    "(.//td[@class='arial14'])[2]")[0].text
                if(order_id in self.checked_ids):
                    print("already checked")
                    continue
                self.checked_ids.append(order_id)

                info_array = []
                check_box = row.find_elements_by_xpath(
                    ".//input[@type='checkbox']")
                for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                    if td.text:
                        info_array.append(td.text)
                if self.checkData(info_array[0]) == False:
                    distance = info_array[12]
                    if distance == '---':
                        continue
                    pay = info_array[13][1:]
                    if float(pay)/float(distance) >= dollar and float(distance) < dist:
                        if minDollar <= float(pay):
                            self.webdriver.execute_script(
                                "arguments[0].click();", check_box[1])
                            select_button = self.webdriver.find_element_by_xpath(
                                "//input[@name='Submit']")
                            self.webdriver.execute_script(
                                "arguments[0].click();", select_button)
                            message = "Load ID: " + \
                                info_array[0] + "\nPick up: " + \
                                info_array[5] + " " + info_array[6] + "\n"
                            message += "Delivery: " + \
                                info_array[9] + " " + info_array[10] + \
                                "\n" + "Pay: " + info_array[13]
                            print("staged " + order_id)
                            self.sendMessage(message)
                            return self.two_way(pick_up, delivery, dollar, minDollar, dist, condition)
            self.refreshPage()

    def iterateStatesOneWayNoFilter(self, pick_up):
        while True:

            print("function call one way no filter")
            print("searching " + pick_up[0])

            self.webdriver.find_element_by_xpath(
                "//select[@name='perpage']/option[text()='All']").click()
            table = self.webdriver.find_element_by_xpath("//table[2]")
            for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
                order_id = row.find_elements_by_xpath(
                    "(.//td[@class='arial14'])[2]")[0].text
                if(order_id in self.checked_ids):
                    print("already checked")
                    continue
                self.checked_ids.append(order_id)
                info_array = []
                check_box = row.find_elements_by_xpath(
                    ".//input[@type='checkbox']")
                for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                    if td.text:
                        info_array.append(td.text)

                self.webdriver.execute_script(
                    "arguments[0].click();", check_box[1])
                select_button = self.webdriver.find_element_by_xpath(
                    "//input[@name='Submit']")
                self.webdriver.execute_script(
                    "arguments[0].click();", select_button)
                message = "Load ID: " + \
                    info_array[0] + "\nPick up: " + \
                    info_array[5] + " " + info_array[6] + "\n"
                message += "Delivery: " + \
                    info_array[9] + " " + info_array[10] + \
                    "\n" + "Pay: " + info_array[13]
                print("staged " + order_id)

                self.sendMessage(message)
                return self.one_way_no_filter(pick_up)

            self.refreshPage()

    def iterateStatesOneWay(self, pick_up, dollar, minDollar,  dist, condition):
        if condition == 'Both' or condition == '':
            return self.iterateStatesOneWayHelper(pick_up, dollar, minDollar,  dist, condition)

        while True:

            print("function call one way filter")
            print("searching " + pick_up)
            self.webdriver.find_element_by_xpath(
                "//select[@name='perpage']/option[text()='All']").click()
            table = self.webdriver.find_element_by_xpath("//table[2]")
            for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
                order_id = row.find_elements_by_xpath(
                    "(.//td[@class='arial14'])[2]")[0].text
                if(order_id in self.checked_ids):
                    print("already checked")
                    continue
                self.checked_ids.append(order_id)

                info_array = []
                check_box = row.find_elements_by_xpath(
                    ".//input[@type='checkbox']")
                for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                    if td.text:
                        info_array.append(td.text)
                if self.checkData(info_array[0]) == False:
                    distance = info_array[12]
                    if distance == '---':
                        continue
                    pay = info_array[13][1:]
                    if float(pay)/float(distance) >= dollar and float(distance) < dist:
                        if info_array[3] == condition and minDollar <= float(pay):
                            self.webdriver.execute_script(
                                "arguments[0].click();", check_box[1])
                            select_button = self.webdriver.find_element_by_xpath(
                                "//input[@name='Submit']")
                            self.webdriver.execute_script(
                                "arguments[0].click();", select_button)
                            message = "Load ID: " + \
                                info_array[0] + "\nPick up: " + \
                                info_array[5] + " " + info_array[6] + "\n"
                            message += "Delivery: " + \
                                info_array[9] + " " + info_array[10] + \
                                "\n" + "Pay: " + info_array[13]
                            print("staged " + order_id)
                            self.sendMessage(message)
                            return self.one_way(pick_up, dollar, minDollar, dist, condition)

            self.refreshPage()

    def iterateStatesOneWayHelper(self, pick_up, dollar, minDollar,  dist, condition):
        while True:
            print("function call one way filter")
            print("searching " + pick_up)
            self.webdriver.find_element_by_xpath(
                "//select[@name='perpage']/option[text()='All']").click()
            table = self.webdriver.find_element_by_xpath("//table[2]")
            for row in table.find_elements_by_xpath(".//tr[@class='rowheight']"):
                order_id = row.find_elements_by_xpath(
                    "(.//td[@class='arial14'])[2]")[0].text
                if(order_id in self.checked_ids):
                    print("already checked")
                    continue
                self.checked_ids.append(order_id)

                info_array = []
                check_box = row.find_elements_by_xpath(
                    ".//input[@type='checkbox']")
                for td in row.find_elements_by_xpath(".//td[@class='arial14']"):
                    if td.text:
                        info_array.append(td.text)
                if self.checkData(info_array[0]) == False:
                    distance = info_array[12]
                    if distance == '---':
                        continue
                    pay = info_array[13][1:]
                    if float(pay)/float(distance) >= dollar and float(distance) < dist:
                        if minDollar <= float(pay):
                            self.webdriver.execute_script(
                                "arguments[0].click();", check_box[1])
                            select_button = self.webdriver.find_element_by_xpath(
                                "//input[@name='Submit']")
                            self.webdriver.execute_script(
                                "arguments[0].click();", select_button)
                            message = "Load ID: " + \
                                info_array[0] + "\nPick up: " + \
                                info_array[5] + " " + info_array[6] + "\n"
                            message += "Delivery: " + \
                                info_array[9] + " " + info_array[10] + \
                                "\n" + "Pay: " + info_array[13]
                            print("staged " + order_id)
                            self.sendMessage(message)
                            return self.one_way(pick_up, dollar, minDollar,  dist, condition)
            self.refreshPage()
