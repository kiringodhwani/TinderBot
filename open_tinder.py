from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import email, password

class OpenTinder:
    def __init__(self):
        self.driver = webdriver.Chrome()
       
    def open_tinder(self):
        sleep(2)
        self.driver.get('https://tinder.com')
        
        # Log in with Facebook
        xpath = '//div[contains(text(), "Log in")]'
        login_button = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
        login_button.click()
        self.handle_potential_popups() # Cookie Button
        sleep(5)
#         self.facebook_login()
#         sleep(6)
        
#         self.handle_potential_popups()
    
#     def facebook_login(self):
#         # Find and click the Facebook login button
#         xpath = '//div[contains(text(), "Log in with Facebook")]'
#         login_with_facebook = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
#         login_with_facebook.click()

#         # Save references to main and Facebook windows
#         sleep(8)
#         base_window = self.driver.window_handles[0]
#         fb_popup_window = self.driver.window_handles[1]
        
#         # Switch to Facebook window
#         self.driver.switch_to.window(fb_popup_window)

#         self.handle_potential_popups()
        
#         sleep(10)
#         email_field = self.driver.find_element(By.NAME, 'email')
#         pw_field = self.driver.find_element(By.NAME, 'pass')
#         login_button = self.driver.find_element(By.NAME, 'login')
#         email_field.send_keys(email)
#         pw_field.send_keys(password)
#         login_button.click()
#         self.driver.switch_to.window(base_window)
        
#         self.handle_potential_popups()
    
    def handle_potential_popups(self):
        
        # Accept Cookies
        try:
            xpath = '//div[contains(text(), "I accept")]'
            cookies_accept_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            cookies_accept_button.click()
            print('Accepted Cookies')
        except:
            pass
        
        # Notifications Popup
        try:
            xpath = '/html/body/div[2]/main/div/div/div/div[3]/button[2]'
            notifications_button = self.driver.find_element('xpath', xpath)
            notifications_button.click()
            print('Allowed Notifications')
        except:
            pass

        # Allow Location Popup
        try:
            xpath = '//*[@id="t-1917074667"]/main/div/div/div/div[3]/button[1]'
            allow_location_button = self.driver.find_element('xpath', xpath)
            allow_location_button.click()
            print('Allowed Location')
        except:
            pass
        
        # Enable Location Popup
        try:
            xpath = '//div[contains(text(), "Enable")]'
            enable_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            enable_button.click()
            print('Enabled Location')
        except:
            pass

        return None