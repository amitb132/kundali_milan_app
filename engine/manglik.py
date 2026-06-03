# engine/manglik.py


MANGLIK_HOUSES = [1, 4, 7, 8, 12]


def house_from_lagna(lagna_rashi_index, planet_rashi_index):
    """
    Whole-sign house distance from Lagna.

    Lagna rashi = 1st house.
    Next rashi = 2nd house.
    """

    return ((planet_rashi_index - lagna_rashi_index) % 12) + 1


def calculate_single_manglik_status(chart):
    """
    Calculates Manglik status using Mars placement from Lagna.

    Rule used:
    Mars in 1st, 4th, 7th, 8th, or 12th house from Lagna = Manglik.
    """

    if chart.get("lagna") is None:
        raise ValueError(
            "Lagna details are missing. Pass latitude and longitude into calculate_moon_details()."
        )

    lagna_rashi = chart["lagna"]["rashi"]
    mars = chart["planets"]["Mars"]

    lagna_rashi_index = lagna_rashi["rashi_index"]
    mars_rashi_index = mars["rashi"]["rashi_index"]

    mars_house = house_from_lagna(lagna_rashi_index, mars_rashi_index)
    is_manglik = mars_house in MANGLIK_HOUSES

    if is_manglik:
        status = "Manglik"
        interpretation = (
            f"Mars is placed in the {mars_house} house from Lagna. "
            "According to this rule-set, this chart is Manglik."
        )
    else:
        status = "Non-Manglik"
        interpretation = (
            f"Mars is placed in the {mars_house} house from Lagna. "
            "According to this rule-set, this chart is not Manglik."
        )

    return {
        "is_manglik": is_manglik,
        "status": status,
        "mars_house_from_lagna": mars_house,
        "lagna_rashi": lagna_rashi["rashi_name"],
        "mars_rashi": mars["rashi"]["rashi_name"],
        "interpretation": interpretation,
    }


def calculate_manglik_matching(chart1, chart2):
    """
    Compares Manglik status of both charts.

    Matching rule:
    - Both Manglik: acceptable/balanced
    - Both Non-Manglik: acceptable/balanced
    - Only one Manglik: reject
    """

    person1 = calculate_single_manglik_status(chart1)
    person2 = calculate_single_manglik_status(chart2)

    p1_manglik = person1["is_manglik"]
    p2_manglik = person2["is_manglik"]

    if p1_manglik and p2_manglik:
        verdict = "Manglik status balanced"
        severity = "success"
        summary = "Both charts are Manglik."
        interpretation = (
            "Both individuals are Manglik according to this rule-set. "
            "The Manglik factor is considered balanced between the two charts."
        )

    elif not p1_manglik and not p2_manglik:
        verdict = "Manglik status balanced"
        severity = "success"
        summary = "Both charts are Non-Manglik."
        interpretation = (
            "Neither individual is Manglik according to this rule-set. "
            "No Manglik mismatch is detected."
        )

    else:
        verdict = "Manglik mismatch"
        severity = "error"
        summary = "Only one chart is Manglik."
        interpretation = (
            "Only one individual is Manglik according to this rule-set. "
            "This match is rejected by the Manglik matching condition."
        )

    return {
        "name": "Manglik Dosha Matching",
        "verdict": verdict,
        "severity": severity,
        "summary": summary,
        "interpretation": interpretation,
        "person1": person1,
        "person2": person2,
        "is_rejected": severity == "error",
    }