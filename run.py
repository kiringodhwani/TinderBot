from open_login_tinder import OpenLoginTinder
from auto_swipe import AutoSwipe
from match_analyzer import MatchAnalyzer
from time import sleep

# Open and Log in to Tinder
print('Start Opening and Logging into Tinder')
OpenLoginTinder = OpenLoginTinder()
driver = OpenLoginTinder.open_login_tinder()
print('Opened and Logged into Tinder')

# # Auto Swipe
# print('Start Autoswiping')
# AutoSwipe = AutoSwipe(driver=driver)
# AutoSwipe.auto_swipe(number_to_like=50, ratio=0.7)
# print('Done Autoswiping')
# sleep(10)

# Analyze Matches
sleep(20)
MatchAnalyzer = MatchAnalyzer(driver=driver)
new_matches = MatchAnalyzer.get_all_new_matches()
for new_match in new_matches:
    print(new_match.get_dictionary())
    print()