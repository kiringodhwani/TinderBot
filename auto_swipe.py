from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import random
import urllib
import requests
import os
import pickle

import numpy as np
import cv2
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN
import tensorflow as tf
from sklearn.preprocessing import Normalizer

from config import email, password

class AutoSwipe:
    """
    A class for auto swiping in an open, logged-into Tinder page in Chrome. 
    
    Option 1 for Auto Swiping: Race-based auto swiping for East Asian women.
    
    Option 2: Randomly flipping through each Tinder profile's collection of images with random
    pauses between flips (mimics how users flip through a profile's photos before deciding to like
    or dislike), pausing for random amounts of time between swipes, and by allowing users to
    determine how many profiles they would like to 'like' (i.e., swipe right on) and what
    percentage of profile's they would like to 'like' (e.g., 70% of profiles).
    
    Attributes
    ----------
    driver : webdriver.Chrome
        A WebDriver instance for Chrome that contains a logged into Tinder page.
    
    auto_swipe_stats : dict
        Tracks the duration of the current auto swiping session and the number of likes and
        dislikes that have occurred.
    
    detector : mtcnn.mtcnn.MTCNN
        Multi-Task Cascaded Convolutional Neural Network (MTCNN) for face detection. This is
        a deep learning model presented in "Joint Face Detection and Alignment Using Multitask 
        Cascaded Convolutional Networks" from 2016.
    
    face_embedding_model : keras.src.models.functional.Functional
        A ResNet50 neural network pre-trained on ImageNet that we use to create face embeddings from faces
        detected in Tinder profile images (https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50).
        
    Methods
    -------
    face_recognition_smart_swipe(number_to_like): 
        Smart swipes through the profiles in an open, logged-into Tinder page in Chrome. Only
        swipes right on (i.e., 'likes') the profiles of people who resemble Mindy Kaling. Swipes
        right on 'number_to_like' profiles in total. Handles any pop ups that appear during the
        auto swiping process.
        
    get_face_embedding(face_pixels):
        Gets the face embedding for one face.
    
    count_faces(filename):
        Counts the number of faces in an image. If the image has exactly 1 face, then also returns
        the pixel coordinates of the bounding box for the face. 
    
    extract_face(filename, x1, x2, y1, y2):
        Provided an image with only one face and the pixel coordinates of the bounding box for
        the face, extracts the face from the image. 
        
    access_current_image(image_number):
        Accesses and downloads the current image of the current profile on the Tinder page.
        
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
    
    delete_files_in_directory(directory_path):
        Deletes all of the files in a directory.
    """
    
    def __init__(self, driver):
        """Initializes a new instance of the AutoSwipe class. Stores the WebDriver instance and
           a dictionary to track the stats of the auto swiping session. Also instantiates a
           Multi-Task Cascaded Convolutional Neural Network (MTCNN) for face detection. This is
           a deep learning model presented in "Joint Face Detection and Alignment Using Multitask 
           Cascaded Convolutional Networks" from 2016. Lastly, instantiates a ResNet50 neural
           network pre-trained on ImageNet that we use to create face embeddings from faces detected
           in Tinder profile images (https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50).
        
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
        self.detector = MTCNN()
        self.face_embedding_model = tf.keras.applications.ResNet50(weights='imagenet')
    
    def face_recognition_smart_swipe(self, number_to_like):
        """Smart swipes through the profiles in an open, logged-into Tinder page in Chrome. Only
        swipes right on (i.e., 'likes') the profiles of people who resemble Mindy Kaling. Swipes
        right on 'number_to_like' profiles in total. Handles any pop ups that appear during the
        auto swiping process.
        
        Parameters
        ----------
            number_to_like : int
                The total number of profiles to be swiped right on ('liked')
        """
        self.handle_potential_popups() # Say 'Maybe Later' to See Who Liked You and close Tinder Web Exclusive pop Up
        print()
        
        time.sleep(5)
        
#         # Load the Mindy Kaling facial recognition classifier.
#         with open('mlpclassifier_v1.pkl', 'rb') as f:
#             model = pickle.load(f)

        # Load the East Asian or Not Classifier
        with open('KNNclassifier_v1.pkl', 'rb') as f:
            model = pickle.load(f)
        
            
        # For normalizing face embeddings.
        in_encoder = Normalizer(norm='l2')
        
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
            
#             # Click the information button to expand the profile
#             xpath = '//*[@id="c-1330188189"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div/div/div[1]/button'
#             information_button = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
#             information_button.click()
#             time.sleep(2)
            
            # Click once to expand the profile
            actions = ActionChains(self.driver)
            actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME,'body'), 0,0) # Test click
            actions.move_by_offset(80, 70).click().perform()
                
            # Flip through the current profile's set of photos. Apply a facial recognition classifier that is
            # trained to recognize faces that resemble Mindy Kaling. Apply the facial recognition classifier
            # to images in the current user's profile that have only one face and swipe right if the model
            # detects Mindy Kaling with a confidence of at least 0.9. Otherwise, swipes left.
            image_number = 1
            try:
                while True:
                    self.access_current_image(image_number=image_number)
                    
                    # Count the number of faces in the image. If there is exactly 1 face, then extract it.
                    path = f'sample_data/im{str(image_number)}.jpg'
                    count, x1, x2, y1, y2 = self.count_faces(path)
                    if count == 1:
                        face = self.extract_face(path, x1, x2, y1, y2)
                        
                        # Get face embedding of the extracted face.
                        face_embedding = self.get_face_embedding(face)
                        
                        # Normalize face embedding.
                        face_embedding = in_encoder.transform(face_embedding.reshape(1, -1))
                        
                        # Apply the Mindy Kaling facial recognition classifier to the normalized face embedding. 
                        # If the model has at least 90% confidence that the face is Mindy Kaling (i.e., there
                        # is strong resemblance between the person and Mindy Kaling), then the bot swipes right
                        # (i.e., "likes") the current profile.
                        samples = np.expand_dims(face_embedding[0], axis=0)
                        yhat_prob = model.predict_proba(samples)
                        time.sleep(3)
                        if yhat_prob[0][0] >= 0.75:
                            print(f"\n75+% confidence ({yhat_prob[0][0] * 100}%) that the current person is East Asian, indicating strong likelihood of being East Asian. Right swipe ('like') current profile.\n")
                            amount_liked += 1
                            self.auto_swipe_stats['like'] += 1
                            time.sleep(10)
                            self.right_swipe()
                            break
                        else:
                            print(f"\nUnder 75% confidence ({yhat_prob[0][0] * 100}%) that the current person is East Asian, indicating weak likelihood of being East Asian. Flipping to next photo in profile.\n")

                    # To flip to right image, click 260 pixels right and 70 pixels up from the middle of the page.
                    print('Right Image\n')
                    actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME,'body'), 0,0)
                    actions.move_by_offset(260, 70).click().perform()

                    image_number += 1

                    cur_sleep_length = random.uniform(3.0, 5.0)
                    time.sleep(cur_sleep_length)
                    
            except (NoSuchElementException, TimeoutException) as e:
                print("Flipped through all photos for the current profile without finding a strong likelihood of being East Asian. Left swipe ('dislike') current profile.\n")
                self.auto_swipe_stats['dislike'] += 1
                time.sleep(2)
                self.left_swipe()
            
            # Delete all of the photos saved from the current Tinder profile.
            self.delete_files_in_directory('sample_data')
            
            # Handle any pop ups that occur after swiping (e.g., "It's a Match!" pop up).
            time.sleep(5)
            self.handle_potential_popups()
            
            # Randomize sleep between likes.
            cur_sleep_length = random.uniform(6.0, 9.0)
            print(f"{amount_liked}/{number_to_like} liked, sleep: {cur_sleep_length}")
            term_size = os.get_terminal_size()
            print('-' * term_size.columns)
            print()
            time.sleep(cur_sleep_length)
           
        duration = int(time.time() - start)
        self.auto_swipe_stats["session_duration"] = duration
        self.print_auto_swipe_stats()
        
        
    def get_face_embedding(self, face_pixels):
        """Gets the face embedding for one face.
        
        Parameters
        ----------
            face_pixels : numpy.ndarray
                The face to get the embedding for.
        
        """
        face_pixels = face_pixels.astype('float64')

        # Standardize pixel values across channels (global).
        mean, std = face_pixels.mean(), face_pixels.std()
        face_pixels = (face_pixels - mean) / std

        # Transform face into one sample.
        samples = np.expand_dims(face_pixels, axis=0)

        # Make prediction to get embedding.
        yhat = self.face_embedding_model.predict(samples)
        return yhat[0]
          
            
    def count_faces(self, filename):
        """Counts the number of faces in an image. If the image has exactly 1 face, then also returns
        the pixel coordinates of the bounding box for the face. 
        
        Parameters
        ----------
            filename : str
                The filename of the image to be analyzed.
        
        Returns
        -------
            num_faces : int
                The number of faces in the image.
            x1 : int, x2 : int, y1: int, y2: int
                The pixel coordinates of the bounding box for the face.
        """
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
        pixels = np.asarray(img)

        results = self.detector.detect_faces(pixels)

        for i, face in enumerate(results): 
            x1, y1, width, height = face['box']
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2) 

            # Display the box and faces 
            cv2.putText(img, 'face num'+str(i), (x1-10, y1-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2) 

        output = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        plt.figure(figsize=(5, 5))
        plt.axis("off")
        plt.imshow(output)
        plt.show()
        
        num_faces = len(results)
        if num_faces != 1:
            print(f'\n{num_faces} faces found in the current photo. Flipping to next photo...\n')
            return num_faces, 0, 0, 0, 0
        else:  
            print(f'\n{num_faces} face found in photo. Extracting face and applying East Asian classifier...\n')
            return num_faces, x1, x2, y1, y2
        
    
    def extract_face(self, filename, x1, x2, y1, y2):
        """Provided an image with only one face and the pixel coordinates of the bounding box for
        the face, extracts the face from the image. 
        
        Parameters
        ----------
            filename : str
                The filename of the image to be analyzed.
            x1 : int, x2 : int, y1: int, y2: int
                The pixel coordinates of the bounding box for the face.
        
        Returns
        -------
            face_array : numpy.ndarray
                The extracted face.
        """
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 
        pixels = np.asarray(img)

        face = pixels[y1:y2, x1:x2]
        face_array = cv2.resize(face, (224, 224))

        fig, ax = plt.subplots(figsize=(5, 5))
        plt.imshow(face_array)
        plt.show()
        return face_array
    
                
    def access_current_image(self, image_number):
        """Accesses and downloads the current image of the current profile on the Tinder page.
        
        Parameters
        ----------
            image_number : int
                What number image we are on for the current profile. For the first image in the current user's
                profile, image_number = 1. For the second image in the current user's profile, image_number = 2.
                Etc.
        """
        xpath = f'//*[@id="c-1330188189"]/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div[1]/span/div/div[1]/span[{image_number}]/div/div'

        #img = self.driver.find_element('xpath', xpath)
        img = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        # Access and store image url
        image_url = img.value_of_css_property('background-image').split('\"')[1]
            
        # Retrieve and download the image
        urllib.request.urlretrieve(str(image_url),f"sample_data/im{str(image_number)}.jpg")
        
    
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
            print('\nSaid "Maybe Later" to See Who Liked You')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass
        
        # Close Tinder Web Exclusive Pop Up
        try:
            xpath = '//*[@id="c-1330188189"]/div/div[1]/div/main/div[1]/div/button'
            close_tinder_web_exclusive_button = self.driver.find_element('xpath', xpath)
            close_tinder_web_exclusive_button.click()
            print('\nClosed Tinder Web Exclusive pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass
       
        # Close "It's a Match!" pop up
        try:
            xpath = '//*[@id="t371990310"]/div/div/div[1]/div/div[4]/button'
            close_ItsAMatch_button = self.driver.find_element('xpath', xpath)
            close_ItsAMatch_button.click()
            print('\nClosed "It\'s a Match!" pop up\n')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass
        
        # Close "Add Tinder to Home Screen pop up"
        try:
            xpath = '//*[@id="u1146625330"]/div/div/div[2]/button'
            close_ItsAMatch_button = self.driver.find_element('xpath', xpath)
            close_ItsAMatch_button.click()
            print('\nClosed "Add Tinder to Home Screen" pop up\n')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass

    def delete_files_in_directory(self, directory_path):
        """Deletes all of the files in a directory.
        
        Parameters
        ----------
            directory_path : str
                The directory to have all of its files deleted.
        """
        try:
            files = os.listdir(directory_path)
            for file in files:
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"All photos for the current profile deleted successfully from {directory_path}.\n")
        except OSError:
            print("Error occurred while deleting files.")