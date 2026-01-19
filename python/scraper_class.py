import requests

class Scraper():
    def __init__(self, faction):
        self.base_url = "https://wahapedia.ru/aos4/factions/" #Default wahapedia url, totally powered by them the real mvp
        self.faction = self.format_user_input(faction, False).lower()

    def format_user_input(self, unit_raw: str, unit_switch: bool) -> str:
        """
        The unit switch is for the faction name which need to be hyphenated but kept lower case

        """
        unit_split = unit_raw.split(" ")
        unit_formatted_buffer = []

        if unit_switch:
            for word in unit_split:
                if len(word) > 2: # 2 to parse any words like "it" and "of" to keep them lower case
                    word = word.capitalize()
                else:
                    word = word.lower()
                unit_formatted_buffer.append(word)
        else:
            for word in unit_split:
                word = word.lower() #No need to check length everything needs to be lower
                unit_formatted_buffer.append(word)

        unit_formatted = "-".join(unit_formatted_buffer)
        return unit_formatted
    
    def scrape(self, unit):
        unit_formated = self.format_user_input(unit, True)

        full_url = f"{self.base_url}/{self.faction}/{unit_formated}"

        html = requests.request("GET", full_url)

        print(f"checking for faction: {self.faction}\nunit: {unit_formated}")
        print(html.status_code)
        try:
            print(html.text.split("Points")[1][:17])
        except:
            print("Could not find page for this unit need some form of sugggestion feature")
        print("######################################################################")
        """
        Specifically looking for unit points so splitting on that word, the raw html has the raw points value in a <br> after the tag holding "Points", thats why we take the second [1] block, needs to be tested to make sure there wont be another break at points.
        [:17] is currently just to test to see how consitent it is picking up the first charecter
        """
