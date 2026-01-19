from scraper_class import Scraper
import asyncio


scraper = Scraper("seraphon")

list_of_units = [
    "Skink",
    "Saruas",
    "Saruas Oldblood",
    "Skink Oracle on Trogolodon",
    "Skink Starpriest",
    "Skink Starseer",
    "Kroxigor",
    "Kroxigor",
    "Sauruas Astrolith Starbearer",
    "Hunters of Hunachi Starstone Bollas",
    "Hunters of Hunachi Dartpipes",
    "Spawn of Chotec",
    "Bastiladon",
    "Lord Kroak"
]

"""
scraper = Scraper("cities of sigmar")

list_of_units = [
    "Freeguild Fusiliers",
    "Dreadlord on Black Dragon",
    "Freeguild Command Corps",
    "The Steel Rook",
    "Freeguild Steelhelms",
    "Freeguild Cavalier-Marshal",
    "Freeguild Cavaliers",
    "Alchemite Warforger",
    "Battlemage",
    "Battlemage on Griffon",
    "Freeguild Marshal on Griffon",
    "Ironweld Great Cannon",
    "Ironweld Volley Gun",
    "Fusil-Major on Ogor Warhulk",
    "Pontifex Zenestra, Matriarch of the Great Wheel",
    "Dark Riders",
    "Drakespawn Knights",
    "Black Guard",
    "Sorceress"
]
"""

for unit in list_of_units:
    x = scraper.collect_points(scraper.scrape(unit))
    if x == 0:
        y = scraper.collect_points_name_retry(unit)
        if y[0] == 0:
            print(f"Issue with {y[1]}!!!")
        else:
            print(f"Did you mean {y[1]}? they're worth {y[0]} points!")
    else:
        print(f"{unit} is worth {x} points!")
