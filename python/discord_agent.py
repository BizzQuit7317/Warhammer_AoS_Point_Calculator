class Agent():
    def __init__(self):
        self.faction = None #None by default
        self.factions_list = [ #A list of all faction from wahapedia to ominimise mistakes
    "Cities of Sigmar",
    "Daughters of Khaine",
    "Fyreslayers",
    "Idoneth Deepkin",
    "Kharadron Overlords",
    "Lumineth Realm-lords",
    "Seraphon",
    "Stormcast Eternals",
    "Sylvaneth",
    "Beasts of Chaos",
    "Blades of Khorne",
    "Disciples of Tzeentch",
    "Hedonites of Slaanesh",
    "Helsmiths of Hashut",
    "Maggotkin of Nurgle",
    "Skaven",
    "Slaves to Darkness",
    "Flesh-eater Courts",
    "Nighthaunt",
    "Ossiarch Bonereapers",
    "Soulblight Gravelords",
    "Bonesplitterz",
    "Gloomspite Gitz",
    "Ironjawz",
    "Kruleboyz",
    "Ogor Mawtribes",
    "Sons of Behemat",
    "Endless Spells",
]
        self.current_army_list = []
        self.current_army_points = 0
