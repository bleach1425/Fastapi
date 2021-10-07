from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import os

class function():
    def __init__(self):
        pass
    def selenium_config(self):
        options = Options()
        options.add_argument("--disable-notifications")
        chrome = webdriver.Chrome('./selenium_setting/chromedriver.exe', chrome_options=options)
        chrome.maximize_window()
        return chrome


if __name__ == '__main__':
    func = function()
    chrome = func.selenium_config()
    chrome.get('https://google.com')
