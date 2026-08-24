NODE_POSITIONS = {
    "A": (170, 140),
    "B": (120, 210),
    "C": (300, 150),
    "D": (260, 260),
    "E": (520, 200),
    "F": (440, 340),
    "G": (640, 320),
    "H": (500, 430),
    "I": (630, 450),
    "J": (850, 430),
    "K": (780, 540),
    "L": (920, 500),
}

LABELS = {
    "A": "1 No. Gate",
    "B": "Marine Science",
    "C": "Science Faculty",
    "D": "Library",
    "E": "Arts Faculty",
    "F": "IT Building",
    "G": "Social Science Faculty",
    "H": "Sohid Minar",
    "I": "BBA Faculty",
    "J": "IER",
    "K": "Law Faculty",
    "L": "2 No. Gate",
}

ROADS = [
    ("A", "B", 2.8, 5, "Main Access Road"),
    ("A", "C", 3.6, 6, "Academic Road"),
    ("B", "D", 3.2, 6, "Library Lane"),
    ("C", "D", 2.7, 5, "Central Walk"),
    ("C", "E", 4.5, 8, "Arts Link"),
    ("D", "F", 4.0, 7, "IT Corridor"),
    ("E", "F", 3.2, 6, "Arts-IT Road"),
    ("E", "G", 4.1, 7, "Faculty Road"),
    ("F", "H", 3.8, 7, "Central Spine"),
    ("G", "I", 3.5, 6, "Business Road"),
    ("H", "I", 2.9, 5, "Campus Connector"),
    ("I", "J", 4.2, 8, "IER Link"),
    ("J", "K", 3.4, 6, "Law Road"),
    ("K", "L", 3.9, 7, "Second Gate Access"),
    ("D", "H", 5.1, 9, "Long Corridor"),
    ("F", "G", 4.7, 8, "Science Link"),
    ("H", "J", 5.4, 9, "North-South Link"),
    ("G", "K", 4.8, 8, "Faculty Ring"),
    ("C", "G", 5.6, 9, "Upper Loop"),
    ("F", "I", 4.9, 8, "South Route"),
]

ALL_LOCATIONS = [
    ("A", "1 No. Gate"),
    ("B", "Marine Science"),
    ("C", "Science Faculty"),
    ("D", "Library"),
    ("E", "Arts Faculty"),
    ("F", "IT Building"),
    ("G", "Social Science Faculty"),
    ("H", "Sohid Minar"),
    ("I", "BBA Faculty"),
    ("J", "IER"),
    ("K", "Law Faculty"),
    ("L", "2 No. Gate"),
]

TIME_OPTIONS = ["06:00", "08:00", "10:00", "12:00", "15:00", "18:00", "20:00"]
