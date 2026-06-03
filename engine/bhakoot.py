def rashi_distance(from_rashi_index, to_rashi_index):
    """
    Returns inclusive rashi distance from one Moon rashi to another.

    Example:
    Mesha to Mesha = 1
    Mesha to Vrishabha = 2
    Mesha to Mithuna = 3

    Rashi indices are expected as:
    0 = Mesha, 1 = Vrishabha, ..., 11 = Meena
    """

    return ((to_rashi_index - from_rashi_index) % 12) + 1


def calculate_bhakoot(chart1, chart2):
    """
    Calculates Bhakoot Milan based on Moon rashi relationship.

    Common scoring:
    - 1/1, 1/7, 3/11, 4/10 = 7 points
    - 2/12, 5/9, 6/8 = 0 points
    """

    rashi1 = chart1["moon_rashi"]["rashi_index"]
    rashi2 = chart2["moon_rashi"]["rashi_index"]

    rashi1_name = chart1["moon_rashi"]["rashi_name"]
    rashi2_name = chart2["moon_rashi"]["rashi_name"]

    distance_1_to_2 = rashi_distance(rashi1, rashi2)
    distance_2_to_1 = rashi_distance(rashi2, rashi1)

    distance_pair = {distance_1_to_2, distance_2_to_1}

    if distance_pair == {2, 12}:
        score = 0
        status = "Bhakoot Dosha Present"
        bhakoot_type = "Dwi-Dwadash Bhakoot / 2-12 relationship"
        interpretation = (
            "This is traditionally considered an inauspicious Bhakoot relationship. "
            "It is commonly associated with financial strain, value mismatch, or practical friction."
        )

    elif distance_pair == {5, 9}:
        score = 0
        status = "Bhakoot Dosha Present"
        bhakoot_type = "Nav-Pancham Bhakoot / 5-9 relationship"
        interpretation = (
            "This is traditionally considered an inauspicious Bhakoot relationship. "
            "It is commonly associated with differences in dharma, family growth, children, or long-term direction."
        )

    elif distance_pair == {6, 8}:
        score = 0
        status = "Bhakoot Dosha Present"
        bhakoot_type = "Shadashtak Bhakoot / 6-8 relationship"
        interpretation = (
            "This is traditionally considered one of the more difficult Bhakoot relationships. "
            "It is commonly associated with conflict, health concerns, stress, or instability."
        )

    else:
        score = 7
        status = "Bhakoot Milan Acceptable"
        bhakoot_type = "Sad Bhakoot / favourable rashi relationship"
        interpretation = (
            "The Moon rashis form a favourable Bhakoot relationship according to the basic rule-set. "
            "Full Bhakoot points are awarded."
        )

    return {
        "score": score,
        "max_score": 7,
        "status": status,
        "bhakoot_type": bhakoot_type,
        "interpretation": interpretation,
        "person1_rashi": rashi1_name,
        "person2_rashi": rashi2_name,
        "distance_1_to_2": distance_1_to_2,
        "distance_2_to_1": distance_2_to_1,
    }