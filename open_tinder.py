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
        
        # Open Tinder in a Chrome window
        self.driver.get('https://tinder.com')
        
        # Click the log in button to open the login options (e.g., Facebook, Google,...)
        xpath = '//div[contains(text(), "Log in")]'
        login_button = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)))
        login_button.click()
        self.handle_potential_popups() # Possible Cookie Button
        sleep(5)
        
        # Log in with Facebook
        self.facebook_login()
        sleep(15)
        
        self.handle_potential_popups() # Allow Location Pop Up
        self.handle_potential_popups() # Deny Notifications Pop Up
    
    def facebook_login(self):
        # Find and click the Facebook login button
        xpath = '//div[contains(text(), "Log in with Facebook")]'
        login_with_facebook = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        login_with_facebook.click()

        # Save references to Tinder and Facebook windows
        sleep(5)
        base_window = self.driver.window_handles[0]
        fb_popup_window = self.driver.window_handles[1]
        
        # Switch to Facebook window
        self.driver.switch_to.window(fb_popup_window)

        self.handle_potential_popups()
        sleep(2)

        # Input Facebook login (i.e., email and password)
        email_field = self.driver.find_element(By.NAME, 'email')
        password_field = self.driver.find_element(By.NAME, 'pass')
        email_field.send_keys(email)
        password_field.send_keys(password)
        
        # Click to log in
        login_button = self.driver.find_element(By.NAME, 'login')
        login_button.click()
        
        # Switch back to Tinder window
        self.driver.switch_to.window(base_window)
    
    def handle_potential_popups(self):
        # Accept Cookies
        try:
            xpath = '//div[contains(text(), "I accept")]'
            cookies_accept_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            cookies_accept_button.click()
            print('Accepted Cookies')
        except:
            pass

        # Allow Location Popup
        try:
            xpath = '//*[@id="q-314954669"]/div/div/div/div/div[3]/button[1]/div[2]/div[2]'
            allow_location_button = self.driver.find_element('xpath', xpath)
            allow_location_button.click()
            print('Allowed Location')
        except:
            pass
        
        # Deny Notifications Popup
        try:
            xpath = '//*[@id="q-314954669"]/div/div/div/div/div[3]/button[2]/div[2]/div[2]'
            notifications_button = self.driver.find_element('xpath', xpath)
            notifications_button.click()
            print('Denied Notifications')
        except:
            pass

        return None