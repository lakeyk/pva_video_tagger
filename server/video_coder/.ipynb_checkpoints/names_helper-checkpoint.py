# names_helper.py

INITIALS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "em", "s", "ES", "SES", "mm"]
names_dict = {}

def get_names_dict():
    if len(names_dict) == 0:
        init_names_dict()
    return names_dict

# TODO: Move this to a config file
def init_names_dict():
    # Camp 1 only
    names_dict["Adrian"] = ["Adrian", "Adrieene", "Adrien"]
    names_dict["Caman"] = ["Caman", "Canaan", "Cannon", "Cayman", "Kaman"]
    names_dict["Charlie"] = ["Charlie"]
    names_dict["Drake"] = ["Drake", "rake", "Dreak"]
    names_dict["Griffin"] = ["Griffin", "Gryffin", "Gryfin", "Grifin"]
    names_dict["Jakey"] = ["Jakey", "Jake", "Jackie"]
    names_dict["Luke"] = ["Luke", "luck", "luke", "look"]
    names_dict["Tommy"] = ["Tommy", "Tommie"]
    
    # Both camps
    names_dict["Ari"] = ["Ariana", "Arieane", "Arriana", "Arianna", "Ari", "Are", "Ari's"]
    names_dict["Bella"] = ["Bella"]
    names_dict["Boone"] = ["Boone", "Boon", "Boom", "boon", "boom", "spoon", "phone", "food"]
    names_dict["Carl"] = ["Carl", "Karl"]
    names_dict["Carter"] = ["Carter", "Karter", "Carter's"]
    names_dict["Eugenie"] = ["Eugenie", "Yougenie", "Genie", "Eugene", "Janine", "Eugenia"]
    names_dict["Jacob"] = ["Jacob", "Jakob", "jacob"]
    names_dict["Kalea"] = ["Kalea", "Kalaya", "Calaya", "kelea", "kalea", "Kalia", "kaleia", "play", "paleo", "Playa"]
    names_dict["Koda"] = ["Koda", "Coda", "cola", "coda", "code", "Code", "Toto", "Cota"]
    names_dict["Paloma"] = ["Paloma", "Pamona", "Paloama", "Baloma", "polona", "Palomo"]
    names_dict["Pasha"] = ["Pasha", "Pash", "pasha", "Tasha"]
    names_dict["Peyton"] = ["Peyton", "Payton", "Peytan", "Paytan"]
    names_dict["Sean"] = ["Sean", "Shawn", "Shawna"]
    names_dict["Shane"] = ["Shane"]
    names_dict["Will"] = ["William", "Williams", "Will", "will"]
    names_dict["Zoe"] = ["Zoe", "Zoe's", "Joey"]
    
    # Camp 2 only
    names_dict["Allie"] = ["Allie", "Ally", "Aletheia", "Alethia", "Alexia", "Alethea", "Aleythea", "Alessia", "Ali"]
    names_dict["Alex"] = ["Alex", "Alyx"]
    names_dict["Andrew"] = ["Andrew"]
    names_dict["Audrey"] = ["Audrey", "Audry"]
    names_dict["Avery"] = ["Avery"]
    names_dict["Caleb"] = ["Caleb", "Kaleb", "Kayleb", "Cayleb"]
    names_dict["Cayden"] = ["Cayden", "Kayden", "Caden", "Kaden"]
    names_dict["Cristina"] = ["Cristina", "Christina", "Kristina"]
    names_dict["Dan"] = ["Dan", "Dann", "Stan"]
    names_dict["Frank"] = ["Frank"]
    names_dict["Harald"] = ["Harald", "Harold"]
    names_dict["Harper"] = ["Harper", "Harper's"]
    names_dict["Harrison"] = ["Harrison", "Harison"]
    names_dict["Holt"] = ["Holt", "holt", "hope"]
    names_dict["Jay"] = ["Jay", "Jaya"]
    names_dict["Kyra"] = ["Kyra", "Kira", "Kiera", "Keira"]
    names_dict["Lila"] = ["Lila", "Lilah", "Leia", "Twila"]
    names_dict["Maddie"] = ["Maddie", "Maddy"]
    names_dict["Norah"] = ["Norah", "Nora", "Dora's"]
    names_dict["Oliver"] = ["Oliver"]
    names_dict["Pernille"] = ["Pernille", "Pernelly", "pernelly", "pernilla", "Cornella", "Panela"]
    names_dict["Peter"] = ["Peter", "heater"]
    names_dict["Piper"] = ["Piper", "piper"]
    names_dict["Ramsey"] = ["Ramsey", "Ramsy"]
    names_dict["Rick"] = ["Rick"]
    names_dict["Rylee"] = ["Rylee", "Ryleigh", "Riley", "Reilly", "Kylie"]
    names_dict["Sasha"] = ["Sasha"]
    names_dict["Soren"] = ["Soren", "Soaren", "Soarin", "Sauron", "Sorens", "Soerens"]
    names_dict["Spencer"] = ["Spencer", "Spenser", "Spencer's"]
    names_dict["Sydney"] = ["Sydney", "Sidney"]
    names_dict["Thor"] = ["Thor", "thor", "Thore", "thore", "door", "store", "Thorin"]
    names_dict["Violet"] = ["Violet", "violet", "Violette"]
    names_dict["Willa"] = ["Willa"]
    
    # Duplicate Names
    names_dict["HenryM"] = ["Henry M", "Henry em", "Henery M", "Henery em", "Henry Merritt", "Henry Merrik", "Henry mm"]
    names_dict["HenryS"] = ["Henry S", "Henery S", "Henery es", "Henry es"]
    names_dict["HenryL"] = ["Henry L", "Henry ell", "Henery L", "Henery ell"]
    names_dict["Henry"] = ["Henry"]
    names_dict["Zach"] = ["Zach"]
    names_dict["Zachary"] = ["Zachary", "Zachary Z"]
    names_dict["ZacharyS"] = ["Zachary S", "Zackary S", "Zachary es", "Zachary ES", "Zachary s", "Zackary es", "Zackary ES", "Zackary s", "jackass", "Zach SES"]

    names_dict["Ellie"] = ["Ellie"]
    names_dict["Nicole"] = ["Nicole"]
    names_dict["Noel"] = ["Noel", "no"]

    return names_dict