from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import random

from config import email, password

class AutoSwipe:
    def __init__(self, driver):
        self.driver = driver
        self.auto_swipe_stats = {
            "session_duration": 0,
            "like": 0,
            "dislike": 0,
        }
    
    def auto_swipe(self, number_to_like, ratio=0.7):
        time.sleep(5)
        self.handle_potential_popups() # Say 'Maybe Later' to See Who Liked You and close Tinder Web Exclusive pop Up
        time.sleep(50)

        start = time.time()
        amount_liked = 0
        while amount_liked < number_to_like:
            # --------------------------------------------------------------
            # Possible end conditions where we can no longer make likes:
            #  1. No more remaining daily likes
            try:
                xpath = '//div[contains(text(), "Go Global")]'
                self.driver.find_element('xpath', xpath)
                print('Ran out of potential matches in the area.')
                break
            except NoSuchElementException:
                pass
            #  2. Ran out of potential matches in the area
            try:
                xpath = '//*[@id="q-314954669"]/div/div/div[1]/div[3]/div[1]/div[2]/div/div[1]/span[1]/div/div'
                self.driver.find_element('xpath', xpath)
                self.auto_swipe_stats['like'] -= 1  # To get this pop up, the bot must have tried to like the last person. This
                                                    # like does go through, but our # of likes for the session is still
                                                    # incremented by 1. To ensure this like doesn't count, we decrement
                                                    # the number of likes for the current session here.
                print('No more likes remaining for today.')
                break
            except NoSuchElementException:
                pass
            # --------------------------------------------------------------
            
            # Random clicking back and forth through the current profile's selection of photos. Mimics how 
            # a user flips through a profile's photos before deciding to like or dislike. 
            try:
                time.sleep(2)
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME,'body'), 0,0) # Test click
                actions.move_by_offset(260, 70).click().perform()
                for i in range(random.randint(6, 11)):
                    if i < 4 or random.random() <= 0.7:
                        # To flip to right image, click 260 pixels right and 70 pixels up from the middle of the page.
                        print('Right Image')
                        actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME,'body'), 0,0)
                        actions.move_by_offset(260, 70).click().perform()
                    else:
                        # To flip to left image, click 80 pixels right and 70 pixels up from the middle of the page.
                        print('Left Image')
                        actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME,'body'), 0,0)
                        actions.move_by_offset(80, 70).click().perform()

                    sleep_btw_flips = random.uniform(2.0, 4.0)
                    time.sleep(sleep_btw_flips)
                    
            except NoSuchElementException:
                print('Couldn\'t locate information button')
            
            # Swipe right or left
            if random.random() <= ratio:
                self.right_swipe()
                amount_liked += 1
                self.auto_swipe_stats['like'] += 1
            else:
                self.left_swipe()
                self.auto_swipe_stats['dislike'] += 1

            self.handle_potential_popups()
            
            # Randomize sleep between likes
            cur_sleep_length = random.uniform(3.0, 5.0)
            print(f"{amount_liked}/{number_to_like} liked, sleep: {cur_sleep_length}")
            time.sleep(cur_sleep_length)
           
        duration = int(time.time() - start)
        self.auto_swipe_stats["session_duration"] = duration
        self.print_auto_swipe_stats()
    
    # Right swipe is a like
    def right_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)
        
    # Left swipe is a dislike
    def left_swipe(self):
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_LEFT)
    
    def print_auto_swipe_stats(self):
        print(f"This session lasted {self.auto_swipe_stats['session_duration']} seconds.")
        print(f"You've liked {self.auto_swipe_stats['like']} profiles during this session.")
        print(f"You've disliked {self.auto_swipe_stats['dislike']} profiles during this session.")
    
    def handle_potential_popups(self):
        # Say 'Maybe Later' to See Who Likes You
        try:
            xpath = '//div[contains(text(), "Maybe Later")]'
            close_see_who_liked_you_button = self.driver.find_element('xpath', xpath)
            close_see_who_liked_you_button.click()
            print('Said "Maybe Later" to See Who Liked You')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass
        
        # Close Tinder Web Exclusive Pop Up
        try:
            xpath = '//*[@id="u-1419960890"]/div/div[1]/div/main/div[1]/div/button'
            close_tinder_web_exclusive_button = self.driver.find_element('xpath', xpath)
            close_tinder_web_exclusive_button.click()
            print('Closed Tinder Web Exclusive pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass
       
        # Close "It's a Match!" pop up
        try:
            xpath = '//*[@id="u-1089589689"]/div/div/div[1]/div/div[4]/button'
            close_ItsAMatch_button = self.driver.find_element('xpath', xpath)
            close_ItsAMatch_button.click()
            print('Closed "It\'s a Match! pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass