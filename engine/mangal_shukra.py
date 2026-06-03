# engine/mangal_shukra.py


def planet_rashi_set(chart, planet_name):
    """
    Returns both rashi and navamsa rashi positions of a planet as comparable items.
    """

    planet = chart["planets"][planet_name]

    return [
        {
            "planet": planet_name,
            "varga": "Rashi",
            "rashi_index": planet["rashi"]["rashi_index"],
            "rashi_name": planet["rashi"]["rashi_name"],
        },
        {
            "planet": planet_name,
            "varga": "Navamsa",
            "rashi_index": planet["navamsa"]["rashi_index"],
            "rashi_name": planet["navamsa"]["rashi_name"],
        },
    ]


def compare_planet_positions(person1_positions, person2_positions):
    """
    Finds all zodiac overlaps between two planet-position sets.
    """

    matches = []

    for p1 in person1_positions:
        for p2 in person2_positions:
            if p1["rashi_index"] == p2["rashi_index"]:
                matches.append(
                    {
                        "rashi_name": p1["rashi_name"],
                        "person1_planet": p1["planet"],
                        "person1_varga": p1["varga"],
                        "person2_planet": p2["planet"],
                        "person2_varga": p2["varga"],
                    }
                )

    return matches


def calculate_mangal_shukra_sambandha(chart1, chart2):
    """
    Custom compatibility rule.

    Person 1 is treated as Male/Groom.
    Person 2 is treated as Female/Bride.

    Checks whether Mars and Venus of both persons connect through
    same zodiac sign in either Rashi or Navamsa.
    """

    p1_mars = planet_rashi_set(chart1, "Mars")
    p1_venus = planet_rashi_set(chart1, "Venus")

    p2_mars = planet_rashi_set(chart2, "Mars")
    p2_venus = planet_rashi_set(chart2, "Venus")

    mars_mars_matches = compare_planet_positions(p1_mars, p2_mars)
    venus_venus_matches = compare_planet_positions(p1_venus, p2_venus)

    male_mars_female_venus_matches = compare_planet_positions(p1_mars, p2_venus)
    female_mars_male_venus_matches = compare_planet_positions(p2_mars, p1_venus)

    has_mars_mars = len(mars_mars_matches) > 0
    has_venus_venus = len(venus_venus_matches) > 0
    has_male_mars_female_venus = len(male_mars_female_venus_matches) > 0
    has_female_mars_male_venus = len(female_mars_male_venus_matches) > 0

    all_matches = (
        mars_mars_matches
        + venus_venus_matches
        + male_mars_female_venus_matches
        + female_mars_male_venus_matches
    )

    has_any_match = len(all_matches) > 0

    if has_mars_mars and has_venus_venus:
        strength = "Very Strong"
        summary = "Both Mars and Venus sambandha are present."
        interpretation = (
            "This indicates a strong combination of passion, affection, emotional warmth, "
            "respect, and long-term relationship harmony."
        )

    elif has_male_mars_female_venus:
        strength = "Strong"
        summary = "Male Mars and Female Venus sambandha is present."
        interpretation = (
            "This is considered the best Mars-Venus combination in this rule-set. "
            "It indicates attraction, relationship chemistry, passion, and harmony."
        )

    elif has_venus_venus:
        strength = "Good"
        summary = "Venus-Venus sambandha is present."
        interpretation = (
            "This indicates affection, comfort, love, laughter, and long-term companionship. "
            "The relationship may feel emotionally pleasant and socially harmonious."
        )

    elif has_mars_mars:
        strength = "Moderate"
        summary = "Mars-Mars sambandha is present."
        interpretation = (
            "This indicates passion, attraction, and strong physical energy. "
            "However, by itself it may show more passion than softness or emotional love."
        )

    elif has_female_mars_male_venus:
        strength = "Moderate"
        summary = "Female Mars and Male Venus sambandha is present."
        interpretation = (
            "This indicates mutual attraction and chemistry, though it is not treated as "
            "the strongest directional combination in this rule-set."
        )

    else:
        strength = "Weak"
        summary = "No clear Mangal-Shukra sambandha found."
        interpretation = (
            "No direct rashi/navamsa overlap was found between Mars and Venus placements "
            "in this rule-set. This does not reject the match, but it does not add extra "
            "relationship-harmony support from this factor."
        )

    return {
        "name": "Mangal Shukra Sambandha",
        "has_match": has_any_match,
        "strength": strength,
        "summary": summary,
        "interpretation": interpretation,
        "matches": all_matches,
        "mars_mars_matches": mars_mars_matches,
        "venus_venus_matches": venus_venus_matches,
        "male_mars_female_venus_matches": male_mars_female_venus_matches,
        "female_mars_male_venus_matches": female_mars_male_venus_matches,
    }