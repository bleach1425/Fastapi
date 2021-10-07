from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import time

class auto_phone_king():
    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        self.chrome = webdriver.Chrome('./chromedriver', chrome_options=options)
        self.chrome.implicitly_wait(15)
    def Go_Page(self):
        self.chrome.get('https://www.sogi.com.tw/')
        self.chrome.maximize_window()
    def find_login_button(self):
        self.chrome.find_element_by_xpath('//*[@id="navbarSupportedContent"]/div/ul/li[2]/a/i').click()
    def login(self):
        self.chrome.find_element_by_id('user_account').send_keys('rubio6969s@gmail.com')
        time.sleep(0.5)
        self.chrome.find_element_by_id('user_password').send_keys('eftest')
        time.sleep(0.5)
        self.chrome.find_element_by_xpath('//*[@id="new_user"]/div[4]/button').click()
    def search_img(self):
        pyautogui.moveTo(1021, 497)
        self.chrome.implicitly_wait(3)
        while 1:
            distance = 300
            pyautogui.scroll(-distance)
            r = pyautogui.locateOnScreen('images.jpg', confidence=0.8)
            print(r)
            if r:
                break
        time.sleep(5)
        print("Test End")

def main():
    func = auto_phone_king()
    func.Go_Page()
    func.find_login_button()
    func.login()
    func.search_img()

if __name__ == '__main__':
    main()