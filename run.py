from open_login_tinder import OpenLoginTinder
from auto_swipe import AutoSwipe
from match_analyzer import MatchAnalyzer
from time import sleep

# Open and Log in to Tinder
print('\nStart opening and logging into Tinder...')
OpenLoginTinder = OpenLoginTinder()
driver = OpenLoginTinder.open_login_tinder()
print('Opened and logged into Tinder!\n')

# Auto Swipe
number_to_like = 50
print(f'Start auto-swiping to like {number_to_like} profiles...')
AutoSwipe = AutoSwipe(driver=driver)
AutoSwipe.auto_swipe(number_to_like=number_to_like, ratio=0.7)
print('Done auto-swiping!\n')

# # Analyze Matches
# print('Start analyzing and messaging matches...')
# MatchAnalyzer = MatchAnalyzer(driver=driver)
# new_matches = MatchAnalyzer.get_and_message_all_new_matches()
# print('Finished analyzing and messaging matches!\n')