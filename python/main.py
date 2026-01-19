from scraper_class import Scraper

"""
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

    # Additional Cities of Sigmar units
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


for unit in list_of_units:
    scraper.scrape(unit)

print("~~~~~~~~~~~~~~~~~~~~~\n|\n| Finished running!! |\n|\n~~~~~~~~~~~~~~~~~~~~~")
