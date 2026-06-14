FLAGS = [
    # Easy
    {"name": "United States",  "code": "us", "difficulty": "easy"},
    {"name": "United Kingdom", "code": "gb", "difficulty": "easy"},
    {"name": "France",         "code": "fr", "difficulty": "easy"},
    {"name": "Germany",        "code": "de", "difficulty": "easy"},
    {"name": "Japan",          "code": "jp", "difficulty": "easy"},
    {"name": "Canada",         "code": "ca", "difficulty": "easy"},
    {"name": "Brazil",         "code": "br", "difficulty": "easy"},
    {"name": "Australia",      "code": "au", "difficulty": "easy"},
    {"name": "China",          "code": "cn", "difficulty": "easy"},
    {"name": "India",          "code": "in", "difficulty": "easy"},
    # Hard
    {"name": "Sweden",         "code": "se", "difficulty": "hard"},
    {"name": "Norway",         "code": "no", "difficulty": "hard"},
    {"name": "Portugal",       "code": "pt", "difficulty": "hard"},
    {"name": "Argentina",      "code": "ar", "difficulty": "hard"},
    {"name": "South Korea",    "code": "kr", "difficulty": "hard"},
    {"name": "Egypt",          "code": "eg", "difficulty": "hard"},
    {"name": "Mexico",         "code": "mx", "difficulty": "hard"},
    {"name": "Thailand",       "code": "th", "difficulty": "hard"},
    {"name": "Netherlands",    "code": "nl", "difficulty": "hard"},
    {"name": "Switzerland",    "code": "ch", "difficulty": "hard"},
    # Impossible
    {"name": "Bhutan",         "code": "bt", "difficulty": "impossible"},
    {"name": "Eritrea",        "code": "er", "difficulty": "impossible"},
    {"name": "Maldives",       "code": "mv", "difficulty": "impossible"},
    {"name": "Burkina Faso",   "code": "bf", "difficulty": "impossible"},
    {"name": "Kyrgyzstan",     "code": "kg", "difficulty": "impossible"},
    {"name": "Comoros",        "code": "km", "difficulty": "impossible"},
    {"name": "Vanuatu",        "code": "vu", "difficulty": "impossible"},
    {"name": "Tuvalu",         "code": "tv", "difficulty": "impossible"},
    {"name": "Andorra",        "code": "ad", "difficulty": "impossible"},
    {"name": "Lesotho",        "code": "ls", "difficulty": "impossible"},
]

BY_DIFFICULTY = {
    "easy":       [f for f in FLAGS if f["difficulty"] == "easy"],
    "hard":       [f for f in FLAGS if f["difficulty"] == "hard"],
    "impossible": [f for f in FLAGS if f["difficulty"] == "impossible"],
}

ROUNDS = 7
TIMER_SECONDS = 15
BASE_POINTS = 1000
SPEED_BONUS_MAX = 500
