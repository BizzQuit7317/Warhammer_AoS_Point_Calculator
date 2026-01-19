import requests, functions as tf

base_url = "https://wahapedia.ru/aos4/factions/" #https://wahapedia.ru/aos4/factions/seraphon/Spawn-of-Chotec

faction = "seraphon" #Input from user
unit = "spawn of chotec" #Input from user

unit_formated = tf.format_user_unit_input(unit)

full_url = f"{base_url}/{faction.lower()}/{unit_formated}"

html = requests.request("GET", full_url)

print(html.status_code)
print(html.text.split("Points")[1][:17])
