# names_helper.py

INITIALS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "em", "s", "ES"]
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
    names_dict["Jake"] = ["Jake"]
    names_dict["Luke"] = ["Luke", "luck", "luke", "look"]
    names_dict["Tommy"] = ["Tommy", "Tommie"]
    
    # Both camps
    names_dict["Ariana"] = ["Ariana", "Arieane", "Arriana", "Arianna"]
    names_dict["Bella"] = ["Bella"]
    names_dict["Boone"] = ["Boone", "Boon", "Boom", "boon", "boom"]
    names_dict["Carl"] = ["Carl", "Karl"]
    names_dict["Carter"] = ["Carter", "Karter"]
    names_dict["Eugenie"] = ["Eugenie", "Yougenie", "Genie", "Eugene"]
    names_dict["Jacob"] = ["Jacob", "Jakob"]
    names_dict["Kelea"] = ["Kalea", "Kalaya", "Calaya", "kelea", "kalea"]
    names_dict["Koda"] = ["Koda", "Coda", "cola", "coda", "code", "Code"]
    names_dict["Paloma"] = ["Paloma", "Pamona", "Paloama", "Baloma"]
    names_dict["Pasha"] = ["Pasha", "Pash", "pasha"]
    names_dict["Peyton"] = ["Peyton", "Payton", "Peytan", "Paytan"]
    names_dict["Sean"] = ["Sean", "Shawn", "Shawna"]
    names_dict["Shane"] = ["Shane"]
    names_dict["William"] = ["William", "Williams"]
    names_dict["Zoe"] = ["Zoe", "Zoe's"]
    
    # Camp 2 only
    names_dict["Aletheia"] = ["Aletheia", "Alethia", "Alexia", "Alethea", "Aleythea", "Alessia"]
    names_dict["Alex"] = ["Alex", "Alyx"]
    names_dict["Andrew"] = ["Andrew"]
    names_dict["Audrey"] = ["Audrey", "Audry"]
    names_dict["Avery"] = ["Avery"]
    names_dict["Caleb"] = ["Caleb", "Kaleb", "Kayleb", "Cayleb"]
    names_dict["Cayden"] = ["Cayden", "Kayden", "Caden", "Kaden"]
    names_dict["Cristina"] = ["Cristina", "Christina", "Kristina"]
    names_dict["Dan"] = ["Dan", "Dann"]
    names_dict["Frank"] = ["Frank"]
    names_dict["Harald"] = ["Harald", "Harold"]
    names_dict["Harper"] = ["Harper"]
    names_dict["Harrison"] = ["Harrison", "Harison"]
    names_dict["Holt"] = ["Holt", "holt"]
    names_dict["Jay"] = ["Jay", "Jaya"]
    names_dict["Kyra"] = ["Kyra"]
    names_dict["Lila"] = ["Lila", "Lilah"]
    names_dict["Maddie"] = ["Maddie", "Maddy"]
    names_dict["Norah"] = ["Norah", "Nora"]
    names_dict["Oliver"] = ["Oliver"]
    names_dict["Pernille"] = ["Pernille", "Pernelly", "pernelly"]
    names_dict["Peter"] = ["Peter", "heater"]
    names_dict["Piper"] = ["Piper", "piper"]
    names_dict["Ramsey"] = ["Ramsey", "Ramsy"]
    names_dict["Rick"] = ["Rick"]
    names_dict["Rylee"] = ["Rylee", "Ryleigh", "Riley", "Reilly"]
    names_dict["Sasha"] = ["Sasha"]
    names_dict["Soren"] = ["Soren", "Soaren", "Soarin"]
    names_dict["Spencer"] = ["Spencer", "Spenser"]
    names_dict["Sydney"] = ["Sydney", "Sidney"]
    names_dict["Thor"] = ["Thor", "thor", "Thore", "thore", "door"]
    names_dict["Violet"] = ["Violet", "violet", "Violette"]
    names_dict["Willa"] = ["Willa"]
    
    # Duplicate Names
    names_dict["HenryM"] = ["Henry M", "Henry em", "Henery M", "Henery em"]
    names_dict["HenryS"] = ["Henry S", "Henery S", "Henery es", "Henry es"]
    names_dict["HenryL"] = ["Henry L", "Henry ell", "Henery L", "Henery ell"]
    names_dict["Zach"] = ["Zach"]
    names_dict["Zachary"] = ["Zachary", "Zachary Z"]
    names_dict["ZacharyS"] = ["Zachary S", "Zackary S", "Zachary es", "Zachary ES", "Zachary s", "Zackary es", "Zackary ES", "Zackary s"]

    return names_dict