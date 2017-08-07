import copy
import re

TOTAL_GAME_PHASES = 2

CYLON_LEADER_CHARACTERS = {
    "caprica", "doral", "biers", "cavil", # pegasus
    "o'neil", "athena" # daybreak
}
NON_CYLON_LEADER_CHARACTERS = {
    "adama", "s tigh", "boomer", "apollo", "starbuck", "chief", "zarek", "baltar", "roslin",     # original
    "cain", "helo", "dee", "kat", "e tigh", # pegasus
    "gaeta", "anders", "cally", "foster",   # exodus
    "hoshi", "hot dog", "doc", "helo a", "apollo a", "zarek a", "baltar a", "lampkin"  # daybreak
}

CHARACTER_NAME_EQUIVALENCE = {
    "w adama": "adama", "william adama": "adama", "william": "adama", 
	"saul": "s tigh", "saul tigh": "s tigh", 
	"s valerii": "boomer", "sharon valerii": "boomer", "valerii": "boomer", 
	"l adama": "apollo", "lee adama": "apollo", "lee": "apollo", 
	"k thrace": "starbuck", "kara thrace": "starbuck", "kara": "starbuck", "thrace": "starbuck", 
	"g tyrol": "chief", "galen tyrol": "chief", "galen": "chief", 
	"t zarek": "zarek", "tom zarek": "zarek", "tom": "zarek", 
	"g baltar": "baltar", "gaius baltar": "balter", "gauis": "balter", 
	"l roslin": "roslin", "laura roslin": "roslin", "laura": "roslin", 
	# original
    "h cain": "cain", "helena cain": "cain", "helena": "cain", 
	"k agathon": "helo", "karl agathon": "helo", "karl": "helo",
	"a dualla": "dee", "anastasia dualla": "dee", "anastasia": "dee", "dualla": "dee", 
	"l katraine": "kat", "louanna katraine": "kat", "louanna": "kat", "katraine": "kat", 
	"ellen tigh": "e tigh", "ellen": "e tigh", 
	"j cavil": "cavil", "john cavil": "cavil", "john": "cavil", "1": "cavil", 
	"l condy": "condy", "leoben condy": "condy", "2": "condy", 
	"d biers": "biers", "d'anna biers": "biers", "d'anna": "biers", "3": "biers", 
	"a doral": "doral", "aaron doral": "doral", "aaron": "doral", "5": "doral", 
	"c six": "caprica", "caprica six": "caprica", "six": "caprica", "6": "caprica", 
	# pegasus
    "f gaeta": "gaeta", "felix gaeta": "gaeta", "felix": "gaeta", 
	"s anders": "anders", "samuel anders": "anders", 
	"c Tyrol": "cally", "Callandra Tyrol": "cally", "Callandra": "cally", 
	"t foster": "foster", "tory foster": "foster", "tory": "foster", 
    # exodus
    "l hoshi": "hoshi", "louis hoshi": "hoshi", "louis": "hoshi", 
	"b costanza": "hot dog", "brendan costanza": "hot dog", "brendan": "hot dog", "costanza": "hot dog", 
	"s cottle": "doc", "sherman cottle": "doc", "sherman": "doc", "cottle": "doc", "doc cottle": "doc", 
	"k agathon a": "helo a", "karl agathon a": "helo a", "karl a": "helo a",
	"l adama a": "apollo a", "lee adama a": "apollo a", "lee a": "apollo a",
	"t zarek a": "zarek a", "tom zarek a": "zarek a", "tom a": "zarek a", 
	"g baltar a": "baltar a", "gaius baltar a": "baltar a", "gaius a": "baltar a", 
	"r lampkin": "lampkin", "romo lampkin": "lampkin", "romo": "lampkin", 
	"s o'neil": "o'neil", "simon o'neil": "o'neil", "simon": "o'neil", "simon": "o'neil", "4": "o'neil", 
	"s agathon": "athena", "sharon agathon": "athena", "8": "athena", 
    # daybreak
}

class Character:
    def __init__(self, character, loyalty, phase=None):
        if character in CHARACTER_NAME_EQUIVALENCE:
            character = CHARACTER_NAME_EQUIVALENCE[character]

        self.character = character
        self.loyalty = loyalty
        self.phase = phase

        assert character in CYLON_LEADER_CHARACTERS or character in NON_CYLON_LEADER_CHARACTERS, "character %s not recognized" % character
        if loyalty != "cylon_leader":
            assert character in NON_CYLON_LEADER_CHARACTERS, "character %s is a cylon leader" % character


def verify_character_change_path(name, characters):
    # hey look its a state machine!

    # legal moves:
    #   human => cylon (doesn't change character)
    #   human => cylon_leader (doesn't change character) note that cylon leaders can play as any character but humans/cylons cannot play as cylon leaders
    #   cylon => cylon
    #   human => human
    #   cylon_leader => cylon_leader


    became_cylon = False

    loyalty_string = ""
    for character in characters:
        if character.loyalty == "cylon_leader":
            loyalty_string += "L"
        elif character.loyalty == "human":
            loyalty_string += "h"
        elif character.loyalty == "cylon":
            loyalty_string += "c"
    
    assert re.match("(^h*c*$)|(^h*L*$)", loyalty_string), "player %(player)s's loyalty changes are illegal (%(loyalty_string)s)" % {"player": name, "loyalty_string": loyalty_string}


class Player:
    def __init__(self, name, characters_info):
        """constructs a player object. if fewer than TOTAL_GAME_PHASES characters passed in, automatically generates new characters""", 
        """also verifies some things about player object""", 
        assert len(characters_info) > 0, "player %s must play as at least one character" % name

        characters = []
        for index, character_info in enumerate(characters_info, 1):
            characters.append(Character(character_info["character"], character_info["loyalty"], index))
        while len(characters) < TOTAL_GAME_PHASES:
            new_last_character = copy.deepcopy(characters[-1])
            new_last_character.phase += 1
            characters.append(new_last_character)

        verify_character_change_path(name, characters)

        self.name = name
        self.characters = characters


    def __str__(self):
        output = ["player ", self.name, ":"]
        for character in self.characters:
            output += [" (", character.character, ": ", character.loyalty, ")"]
        return "".join(output)
