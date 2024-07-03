from open_login_tinder import OpenLoginTinder
from auto_swipe import AutoSwipe
from match_analyzer import MatchAnalyzer
from time import sleep

# Open and Log in to Tinder
print('\nStart opening and logging into Tinder...')
OpenLoginTinder = OpenLoginTinder()
driver = OpenLoginTinder.open_login_tinder()
print('Opened and logged into Tinder!\n')

# # Auto Swipe
# print('Start auto-swiping...')
# AutoSwipe = AutoSwipe(driver=driver)
# AutoSwipe.auto_swipe(number_to_like=50, ratio=0.7)
# print('Done auto-swiping!\n')
# sleep(10)

# Analyze Matches
sleep(20)
print('Start analyzing and messaging matches...')
MatchAnalyzer = MatchAnalyzer(driver=driver)
new_matches = MatchAnalyzer.get_all_new_matches()
print('Finished analyzing and messaging matches!\n')