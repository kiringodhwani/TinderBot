from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

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

        start = time.time()
        amount_liked = 0
        while amount_liked < number_to_like:
            # Possible end conditions where we can no longer make likes:
            #  1. No more remaining daily likes
            #  2. Ran out of potential matches in the area
            try:
                xpath = '//div[contains(text(), "Go Global")]'
                self.driver.find_element('xpath', xpath)
                print('Ran out of potential matches in the area.')
                break
            except NoSuchElementException:
                pass
            
            if random.random() <= ratio:
                self.right_swipe()
                amount_liked += 1
                self.auto_swipe_stats['like'] += 1
            else:
                self.left_swipe()
                self.auto_swipe_stats['dislike'] += 1

            self.handle_potential_popups()
            
            # Randomize sleep between likes
            cur_sleep_length = random.uniform(0.5, 2.3)
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
            xpath = '//*[@id="q1413426407"]/div/div[1]/div/main/div[1]/div/button'
            close_tinder_web_exclusive_button = self.driver.find_element('xpath', xpath)
            close_tinder_web_exclusive_button.click()
            print('Closed Tinder Web Exclusive pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass