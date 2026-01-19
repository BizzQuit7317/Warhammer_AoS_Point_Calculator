# Warhammer_AoS_Point_Calculator
Powered by wahapedia, a simple script to scrape the html of the page and return the points for a unit.

# To Do:
- Implement some simple checking on names that return a 404, potentially just adding an s or something
- Connect to csv so I can check result and have a better view of data when debuggin
- Connect to discord bot for test
- Make discord bot function (no idea what that entails)

# Ideas:
when retrying names I want 2 methods, first keeping a track of like common mispellings, things like users writing skink when its listed as skink**S**.
depending on efficency and data storage might noot be feasable.
Trying common mistakes, if this works well might not need first, but again trying to pluralise things or adding with or something other spot, 
this will be more limited by time retrying ssomething, could use async function to send multiple retry requests or for multi unit lists then have it re roll on units it cannot find.

# Info
- Discord bot name: AoS_Wahapedia_Scraper
