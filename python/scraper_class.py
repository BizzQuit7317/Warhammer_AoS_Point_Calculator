import requests, re

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
    
    def scrape(self, unit) -> str:
        unit_formated = self.format_user_input(unit, True)

        full_url = f"{self.base_url}/{self.faction}/{unit_formated}"

        html = requests.request("GET", full_url)
        return html
    
    def collect_faction_units(self) -> list:
        full_url = f"{self.base_url}/{self.faction}/warscrolls.html"
        raw_html = requests.request("GET", full_url)
    
        snippet = raw_html.text.split("<!--/noindex-->")[1] #Randomly lucky comment I can use to reduce the snippet

        parts = snippet.split('href="#')[1:]
        unit_ids = []

        for part in parts:
            # Grab everything until the closing quote "
            id_name = part.split('"')[0]
            if id_name:
                unit_ids.append(id_name)

        clean_list = [name.replace("-", " ") for name in unit_ids]
        return sorted(list(set(clean_list)))

    def collect_points(self, raw_html: str) -> int:
        try:
            points = list(map(int, re.findall(r"\d+", raw_html.text.split("Points")[1][:19]))) #17 gets us to the first digit, 19 will cover all digits since there are no 4 digit point units in aos
            if len(points) != 1:
                print(f"[DBG] more than 1 set of points found: {points}. Returning first set!")
            return points[0]
        except:
            return 0
    
    def collect_points_name_retry(self, unit_name: str) -> list:
        """
        returns a list to keep track of working unit name
        index 0 -> points
        index 1 -> list of names tried
        will go through a series of checks and potential test
        1. pluralising
        """
        original_name = unit_name # Buffer to keep track of the original name o we can return the latest name used
        names_tried = []

        unit_name_plural = f"{unit_name}s"
        points = self.collect_points(self.scrape(unit_name_plural))

        names_tried.append(unit_name_plural)

        if points != 0:
            return [points, names_tried]
        
        return [0, names_tried]

        
