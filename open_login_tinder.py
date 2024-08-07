from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import email, password

class OpenLoginTinder:
    """
    A class for opening a Chrome window, logging into Tinder.com using a Facebook account, and
    handling any pop ups that appear during the login process.
    
    Attributes
    ----------
    driver : webdriver.Chrome
        Allows us to control a Chrome session with Python code.
        
    Methods
    -------
    open_login_tinder():
        Opens tinder.com in Chrome, logs into Tinder using Facebook, and handles any pop ups
        that appear during the login process.
    
    facebook_login():
        Provided the login page on Tinder, clicks the Facebook login option, logs in by inputting
        Facebook credentials, and handles any pop ups that appear.
        
    handle_potential_popups():
        Defines the logic to handle pop ups that appear during the login process. This includes
        selecting 'accept' on a pop up about accepting cookies, selecting 'allow' on a pop up
        about allowing Tinder to use your location, and selecting 'deny' on a pop up about
        allowing Tinder to send you notifications.
    """
    
    def __init__(self):
        """Initializes a new instance of the OpenLoginTinder class.
           
        Parameters
        ----------
            driver : webdriver.Chrome class
                This method creates a new WebDriver instance using ChromeDriver. This driver
                can then be used to interact with a Chrome browser for web automation.
        """
        self.driver = webdriver.Chrome()
       
    def open_login_tinder(self):
        """Opens tinder.com in Chrome, logs into Tinder using Facebook, and handles any pop ups
           that appear during the login process.
        
        Returns
        -------
            self.driver : webdriver.Chrome
                The WebDriver instance for Chrome that contains the logged into Tinder page. 
        """
        # Open Tinder in a Chrome window
        self.driver.get('https://tinder.com')

        sleep(2)
        self.handle_potential_popups() # Possible Cookie Button
        sleep(3)
        
        # Click the log in button to open the login options (e.g., Facebook, Google,...)
        xpath = '//div[contains(text(), "Log in")]'
        login_button = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, xpath)))
        login_button.click()
        
        # Log in with Facebook
        self.facebook_login()
        sleep(10)
        
        self.handle_potential_popups() 
        sleep(15)
        return self.driver
    
    def facebook_login(self):
        """Provided the login page on Tinder, clicks the Facebook login option, logs in by inputting
           Facebook credentials, and handles any pop ups that appear.
        """
        # Find and click the Facebook login button
        xpath = '//div[contains(text(), "Log in with Facebook")]'
        login_with_facebook = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, xpath)))
        login_with_facebook.click()
        sleep(3)
        
        # Save references to Tinder and Facebook windows
        base_window = self.driver.window_handles[0]
        fb_popup_window = self.driver.window_handles[1]
        
        # Switch to Facebook window
        self.driver.switch_to.window(fb_popup_window)

        #self.handle_potential_popups()

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
        """Defines the logic to handle pop ups that appear during the login process. This includes
        selecting 'accept' on a pop up about accepting cookies, selecting 'allow' on a pop up
        about allowing Tinder to use your location, and selecting 'deny' on a pop up about
        allowing Tinder to send you notifications.
        """
        # Accept Cookies
        try:
            xpath = '//div[contains(text(), "I accept")]'
            cookies_accept_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            cookies_accept_button.click()
            print('Accepted Cookies')
            time.sleep(8)
            self.handle_potential_popups()
        except:
            pass

        # Allow Location Popup
        try:
            xpath = '//div[contains(text(), "Allow")]'
            allow_location_button = self.driver.find_element('xpath', xpath)
            allow_location_button.click()
            print('Allowed Location')
            time.sleep(8)
            self.handle_potential_popups()
        except:
            pass
        
        # Deny Notifications Popup
        try:
            xpath = '//*[@id="o-1596989266"]/div/div/div/div/div[3]/button[2]'
            notifications_button = self.driver.find_element('xpath', xpath)
            notifications_button.click()
            print('Denied Notifications')
            time.sleep(8)
            self.handle_potential_popups()
        except:
            pass

        return None