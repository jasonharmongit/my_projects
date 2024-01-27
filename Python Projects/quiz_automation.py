from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
import time
import subprocess

class Driver():

    def login(self):
        # start a browser in debugging mode:
        subprocess.Popen('C:\chrome-win\chrome.exe --remote-debugging-port=4200 --user-data-dir="C:\selenum\ChromeProfile"')
        time.sleep(3)
        self._chrome_options = Options()
        self._chrome_options.add_experimental_option("debuggerAddress", "localhost:4200")
        self._driver = webdriver.Chrome(options=self._chrome_options)
        
        self._driver.get('https://usu.instructure.com/')
        self._driver.find_element(By.XPATH,'//*[@name="loginfmt"]').send_keys('a02305364@aggies.usu.edu')
        self._driver.quit

    def connect(self):
        self._chrome_options = Options()
        self._chrome_options.add_experimental_option("debuggerAddress", "localhost:4200")
        self._driver = webdriver.Chrome(options=self._chrome_options)
        self._driver.implicitly_wait(10)

    def grade(self):
        grading_iframe = self._driver.find_element(By.XPATH, '//iframe[@id="speedgrader_iframe"]')
        self._driver.switch_to.frame(grading_iframe)

        answer = self._driver.find_element(By.XPATH,'//*[@class="user_content quiz_response_text enhanced"]').text
        print('\nstudent answer:')
        print('-------------------------------\n', answer)
        print('-------------------------------\n')
        
        commands_key = ['ls','cd','pwd','mkdir','cp','mv','man','touch','grep','ps']
        used_commands = []
        missed_commands = []
        self.points = 10
        for c in commands_key:
            if c in answer:
                used_commands.append(c)
            else:
                missed_commands.append(c)
                self.points -= 1
        print('used commands: ', used_commands)
        print('missed commands: ', missed_commands)
        print('points recieved: ', self.points)

        if self.points < 10:
            print('[COMMENT:]')
            print("Didn't demonstrate the following commands: ", missed_commands)
            print('\n\n\n')

    def comment(self):
        com_loop = True
        while com_loop == True:
            com_text = input('enter comment text:')
            good = input('[COMMENT]:\n{}\n\ngood? ([enter]=yes, [n]=no)'.format(com_text))
            if good == '':
                self._driver.find_element(By.XPATH,'(//div[@class="quiz_comment"])[last()]/textarea').send_keys(com_text)
                com_loop = False
    
    def main(self):
        main_loop = True
        graded_count = 0
        while main_loop:
            self.grade()

            next_step = input('<copy/paste comment, if necessary. enter a number to override the points awared, press [enter] to continue, or press [e] to end.>')
            confirm_loop = True
            award_points = self.points
            while confirm_loop:
                try:
                    award_points = int(next_step)
                    next_step = input('override with {} points? <re-enter new points, hit [enter] for yes, or hit [r] to revert back to detected points>'.format(award_points))
                    if next_step == '':
                        confirm_loop = False 
                    elif next_step == 'r':
                        next_step = self.points
                        award_points = self.points
                except:
                    confirm_loop = False

            if next_step == '':
                self._driver.find_element(By.XPATH,'(//input[@class="question_input"])[last()]').send_keys(str(award_points))
                self._driver.find_element(By.XPATH,'//button[@class="btn btn-primary update-scores"]').click()
                self._driver.quit
                time.sleep(1)
                self.connect()
                self._driver.find_element(By.ID,'next-student-button').click()
                graded_count += 1
            else:
                main_loop = False
                print('grading session complete. you graded {} students'.format(graded_count))


# driver code:
d = Driver()
# d.login()
d.connect()
d.main()
# d.comment()
print()