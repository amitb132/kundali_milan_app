# engine/ashtakoot.py

RASHI_LORDS = {
    0: "Mars",      # Mesha
    1: "Venus",    # Vrishabha
    2: "Mercury",  # Mithuna
    3: "Moon",     # Karka
    4: "Sun",      # Simha
    5: "Mercury",  # Kanya
    6: "Venus",    # Tula
    7: "Mars",     # Vrischika
    8: "Jupiter",  # Dhanu
    9: "Saturn",   # Makara
    10: "Saturn",  # Kumbha
    11: "Jupiter", # Meena
}


VARNA_RANK = {
    # Higher rank = traditionally higher varna category
    # Shudra = 1, Vaishya = 2, Kshatriya = 3, Brahmin = 4
    0: 3,   # Mesha - Kshatriya
    1: 2,   # Vrishabha - Vaishya
    2: 1,   # Mithuna - Shudra
    3: 4,   # Karka - Brahmin
    4: 3,   # Simha - Kshatriya
    5: 2,   # Kanya - Vaishya
    6: 1,   # Tula - Shudra
    7: 4,   # Vrischika - Brahmin
    8: 3,   # Dhanu - Kshatriya
    9: 2,   # Makara - Vaishya
    10: 1,  # Kumbha - Shudra
    11: 4,  # Meena - Brahmin
}


VARNA_NAMES = {
    1: "Shudra",
    2: "Vaishya",
    3: "Kshatriya",
    4: "Brahmin",
}


GANA_BY_NAKSHATRA = {
    0: "Deva",      # Ashwini
    1: "Manushya",  # Bharani
    2: "Rakshasa",  # Krittika
    3: "Manushya",  # Rohini
    4: "Deva",      # Mrigashira
    5: "Manushya",  # Ardra
    6: "Deva",      # Punarvasu
    7: "Deva",      # Pushya
    8: "Rakshasa",  # Ashlesha
    9: "Rakshasa",  # Magha
    10: "Manushya", # Purva Phalguni
    11: "Manushya", # Uttara Phalguni
    12: "Deva",     # Hasta
    13: "Rakshasa", # Chitra
    14: "Deva",     # Swati
    15: "Rakshasa", # Vishakha
    16: "Deva",     # Anuradha
    17: "Rakshasa", # Jyeshtha
    18: "Rakshasa", # Mula
    19: "Manushya", # Purva Ashadha
    20: "Manushya", # Uttara Ashadha
    21: "Deva",     # Shravana
    22: "Rakshasa", # Dhanishta
    23: "Rakshasa", # Shatabhisha
    24: "Manushya", # Purva Bhadrapada
    25: "Manushya", # Uttara Bhadrapada
    26: "Deva",     # Revati
}


NADI_BY_NAKSHATRA = {
    0: "Aadi",
    1: "Madhya",
    2: "Antya",
    3: "Antya",
    4: "Madhya",
    5: "Aadi",
    6: "Aadi",
    7: "Madhya",
    8: "Antya",
    9: "Antya",
    10: "Madhya",
    11: "Aadi",
    12: "Aadi",
    13: "Madhya",
    14: "Antya",
    15: "Antya",
    16: "Madhya",
    17: "Aadi",
    18: "Aadi",
    19: "Madhya",
    20: "Antya",
    21: "Antya",
    22: "Madhya",
    23: "Aadi",
    24: "Aadi",
    25: "Madhya",
    26: "Antya",
}


YONI_BY_NAKSHATRA = {
    0: "Horse",
    1: "Elephant",
    2: "Sheep",
    3: "Serpent",
    4: "Serpent",
    5: "Dog",
    6: "Cat",
    7: "Sheep",
    8: "Cat",
    9: "Rat",
    10: "Rat",
    11: "Cow",
    12: "Buffalo",
    13: "Tiger",
    14: "Buffalo",
    15: "Tiger",
    16: "Deer",
    17: "Deer",
    18: "Dog",
    19: "Monkey",
    20: "Mongoose",
    21: "Monkey",
    22: "Lion",
    23: "Horse",
    24: "Lion",
    25: "Cow",
    26: "Elephant",
}


YONI_ENEMY_PAIRS = {
    frozenset(["Horse", "Buffalo"]),
    frozenset(["Elephant", "Lion"]),
    frozenset(["Sheep", "Monkey"]),
    frozenset(["Serpent", "Mongoose"]),
    frozenset(["Dog", "Deer"]),
    frozenset(["Cat", "Rat"]),
    frozenset(["Cow", "Tiger"]),
}


PLANET_RELATIONSHIPS = {
    "Sun": {
        "friends": ["Moon", "Mars", "Jupiter"],
        "neutral": ["Mercury"],
        "enemies": ["Venus", "Saturn"],
    },
    "Moon": {
        "friends": ["Sun", "Mercury"],
        "neutral": ["Mars", "Jupiter", "Venus", "Saturn"],
        "enemies": [],
    },
    "Mars": {
        "friends": ["Sun", "Moon", "Jupiter"],
        "neutral": ["Venus", "Saturn"],
        "enemies": ["Mercury"],
    },
    "Mercury": {
        "friends": ["Sun", "Venus"],
        "neutral": ["Mars", "Jupiter", "Saturn"],
        "enemies": ["Moon"],
    },
    "Jupiter": {
        "friends": ["Sun", "Moon", "Mars"],
        "neutral": ["Saturn"],
        "enemies": ["Mercury", "Venus"],
    },
    "Venus": {
        "friends": ["Mercury", "Saturn"],
        "neutral": ["Mars", "Jupiter"],
        "enemies": ["Sun", "Moon"],
    },
    "Saturn": {
        "friends": ["Mercury", "Venus"],
        "neutral": ["Jupiter"],
        "enemies": ["Sun", "Moon", "Mars"],
    },
}


VASHYA_BY_RASHI = {
    0: "Chatushpada",  # Mesha
    1: "Chatushpada",  # Vrishabha
    2: "Manava",       # Mithuna
    3: "Jalchar",      # Karka
    4: "Vanachara",    # Simha
    5: "Manava",       # Kanya
    6: "Manava",       # Tula
    7: "Keeta",        # Vrischika
    8: "Chatushpada",  # Dhanu simplified
    9: "Chatushpada",  # Makara simplified
    10: "Manava",      # Kumbha
    11: "Jalchar",     # Meena
}


def rashi_distance(from_rashi_index, to_rashi_index):
    return ((to_rashi_index - from_rashi_index) % 12) + 1


def get_core_values(chart):
    return {
        "rashi_index": chart["moon_rashi"]["rashi_index"],
        "rashi_name": chart["moon_rashi"]["rashi_name"],
        "nakshatra_index": chart["moon_nakshatra"]["nakshatra_index"],
        "nakshatra_name": chart["moon_nakshatra"]["nakshatra_name"],
        "pada": chart["moon_nakshatra"]["pada"],
    }


def calculate_varna(chart1, chart2):
    """
    Directional rule.
    Person 1 is treated as groom/boy.
    Person 2 is treated as bride/girl.

    Score 1 if groom varna rank >= bride varna rank, else 0.
    """

    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    groom_rank = VARNA_RANK[c1["rashi_index"]]
    bride_rank = VARNA_RANK[c2["rashi_index"]]

    score = 1 if groom_rank >= bride_rank else 0

    return {
        "name": "Varna",
        "score": score,
        "max_score": 1,
        "details": f"{VARNA_NAMES[groom_rank]} / {VARNA_NAMES[bride_rank]}",
    }


def calculate_vashya(chart1, chart2):
    """
    Simplified Vashya scoring.
    Full refinement can later split Dhanu/Makara by degrees.
    """

    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    v1 = VASHYA_BY_RASHI[c1["rashi_index"]]
    v2 = VASHYA_BY_RASHI[c2["rashi_index"]]

    if v1 == v2:
        score = 2
    elif "Manava" in [v1, v2]:
        score = 1
    else:
        score = 0

    return {
        "name": "Vashya",
        "score": score,
        "max_score": 2,
        "details": f"{v1} / {v2}",
    }


def calculate_tara(chart1, chart2):
    """
    Tara/Dina score.

    Count nakshatra distance both ways.
    If distance % 9 is 3, 5, or 7, that direction is inauspicious.
    Each good direction gives 1.5 points.
    """

    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    n1 = c1["nakshatra_index"]
    n2 = c2["nakshatra_index"]

    d1 = ((n2 - n1) % 27) + 1
    d2 = ((n1 - n2) % 27) + 1

    bad_remainders = [3, 5, 7]

    r1 = d1 % 9
    r2 = d2 % 9

    good1 = r1 not in bad_remainders
    good2 = r2 not in bad_remainders

    score = 0
    if good1:
        score += 1.5
    if good2:
        score += 1.5

    return {
        "name": "Tara",
        "score": score,
        "max_score": 3,
        "details": f"Distances {d1} / {d2}",
    }


def calculate_yoni(chart1, chart2):
    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    y1 = YONI_BY_NAKSHATRA[c1["nakshatra_index"]]
    y2 = YONI_BY_NAKSHATRA[c2["nakshatra_index"]]

    pair = frozenset([y1, y2])

    if y1 == y2:
        score = 4
    elif pair in YONI_ENEMY_PAIRS:
        score = 0
    else:
        score = 2

    return {
        "name": "Yoni",
        "score": score,
        "max_score": 4,
        "details": f"{y1} / {y2}",
    }


def relationship_from_to(planet1, planet2):
    if planet1 == planet2:
        return "same"

    rel = PLANET_RELATIONSHIPS[planet1]

    if planet2 in rel["friends"]:
        return "friend"
    if planet2 in rel["neutral"]:
        return "neutral"
    if planet2 in rel["enemies"]:
        return "enemy"

    return "neutral"


def calculate_graha_maitri(chart1, chart2):
    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    lord1 = RASHI_LORDS[c1["rashi_index"]]
    lord2 = RASHI_LORDS[c2["rashi_index"]]

    rel1 = relationship_from_to(lord1, lord2)
    rel2 = relationship_from_to(lord2, lord1)

    if lord1 == lord2:
        score = 5
    elif rel1 == "friend" and rel2 == "friend":
        score = 5
    elif "friend" in [rel1, rel2] and "neutral" in [rel1, rel2]:
        score = 4
    elif rel1 == "neutral" and rel2 == "neutral":
        score = 3
    elif "friend" in [rel1, rel2] and "enemy" in [rel1, rel2]:
        score = 1
    elif "neutral" in [rel1, rel2] and "enemy" in [rel1, rel2]:
        score = 0.5
    else:
        score = 0

    return {
        "name": "Graha Maitri",
        "score": score,
        "max_score": 5,
        "details": f"{lord1} to {lord2}: {rel1}; {lord2} to {lord1}: {rel2}",
    }


def calculate_gana(chart1, chart2):
    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    g1 = GANA_BY_NAKSHATRA[c1["nakshatra_index"]]
    g2 = GANA_BY_NAKSHATRA[c2["nakshatra_index"]]

    if g1 == g2:
        score = 6
    elif set([g1, g2]) == set(["Deva", "Manushya"]):
        score = 5
    elif set([g1, g2]) == set(["Deva", "Rakshasa"]):
        score = 1
    else:
        score = 0

    return {
        "name": "Gana",
        "score": score,
        "max_score": 6,
        "details": f"{g1} / {g2}",
    }


def calculate_bhakoot(chart1, chart2):
    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    r1 = c1["rashi_index"]
    r2 = c2["rashi_index"]

    d1 = rashi_distance(r1, r2)
    d2 = rashi_distance(r2, r1)

    distance_pair = {d1, d2}

    if distance_pair == {2, 12}:
        score = 0
        details = "Dwi-Dwadash / 2-12 relationship"
    elif distance_pair == {5, 9}:
        score = 0
        details = "Nav-Pancham / 5-9 relationship"
    elif distance_pair == {6, 8}:
        score = 0
        details = "Shadashtak / 6-8 relationship"
    else:
        score = 7
        details = "Favourable Bhakoot relationship"

    return {
        "name": "Bhakoot",
        "score": score,
        "max_score": 7,
        "details": f"{c1['rashi_name']} to {c2['rashi_name']} = {d1}/{d2}; {details}",
    }


def calculate_nadi(chart1, chart2):
    c1 = get_core_values(chart1)
    c2 = get_core_values(chart2)

    nadi1 = NADI_BY_NAKSHATRA[c1["nakshatra_index"]]
    nadi2 = NADI_BY_NAKSHATRA[c2["nakshatra_index"]]

    score = 0 if nadi1 == nadi2 else 8

    return {
        "name": "Nadi",
        "score": score,
        "max_score": 8,
        "details": f"{nadi1} / {nadi2}",
    }


def interpret_total_score(total_score):
    if total_score >= 28:
        return "Strong Ashtakoot compatibility by score."
    elif total_score >= 24:
        return "Good Ashtakoot compatibility by score."
    elif total_score >= 18:
        return "Acceptable Ashtakoot compatibility by score, but detailed dosha checks are needed."
    else:
        return "Low Ashtakoot compatibility by score."


def calculate_ashtakoot(chart1, chart2):
    components = [
        calculate_varna(chart1, chart2),
        calculate_vashya(chart1, chart2),
        calculate_tara(chart1, chart2),
        calculate_yoni(chart1, chart2),
        calculate_graha_maitri(chart1, chart2),
        calculate_gana(chart1, chart2),
        calculate_bhakoot(chart1, chart2),
        calculate_nadi(chart1, chart2),
    ]

    total_score = sum(item["score"] for item in components)

    bhakoot_score = next(item["score"] for item in components if item["name"] == "Bhakoot")
    nadi_score = next(item["score"] for item in components if item["name"] == "Nadi")

    warnings = []

    if bhakoot_score == 0:
        warnings.append("Bhakoot Dosha is present.")

    if nadi_score == 0:
        warnings.append("Nadi Dosha is present.")

    return {
        "total_score": total_score,
        "max_score": 36,
        "components": components,
        "interpretation": interpret_total_score(total_score),
        "warnings": warnings,
    }