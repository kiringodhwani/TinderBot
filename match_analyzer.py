from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import random
import requests

from config import email, password, api_key
from match import Match

content = '/html/body/div[1]'

class MatchAnalyzer:
    """
    A class for scraping important information from your Tinder matches (i.e., Chat ID, name, 
    age, work, place of study, location of home, gender, Tinder bio, relationship preference,
    distance from you, and passions) and then using the scraped information to generate and
    send messages to the matches. 
    
    Attributes
    ----------
    driver : webdriver.Chrome
        A WebDriver instance for Chrome that contains a logged into Tinder page.
        
    Methods
    -------
    get_and_message_all_new_matches():
        Gets the Chat IDs of all the user's new, unmessaged Tinder matches and then scrapes 
        various pieces of information from these profiles (see the Match class). Then, sends
        a message to each new match based on the scraped information.
    
    send_intro_message(match):
        Sends an introductory message to a specific match. 
    
    create_message(match):
        Creates an introductory message for a specific Tinder match that is new and has
        not been messaged yet.
    
    get_chat_ids():
        Clicks into the 'Matches' tab on Tinder to see new matches and then scrapes the Chat ID
        associated with each match. These Chat IDs act as unique identifiers for each match on
        Tinder.
    
    get_match(chatid):
        Extracts all of the important information for a match (e.g., name, age, bio,
        passions, etc.) using its Chat ID.
    
    open_chat(chatid):
        Opens the 'Chat Page' for the match with the passed in Chat ID. The 'Chat Page' consists
        of a message box to communicate with the match as well as the match's profile. From the
        'Chat Page', we can scrape all necessary information from the match's profile. 
    
    is_chat_opened(chatid):
        Verifies if the 'Chat Page' for the match with the passed in Chat ID is currently opened in
        the Chrome driver.
    
    get_name(chatid):
        Provided the Chat ID of a specific match, scrapes the match's name from the match's 'Chat Page'.
    
    get_age(chatid):
        Provided the Chat ID of a specific match, scrapes the match's age from the match's 'Chat Page'.
    
    get_passions(chatid):
        Provided the Chat ID of a specific match, scrapes the match's passions from the match's 'Chat Page'.
    
    get_bio(chatid):
        Provided the Chat ID of a specific match, scrapes the match's Tinder bio from the match's 'Chat Page'.
    
    get_looking_for(chatid):
        Provided the Chat ID of a specific match, scrapes the match's relationship preference from the
        match's 'Chat Page'.
    
    get_row_data(chatid):
        Provided the Chat ID of a specific match, scrapes the match's work, place of study, location of
        home, gender, and distance from you from the match's 'Chat Page'.
        
    handle_potential_popups():
        Defines the logic to handle pop ups that appear while scraping information from your matches. This
        includes declining a pop up that asks if you want to 'See Who Likes You' and closing a pop up
        advertising 'Tinder Web Exclusive'.
    """
    
    def __init__(self, driver):
        """Initializes a new instance of the MatchScraper class.
        
        Parameters
        ----------
            driver : webdriver.Chrome
                Accepts a WebDriver instance for Chrome that contains a logged into Tinder page.
                REQUIRES that the Tinder page has ALREADY BEEN LOGGED INTO.
        """
        self.driver = driver
        
    def get_and_message_all_new_matches(self):
        """Gets the Chat IDs of all the user's new, unmessaged Tinder matches and then scrapes 
        various pieces of information from these profiles (see the Match class). Then, sends
        a message to each new match based on the scraped information.
        
        Returns
        -------
            matches : list
                A list of Match objects. Each Match object represents one scraped Tinder match and
                contains the match's Chat ID, name, age, work, place of study, location of home, gender,
                Tinder bio, relationship preference, distance from you, and passions. 
        """
        self.handle_potential_popups()
        time.sleep(5)
        
        iteration = 0
        matches = []
        used_chatids = ['recs'] # allows us to determine if we accidentally repeat chat IDs while scrolling.
        
        # We keep scrolling through all new matches until we have processed all of them.
        while True:
            print('\nGetting Chat IDs of all new matches...')
            new_chatids = self.get_chat_ids()
            copied = new_chatids.copy()
            for chatid in copied:
                if chatid in used_chatids:
                    new_chatids.remove(chatid)
                else:
                    used_chatids.append(chatid)
            
            # Break if no new matches are found
            if len(new_chatids) == 0:
                print('No more new matches found :(')
                break
            
            print('New Chat IDs: ', new_chatids)

            print('Getting information for each match using the Chat IDs...\n')
            for chatid in new_chatids:
                iteration += 1
                print(f'Scraping information from match #{iteration}...')
                new_match = self.get_match(chatid)
                print(new_match.get_dictionary())
                
                print('Sending introductory message to match...')
                self.send_intro_message(new_match)
                matches.append(new_match)

            print('Scrolling down to get more Chat IDs...')
            xpath = '//div[@role="tabpanel"]'
            tab = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', tab)
            time.sleep(4)

        return matches
    
    def send_intro_message(self, match):
        """Sends an introductory message to a specific match. 
        
        Parameters
        ----------
            match : Match
                A Match object for the new, unmessaged Tinder match that we are interested in
                sending an introductory message to. This object contains the match's Chat ID,
                name, age, work, place of study, location of home, gender, Tinder bio,
                relationship preference, distance from you, and passions. 
        """
        if not self.is_chat_opened(match.get_chat_id()):
            self.open_chat(match.get_chat_id())

        # locate the textbox and send message
        try:
            message = self.create_message(match)
            
            print(f'Attempting to send "{message}"...')
            xpath = '//textarea'
            time.sleep(5)

            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,xpath)))

            textbox = self.driver.find_element(By.XPATH, xpath)
            textbox.send_keys(message)
            #textbox.send_keys(Keys.ENTER) # this line sends the message which we don't actually want to do

            print("Message sent succesfully.\n".format(message))

            # sleep so message can be sent
            time.sleep(1.5)
        except Exception as e:
            print("SOMETHING WENT WRONG LOCATING TEXTBOX")
            print(e)
    
    def create_message(self, match):
        """Creates an introductory message for a specific Tinder match that is new and has
        not been messaged yet.
        
        Returns
        -------
            match : Match
                A Match object for the new, unmessaged Tinder match that we are interested in
                writing an introductory message for. This object contains the match's Chat ID,
                name, age, work, place of study, location of home, gender, Tinder bio,
                relationship preference, distance from you, and passions. 
        """
        # Format the match's list of passions as a comma separated string with 'and' between the
        # last two passions (e.g., ['Sushi', 'Tennis', 'Running'] --> 'Sushi, Tennis, and Running')
        passions = match.get_passions()
        last_passion = passions[-1]
        other_passions = ", ".join(str(x) for x in passions[:-1])
        formatted_passions = f"{other_passions} and {last_passion}"
        
        # Build Gemini prompt to write introductory message
        prompt = f"""Task: Write an introductory message to a girl named {match.get_name()} that I met on a dating app.

Context: {match.get_name()} is a {match.get_age()}-year-old girl that lives in Boston. She is passionate about {formatted_passions}.

Examples:
- For a 21-year-old girl from Boston named Maria that is passionate about Tennis -> "Tennis this weekend? I can pick you up."
- For a 19-year-old girl from Boston named Jenna that is passionate about painting and sushi -> "How about we show each other our favorite paintings at the MFA and then I buy you some sushi at a great spot across the street?
- For a 22-year-old girl from Boston named Maya that is passionate about ramen -> "Ramen date on me?"

Format: A concise 1-2 sentence text message with no exclamation points. Do not include bracketed text  like "[sushi restaurant near you]" or “[Rock climbing gym in Boston]”; instead, provide real  locations in Boston in your message."""
        
        # Send a request to the Google Gemini API
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
        headers = { 
            "Content-Type": "application/json", 
            "x-goog-api-key": api_key 
        }
        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    def get_chat_ids(self):
        """Clicks into the 'Matches' tab on Tinder to see new matches and then scrapes the Chat ID
        associated with each match. These Chat IDs act as unique identifiers for each match on Tinder.
        
        Returns
        -------
            chatids : list
                A list containing the Chat IDs of the new matches.
        """
        chatids = []

        # Wait until tabs in left sidebar have loaded so that we can click into the new matches.
        try:
            xpath = '//button[@role="tab"]'
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print("Match tab could not be found, trying again")
            self.driver.get(self.HOME_URL)
            time.sleep(1)
            return self.get_chat_ids(new, messaged)

        tabs = self.driver.find_elements(By.XPATH, xpath)

        # Make sure in 'matches' tab instead of 'messaged' because we only message new messages that haven't
        # been messaged yet.
        for tab in tabs:
            if tab.text == 'Matches':
                try:
                    print('Clicked into Matches tab')
                    tab.click()
                except:
                    self.driver.get(self.HOME_URL)
                    return self.get_chat_ids()


        # Scrape chat IDs for new matches. 
        try:
            xpath = '//div[@role="tabpanel"]'
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

            div = self.driver.find_element(By.XPATH, xpath)
            
            list_refs = div.find_elements(By.XPATH, '//*[@id="u-2072757490"]/ul/li/a')
            for index in range(len(list_refs)):
                try:
                    ref = list_refs[index].get_attribute('href')
                    if "likes-you" in ref or "my-likes" in ref:
                        continue
                    else:
                        chatids.append(ref.split('/')[-1])
                except:
                    continue

        except NoSuchElementException:
            pass

        return chatids
    
    def get_match(self, chatid):
        """Extracts all of the important information for a match (e.g., name, age, bio,
        passions, etc.) using its Chat ID.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose information we would like to scrape. 
        
        Returns
        -------
            Match
                A Match object for the match with the passed in Chat ID. This object contains the
                match's Chat ID, name, age, work, place of study, location of home, gender, Tinder
                bio, relationship preference, distance from you, and passions. 
        """
        if not self.is_chat_opened(chatid):
            self.open_chat(chatid)
            
        name = self.get_name(chatid)
        age = self.get_age(chatid)
        bio = self.get_bio(chatid)
        looking_for = self.get_looking_for(chatid)

        rowdata = self.get_row_data(chatid)
        work = rowdata.get('work')
        study = rowdata.get('study')
        home = rowdata.get('home')
        gender = rowdata.get('gender')
        distance = rowdata.get('distance')

        passions = self.get_passions(chatid)

        return Match(name=name, chatid=chatid, age=age, work=work, study=study, home=home, 
                     gender=gender, distance=distance, bio=bio, looking_for=looking_for, passions=passions)
    
    def open_chat(self, chatid):
        """Opens the 'Chat Page' for the match with the passed in Chat ID. The 'Chat Page' consists
        of a message box to communicate with the match as well as the match's profile. From the
        'Chat Page', we can scrape all necessary information from the match's profile. 
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose 'Chat Page' we would like to open. 
        """
        if self.is_chat_opened(chatid):
            return

        href = f'/app/messages/{chatid}'

#         # Find the match with the passed in chatid. First check if the match has already been messaged. 
#         try:
#             xpath = '//*[@role="tab"]'
#             WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

#             tabs = self.driver.find_elements(By.XPATH, xpath)
#             for tab in tabs:
#                 if tab.text == "Messages":
#                     tab.click()
#             time.sleep(1)
#         except Exception as e:
#             self.driver.get(self.HOME_URL)
#             print(e)
#             return self.open_chat(chatid)

#         try:
#             match_button = self.driver.find_element(By.XPATH, '//a[@href="{}"]'.format(href))
#             self.driver.execute_script("arguments[0].click();", match_button)
#             print('Found in message tab')

#         except Exception as e:

        # Check if match is new, not yet messaged. 
        xpath = '//*[@role="tab"]'
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))

        tabs = self.driver.find_elements(By.XPATH, xpath)
        for tab in tabs:
            if tab.text == "Matches":
                tab.click()
        time.sleep(1)

        try:
            matched_button = self.driver.find_element(By.XPATH, '//a[@href="{}"]'.format(href))
            matched_button.click()
        except Exception as e:
            print(e)
        time.sleep(1)
        
    def is_chat_opened(self, chatid):
        """Verifies if the 'Chat Page' for the match with the passed in Chat ID is currently opened in
        the Chrome driver.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose 'Chat Page' we want verify is opened.
        
        Returns
        -------
            bool
                True if the 'Chat Page' for the match with the passed in Chat ID is currently opened
                and False otherwise.
        """
        if chatid in self.driver.current_url:
            return True
        else:
            return False
    
    def get_name(self, chatid):
        """Provided the Chat ID of a specific match, scrapes the match's name from the match's 'Chat Page'.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose name we would like to scrape. 
        
        Returns
        -------
            name : str
                The name of the match with the passed in Chat ID.
        """
        if not self.is_chat_opened(chatid):
            self.open_chat(chatid)

        try:
            xpath = '//*[@id="u-1419960890"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div/h1'
            element = self.driver.find_element(By.XPATH, xpath)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            name = element.text
            return name
        except Exception as e:
            print(e)

    def get_age(self, chatid):
        """Provided the Chat ID of a specific match, scrapes the match's age from the match's 'Chat Page'.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose age we would like to scrape. 
        
        Returns
        -------
            age : int
                The age of the match with the passed in Chat ID.
        """
        if not self.is_chat_opened(chatid):
            self.open_chat(chatid)

        age = None

        try:
            xpath = '//*[@id="u-1419960890"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/span'
            element = self.driver.find_element(By.XPATH, xpath)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, xpath)))
            try:
               age = int(element.text)
            except ValueError:
                age = None
        except:
            pass

        return age
    
    def get_passions(self, chatid):
        """Provided the Chat ID of a specific match, scrapes the match's passions from the match's 'Chat Page'.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose passions we would like to scrape. 
        
        Returns
        -------
            passions : list
                The list of passions for the match with the passed in Chat ID.
        """
        if not self.is_chat_opened(chatid):
            self.open_chat(chatid)
        
        passions = []
        
        # Identify the section for 'Passions' in the match's profile, so that we don't accidentally grab
        # information from the 'Lifestyle' or 'Basics' sections of the match's profile.
        passions_xpath = '//h2[contains(text(), "Passions")]'
        parent_xpath = "./.."
        passions_section = self.driver.find_element(By.XPATH, passions_xpath).find_element(By.XPATH, parent_xpath)

        # Following sibling selector - find the match's passions in the 'Passions' section.
        elements = passions_section.find_elements(By.XPATH, ".//div/div/div[position() >= 1]")
        for el in elements:
            passions.append(el.text)

        return passions

    def get_bio(self, chatid):
        """Provided the Chat ID of a specific match, scrapes the match's Tinder bio from the match's 'Chat Page'.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose Tinder bio we would like to scrape. 
        
        Returns
        -------
            bio : str
                The Tinder bio of the match with the passed in Chat ID.
        """
        if not self.is_chat_opened(chatid):
            self.open_chat(chatid)

        try:
            xpath = '//*[@id="u-1419960890"]/div/div[1]/div/main/div[1]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div'
            bio = self.driver.find_element(By.XPATH, xpath).text
            if 'Looking for\n' in bio:
                return None
            else:
                return bio
        except:
            return None
    
    def get_looking_for(self, chatid):
        """Provided the Chat ID of a specific match, scrapes the match's relationship preference from the
        match's 'Chat Page'.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose relationship preference we would like to scrape.
        
        Returns
        -------
            str
                The relationship preference of the match with the passed in Chat ID.
        """
        if not self.is_chat_opened(chatid):
            self.open_chat(chatid)
        try:
            # The 'Bio' and 'Looking For' values can switch places depending on if the match includes a bio.
            xpath = '//*[@id="de_29_2"]/div/div[2] | //*[@id="de_29_3"]/div/div[2]'
            possibilities = self.driver.find_elements(By.XPATH, xpath)
            for possibility in possibilities:
                if 'Looking for\n' in possibility.text:
                    return possibility.text
            return None
        except:
            return None
    
    _WORK_SVG_PATH = "M7.15 3.434h5.7V1.452a.728.728 0 0 0-.724-.732H7.874a.737.737 0 0 0-.725.732v1.982z"
    _STUDYING_SVG_PATH = "M11.87 5.026L2.186 9.242c-.25.116-.25.589 0 .705l.474.204v2.622a.78.78 0 0 0-.344.657c0 .42.313.767.69.767.378 0 .692-.348.692-.767a.78.78 0 0 0-.345-.657v-2.322l2.097.921a.42.42 0 0 0-.022.144v3.83c0 .45.27.801.626 1.101.358.302.842.572 1.428.804 1.172.46 2.755.776 4.516.776 1.763 0 3.346-.317 4.518-.777.586-.23 1.07-.501 1.428-.803.355-.3.626-.65.626-1.1v-3.83a.456.456 0 0 0-.022-.145l3.264-1.425c.25-.116.25-.59 0-.705L12.13 5.025c-.082-.046-.22-.017-.26 0v.001zm.13.767l8.743 3.804L12 13.392 3.257 9.599l8.742-3.806zm-5.88 5.865l5.75 2.502a.319.319 0 0 0 .26 0l5.75-2.502v3.687c0 .077-.087.262-.358.491-.372.29-.788.52-1.232.68-1.078.426-2.604.743-4.29.743s-3.212-.317-4.29-.742c-.444-.161-.86-.39-1.232-.68-.273-.23-.358-.415-.358-.492v-3.687z"
    _HOME_SVG_PATH = "M19.695 9.518H4.427V21.15h15.268V9.52zM3.109 9.482h17.933L12.06 3.709 3.11 9.482z"
    _LOCATION_SVG_PATH = "M11.436 21.17l-.185-.165a35.36 35.36 0 0 1-3.615-3.801C5.222 14.244 4 11.658 4 9.524 4 5.305 7.267 2 11.436 2c4.168 0 7.437 3.305 7.437 7.524 0 4.903-6.953 11.214-7.237 11.48l-.2.167zm0-18.683c-3.869 0-6.9 3.091-6.9 7.037 0 4.401 5.771 9.927 6.897 10.972 1.12-1.054 6.902-6.694 6.902-10.95.001-3.968-3.03-7.059-6.9-7.059h.001z"
    _LOCATION_SVG_PATH_2 = "M11.445 12.5a2.945 2.945 0 0 1-2.721-1.855 3.04 3.04 0 0 1 .641-3.269 2.905 2.905 0 0 1 3.213-.645 3.003 3.003 0 0 1 1.813 2.776c-.006 1.653-1.322 2.991-2.946 2.993zm0-5.544c-1.378 0-2.496 1.139-2.498 2.542 0 1.404 1.115 2.544 2.495 2.546a2.52 2.52 0 0 0 2.502-2.535 2.527 2.527 0 0 0-2.499-2.545v-.008z"
    _GENDER_SVG_PATH = "M15.507 13.032c1.14-.952 1.862-2.656 1.862-5.592C17.37 4.436 14.9 2 11.855 2 8.81 2 6.34 4.436 6.34 7.44c0 3.07.786 4.8 2.02 5.726-2.586 1.768-5.054 4.62-4.18 6.204 1.88 3.406 14.28 3.606 15.726 0 .686-1.71-1.828-4.608-4.4-6.338"
    def get_row_data(self, chatid):
        """Provided the Chat ID of a specific match, scrapes the match's work, place of study,
        location of home, gender, and distance from you from the match's 'Chat Page'.
        
        Parameters
        ----------
            chatid : str
                The Chat ID of the match whose information we would like to scrape.
        
        Returns
        -------
            rowdata : dict
                A dictionary containing the work, place of study, location of home, gender, and
                distance from you for the match with the passed in Chat ID.
        """
        if not self.is_chat_opened(chatid):
            self.open_chat(chatid)

        rowdata = {}

        xpath = '//div[@class="Row"]'
        rows = self.driver.find_elements(By.XPATH, xpath)

        for row in rows:
            svg = row.find_element(By.XPATH, ".//*[starts-with(@d, 'M')]").get_attribute('d')
            value = row.find_element(By.XPATH, ".//div[2]").text
            if svg == self._WORK_SVG_PATH:
                rowdata['work'] = value
            if svg == self._STUDYING_SVG_PATH:
                rowdata['study'] = value
            if svg == self._HOME_SVG_PATH:
                rowdata['home'] = value.split(' ')[-1]
            if svg == self._GENDER_SVG_PATH:
                rowdata['gender'] = value
            if svg == self._LOCATION_SVG_PATH or svg == self._LOCATION_SVG_PATH_2:
                distance = value.split(' ')[0]
                try:
                    distance = int(distance)
                except TypeError:
                    # Means the text has a value of 'Less than 1 km away'
                    distance = 1
                except ValueError:
                    distance = None

                rowdata['distance'] = distance

        return rowdata
    
    def handle_potential_popups(self):
        """Defines the logic to handle pop ups that appear while scraping information from your matches. This
        includes declining a pop up that asks if you want to 'See Who Likes You' and closing a pop up
        advertising 'Tinder Web Exclusive'.
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
            xpath = '//*[@id="u-1419960890"]/div/div[1]/div/main/div[1]/div/button'
            close_tinder_web_exclusive_button = self.driver.find_element('xpath', xpath)
            close_tinder_web_exclusive_button.click()
            print('Closed Tinder Web Exclusive pop up')
            time.sleep(3)
            self.handle_potential_popups()
        except:
            pass