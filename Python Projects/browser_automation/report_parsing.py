"""
July, 2023
This was my first attempt ever in browser automation. Our team had hundreds of reports inside a SAP BusinessObjects application that
could be run in a browser. We wanted to get certain data from the reports that could not be obtained from the backend, nor even by
copy/paste. The idea for this program was to navigate through the list of reports, extracting the data from the HTML of the iframe.
I was able to get the program to successfully extract the data from a single report, but didn't have enough time to work in the 
navigation before the project was scaled down and closed. The code is quite rough and manual, but taught me a lot about Selenium,
automation, algorithms, and object-oriented programming.
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import time
import fileutils 
import os 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import pyautogui
import subprocess 
import sys

class Query():
    def __init__(self,name):
        self._name = name
        self._folders = []
        self._robjects = []
    def add_folder(self, folder):
        self._folders.append(folder)
    def add_robject(self, robject):
        self._robjects.append(robject)

class Folder():
    def __init__(self,name):
        self._name = name
        self._subfolders = []
        self._robjects = []
    def add_subfolder(self, subfolder):
        self._subfolders.append(subfolder)
    def add_robject(self, robject):
        self._robjects.append(robject)

class Driver():
    # def __init__(self):
    # # connect to the existing browser:
    #     self._chrome_options = Options()
    #     self._chrome_options.add_experimental_option("debuggerAddress", "localhost:4920")
    #     self._driver = webdriver.Chrome(options=self._chrome_options)

    def login(self):
        # start a browser in debugging mode:
        subprocess.Popen('chrome.exe --remote-debugging-port=4200 --user-data-dir="C:\selenum\ChromeProfile"')
        time.sleep(3)
        self._chrome_options = Options()
        self._chrome_options.add_experimental_option("debuggerAddress", "localhost:4200")
        self._driver = webdriver.Chrome(options=self._chrome_options)
        # webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        # driver = webdriver.Chrome()
        self._driver.implicitly_wait(10)
        url = '' # removed url for privacy
        self._driver.get(url)
        time.sleep(5)
        username = ''
        self._driver.find_element(By.ID,'okta-signin-username').send_keys(username)
        time.sleep(1)
        self._driver.find_element(By.ID,'okta-signin-submit').click()
        time.sleep(2)
        self._driver.find_element(By.XPATH,'/html/body/div[4]/main/div[2]/div/div/form/div[1]/div[2]/div/div[2]/span/input').send_keys("Rr*4DomUduj@hLD")
        time.sleep(1)
        self._driver.find_element(By.XPATH,'/html/body/div[4]/main/div[2]/div/div/form/div[2]/input').click()
        time.sleep(1)
        self._driver.find_element(By.XPATH,'/html/body/div[4]/main/div[2]/div/div/form[1]/div[2]/input').click()
        self._driver.quit

    def connect(self):
        self._chrome_options = Options()
        self._chrome_options.add_experimental_option("debuggerAddress", "localhost:4200")
        self._driver = webdriver.Chrome(options=self._chrome_options)
        self._driver.implicitly_wait(10)
        self._driver.switch_to.frame('servletBridgeIframe')

    def nav_to_report(self):
        # click "Folders"
        self._driver.find_element(By.ID,'Folders').click()
        # click "Public Folders" NOTE: the ID and XPATH was changing with every reload
        self._driver.find_element(By.XPATH,'//li[@data-ttc-id="treeItem-Public Folders"]').click()

        first_folder = '""'
        self._driver.find_element(By.XPATH,'//*[@title={}]'.format(first_folder)).click()

        second_folder = '""'
        self._driver.find_element(By.XPATH,'//*[@title={}]'.format(second_folder)).click()

        # TODO: figure out how to make the scrolling function reusable to look in other folders
        #scroll and right click on given report:
        action = ActionChains(self._driver)
        report1 = '""'

        while True:
            try:
                action.context_click(self._driver.find_element(By.XPATH,'//*[@title={}]'.format(report1))).perform()
                break
            except:
                scroll_bar = self._driver.find_element(By.XPATH,'//*[@class="sapUiTableVSb"]')
                for x in range(7):
                    scroll_bar.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.25)
                time.sleep(1)

        # TODO: possibly find a better way to click "view" in pop up window. It has a hard time switching between pyautogui and driver.
        # hit enter to view report (ONLY WORKS IF CHROME WINDOW IS FOCUS)
        time.sleep(1)
        pyautogui.press('enter')

    def open_report(self):
        # switch to design mode: 
        self._driver.find_element(By.XPATH,'(//div[@class="sapMSBInner"]//bdi[.="Reading"])[last()]').click()

        click_count = 0
        while True:
            try: 
                self._driver.find_element(By.XPATH,'(//section[@class="sapMPageEnableScrolling sapUiScrollDelegate"]//div[@class="sapMList wingTestDictionaryTree sapWiseAvailableObjects"])[last()]//li[@data-selectable="false"]/span[@aria-label="Expand Node"]').click()
                click_count += 1
            except:
                if click_count == 0:
                    exit = input("could not locate any folders. exit? (y/n)")
                    if exit == 'y':
                        sys.exit()
                    else:
                        break
                else:
                    print("opened {} folders".format(click_count))
                break
                
    def retrieve(self):
        items_xpath = '(//section[@class="sapMPageEnableScrolling sapUiScrollDelegate"]//div[@class="sapMList wingTestDictionaryTree sapWiseAvailableObjects"])[last()]//li'
        text_extension = '//span[@class="sapMTextMaxLine sapMTextLineClamp"]'
        items = self._driver.find_elements(By.XPATH,items_xpath)
        items_text_loc = self._driver.find_elements(By.XPATH,items_xpath + text_extension)
        items_text = [loc.text for loc in items_text_loc]

        self._queries = []
        while len(items) > 0:
            item = items.pop(0)
            level = int(item.get_attribute("aria-level"))
            selectable = item.get_attribute("data-selectable")
            item_text = items_text.pop(0)

            if level == 1: # item is a query
                if item_text in ('Merged Dimensions', 'Variables'):
                    break
                else:
                    current_query = Query(item_text)
                    self._queries.append(current_query)
                    folder_level = 0
                    strange_flag = 0
            
            elif selectable == 'false': # item is a folder
                if level == 2:
                    folder1 = Folder(item_text)
                    current_query.add_folder(folder1)
                    folder_level = 1
                elif level == 3:
                    folder2 = Folder(item_text)
                    folder1.add_subfolder(folder2)
                    folder_level = 2
                elif level == 4:
                    folder3 = Folder(item_text)
                    folder2.add_subfolder(folder3)
                    folder_level = 3
                else:
                    print('MORE THAN 3 FOLDERS!!!')
                    break

            else: # item is a robject
                if folder_level == 0:
                    current_query.add_robject(item_text)
                    if strange_flag == 0:
                        print("Strange Data Source: ", current_query._name)
                        strange_flag = 1
                if folder_level == 1:
                    folder1.add_robject(item_text)
                elif folder_level == 2:
                    folder2.add_robject(item_text)
                elif folder_level == 3:
                    folder3.add_robject(item_text)
        
        return self._queries

    # NOTE: has not been updated to print with a third folder layer
    def to_console(self):
        for q in self._queries:
            print("   query: ", q._name)
            for f in q._folders:
                print("      folder: ", f._name)
                for fr in f._robjects:
                    print("            folder robject: ", fr)
                for s in f._subfolders:
                    print("         subfolder: ", s._name)
                    for sr in s._robjects:
                        print("            subfolder robject: ", sr)

    def to_csv(self,report):
        with open('C:/ReportAutomation/results.csv', 'a') as fil:
            # fil.write('Report,Query,Type,Universe,Parent Folder 2,Parent Folder 1,Base Folder,Report Object\n')
            for q in self._queries:
                intro = report + "," + q._name + ",Return Object"
                for qr in q._robjects:
                    fil.write(intro + ",,,,," + qr + '\n')
                for f1 in q._folders:
                    for fr1 in f1._robjects:
                        fil.write(intro + ",,,," + f1._name + "," + fr1 + '\n')
                    for f2 in f1._subfolders:
                        for fr2 in f2._robjects:
                            fil.write(intro + ",,," + f1._name + "," + f2._name + "," + fr2 + '\n')
                        for f3 in f2._subfolders:
                            for fr3 in f3._robjects:
                                fil.write(intro + ",," + f1._name + "," + f2._name + "," + f3._name + "," + fr3 + '\n')
        fil.close()
        print('Success')
          
d = Driver()

