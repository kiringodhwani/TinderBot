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
    """
    A class for auto swiping in an open, logged-into Tinder page in Chrome. The auto swiping
    mimics human behavior by randomly flipping through each Tinder profile's collection of 
    images with random pauses between flips (mimics how users flip through a profile's photos
    before deciding to like or dislike), pausing for random amounts of time between swipes,
    and by allowing users to determine how many profiles they would like to 'like' (i.e., swipe
    righton ) and what percentage of profile's they would like to 'like' (e.g., 70% of profiles).
    
    Attributes
    ----------
    driver : webdriver.Chrome
        A WebDriver instance for Chrome that contains a logged into Tinder page.
    
    auto_swipe_stats : dict
        Tracks the duration of the current auto swiping session and the number of likes and
        dislikes that have occurred.
        
    Methods
    -------
    auto_swipe(number_to_like, ratio=0.7):
        Auto swipes through the profiles in an open, logged-into Tinder page in Chrome. Swipes
        right on (i.e., 'likes') 'number_to_like' profiles and uses 'ratio' to determine how
        frequently profiles are liked (e.g., 70% of the time). To mimic human behavior, randomly
        clicks back and forth through each profile's selection of photos (mimics how a user 
        flips through a profile's photos before deciding to like or dislike), pauses between swipes,
        and stops swiping if the user runs out of likes or potential matches. Handles any pop ups
        that appear during the auto swiping process.
        
    right_swipe():
        Swipes right on ('likes') the current profile. 
    
    left_swipe(): 
        Swipes left on ('dislikes') the current profile.
    
    print_auto_swipe_stats():
        Prints the results from the auto swiping session that are stored in self.auto_swipe_stats.
        These stats include the the duration of the session and the number of likes and dislikes
        that occurred. 
        
    handle_potential_popups():
        Defines the logic to handle pop ups that appear during the auto swiping process. This
        includes declining a pop up that asks if you want to 'See Who Likes You', closing a pop up
        advertising 'Tinder Web Exclusive', and closing the 'It's a Match!' pop up that appeares
        when you swipe right on someone that also swiped right on you. 
    """
    
    def __init__(self, driver):
        """Initializes a new instance of the AutoSwipe class. Stores the WebDriver instance and
           a dictionary to track the stats of the auto swiping session.
        
        Parameters
        ----------
            driver : webdriver.Chrome
                Accepts a WebDriver instance for Chrome that contains a logged into Tinder page.
                REQUIRES that the Tinder page has ALREADY BEEN LOGGED INTO.
        """
        self.driver = driver
        self.auto_swipe_stats = {
            "session_duration": 0,
            "like": 0,
            "dislike": 0,
        }
    
    def auto_swipe(self, number_to_like, ratio=0.7):
        """Auto swipes through the profiles in an open, logged-into Tinder page in Chrome. Swipes
        right on (i.e., 'likes') 'number_to_like' profiles and uses 'ratio' to determine how
        frequently profiles are liked (e.g., 70% of the time). To mimic human behavior, randomly
        clicks back and forth through each profile's selection of photos (mimics how a user 
        flips through a profile's photos before deciding to like or dislike), pauses between swipes,
        and stops swiping if the user runs out of likes or potential matches. Handles any pop ups
        that appear during the auto swiping process.
        
        Parameters
        ----------
            number_to_like : int
                The total number of profiles to be swiped right on ('liked')
            ratio : float
                How often profiles should be swiped right on (e.g, 0.7 --> 70% of the time)
        """
        self.handle_potential_popups() # Say 'Maybe Later' to See Who Liked You and close Tinder Web Exclusive pop Up
        print()

        start = time.time()
        amount_liked = 0
        while amount_liked < number_to_like:
            # --------------------------------------------------------------
            # Possible end conditions where we can no longer make likes:
            #  1. Ran out of potential matches in the area
            try:
                xpath = '//div[contains(text(), "Go Global")]'
                self.driver.find_element('xpath', xpath)
                print('Ran out of potential matches in the area.\n')
                break
            except NoSuchElementException:
                pass
            #  2. No more remaining daily likes
            try:
                xpath = '//*[@id="u1146625330"]/div/div/div[2]/button'
                close_ran_out_of_likes_popup = self.driver.find_element('xpath', xpath)
                close_ran_out_of_likes_popup.click()
                self.auto_swipe_stats['like'] -= 1  # To get this pop up, the bot must have tried to like the last person. This
                                                    # like does go through, but our # of likes for the session is still
                                                    # incremented by 1. To ensure this like doesn't count, we decrement
                                                    # the number of likes for the current session here.
                print('No more likes remaining for today.\n')
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
                    if i < 3 or random.random() <= 0.7:
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
                print('Couldn\'t click at page center\n')
            
            # Swipe right or left
            if random.random() <= ratio:
                print("Right swipe ('like') current photo")
                self.right_swipe()
                amount_liked += 1
                self.auto_swipe_stats['like'] += 1
            else:
                print("Left swipe ('dislike') current photo")
                self.left_swipe()
                self.auto_swipe_stats['dislike'] += 1

            self.handle_potential_popups()
            
            # Randomize sleep between likes
            cur_sleep_length = random.uniform(3.0, 5.0)
            print(f"{amount_liked}/{number_to_like} liked, sleep: {cur_sleep_length}\n")
            time.sleep(cur_sleep_length)
           
        duration = int(time.time() - start)
        self.auto_swipe_stats["session_duration"] = duration
        self.print_auto_swipe_stats()
    
    # Right swipe is a like
    def right_swipe(self):
        """Swipes right on ('likes') the current profile.
        """
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_RIGHT)
        
    # Left swipe is a dislike
    def left_swipe(self):
        """Swipes left on ('dislikes') the current profile.
        """
        doc = self.driver.find_element('xpath', '//*[@id="Tinder"]/body')
        doc.send_keys(Keys.ARROW_LEFT)
    
    def print_auto_swipe_stats(self):
        """Prints the results from the auto swiping session that are stored in self.auto_swipe_stats.
        These stats include the the duration of the session and the number of likes and dislikes
        that occurred. 
        """
        print(f"This session lasted {self.auto_swipe_stats['session_duration']} seconds.")
        print(f"You've liked {self.auto_swipe_stats['like']} profiles during this session.")
        print(f"You've disliked {self.auto_swipe_stats['dislike']} profiles during this session.")
    
    def handle_potential_popups(self):
        """Defines the logic to handle pop ups that appear during the auto swiping process. This
        includes declining a pop up that asks if you want to 'See Who Likes You', closing a pop up
        advertising 'Tinder Web Exclusive', and closing the 'It's a Match!' pop up that appeares
        when you swipe right on someone that also swiped right on you.
        """
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
            xpath = '//*[@id="t41619109"]/div/div[1]/div/main/div[1]/div/button'
            close_tinder_web_exclusive_button = self.driver.find_element('xpath', xpath)
            close_tinder_web_exclusive_button.click()
            print('Closed Tinder Web Exclusive pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass
       
        # Close "It's a Match!" pop up
        try:
            #xpath = '//*[@id="u-1089589689"]/div/div/div[1]/div/div[4]/button'
            xpath = '//*[@id="t371990310"]/div/div/div[1]/div/div[4]/button'
            close_ItsAMatch_button = self.driver.find_element('xpath', xpath)
            close_ItsAMatch_button.click()
            print('Closed "It\'s a Match!" pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass
        
        # Close "Add Tinder to Home Screen pop up"
        try:
            xpath = '//*[@id="u1146625330"]/div/div/div[2]/button'
            close_ItsAMatch_button = self.driver.find_element('xpath', xpath)
            close_ItsAMatch_button.click()
            print('Closed "Add Tinder to Home Screen" pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass