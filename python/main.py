import requests, functions as tf #tf was test function when building

base_url = "https://wahapedia.ru/aos4/factions/" #Default wahapedia url, totally powered by them the real mvp

faction = "seraphon" #Input from user
unit = "spawn of chotec" #Input from user

unit_formated = tf.format_user_unit_input(unit)

full_url = f"{base_url}/{faction.lower()}/{unit_formated}"

html = requests.request("GET", full_url)

print(html.status_code)
print(html.text.split("Points")[1][:17]) 
"""
Specifically looking for unit points so splitting on that word, the raw html has the raw points value in a <br> after the tag holding "Points", thats why we take the second [1] block, needs to be tested to make sure there wont be another break at points.
[:17] is currently just to test to see how consitent it is picking up the first charecter
"""
