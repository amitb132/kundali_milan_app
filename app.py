from datetime import date, time
import streamlit as st
from engine.chart import calculate_moon_details
from engine.ashtakoot import calculate_ashtakoot
from engine.mangal_shukra import calculate_mangal_shukra_sambandha
from engine.manglik import calculate_manglik_matching
import requests

def format_score(value):
    """
    Formats scores cleanly.
    Example:
    24.0 -> 24
    22.5 -> 22.5
    """
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}"


def get_short_verdict(ashtakoot_result):
    total_score = ashtakoot_result["total_score"]
    warnings = ashtakoot_result["warnings"]

    if total_score >= 28:
        verdict = "Strong match by Ashtakoot score."
        tone = "success"
    elif total_score >= 24:
        verdict = "Good match by Ashtakoot score."
        tone = "success"
    elif total_score >= 18:
        verdict = "Acceptable match by Ashtakoot score, but further checks are recommended."
        tone = "warning"
    else:
        verdict = "Low Ashtakoot compatibility. This match needs careful review."
        tone = "error"

    if warnings:
        warning_text = "Important caution: " + ", ".join(warnings)
    else:
        warning_text = "No major Bhakoot or Nadi warning detected in this basic Ashtakoot check."

    return {
        "verdict": verdict,
        "tone": tone,
        "warning_text": warning_text,
    }

def get_final_tldr_verdict(ashtakoot_result, manglik_result, mangal_shukra_result):
    """
    Final one-line verdict for users who only want the direct answer.

    Approval conditions:
    1. Manglik status must be balanced.
    2. Ashtakoot score must be above 18.
    3. Nadi Dosha must not be present.
    4. At least one Mangal Shukra Sambandha must be present.
    """

    score_ok = ashtakoot_result["total_score"] > 18
    manglik_ok = not manglik_result["is_rejected"]
    mangal_shukra_ok = mangal_shukra_result["has_match"]

    nadi_result = None
    for item in ashtakoot_result["components"]:
        if item["name"] == "Nadi":
            nadi_result = item
            break

    if nadi_result is not None:
        nadi_ok = nadi_result["score"] > 0
    else:
        nadi_ok = False

    failed_reasons = []

    if not score_ok:
        failed_reasons.append("Ashtakoot score is not above 18")

    if not nadi_ok:
        failed_reasons.append("Nadi Dosha is present")

    if not manglik_ok:
        failed_reasons.append("Manglik mismatch is present")

    if not mangal_shukra_ok:
        failed_reasons.append("No Mangal Shukra Sambandha is present")

    if score_ok and nadi_ok and manglik_ok and mangal_shukra_ok:
        return {
            "approved": True,
            "title": "Marriage Approved by This Automated Rule-Set",
            "message": (
                "The match is approved because Ashtakoot score is above 18, "
                "Nadi Dosha is not present, Manglik status is balanced, "
                "and Mangal Shukra Sambandha is present."
            ),
            "failed_reasons": [],
        }

    return {
        "approved": False,
        "title": "Marriage Not Approved by This Automated Rule-Set",
        "message": "The match does not satisfy all required approval conditions.",
        "failed_reasons": failed_reasons,
    }

def get_component_result(ashtakoot_result, component_name):
    """
    Fetches one Ashtakoot component by name.
    Example: Nadi, Bhakoot, Gana, etc.
    """

    for item in ashtakoot_result["components"]:
        if item["name"] == component_name:
            return item

    return None

def send_report_to_formspree(report_payload):
    """
    Sends generated Kundali Milan report data to Formspree.
    The endpoint must be stored in Streamlit Secrets.
    """

    endpoint = st.secrets.get("FORMSPREE_REPORT_ENDPOINT")

    if not endpoint:
        raise ValueError("FORMSPREE_REPORT_ENDPOINT is missing from Streamlit Secrets.")

    response = requests.post(
        endpoint,
        json=report_payload,
        timeout=10,
        headers={
            "Accept": "application/json",
        },
    )

    if response.status_code not in [200, 201, 202]:
        raise RuntimeError(
            f"Formspree submission failed: {response.status_code} — {response.text}"
        )

    return True

MIN_BIRTH_DATE = date(1975, 1, 1)
MAX_BIRTH_DATE = date(2020, 12, 31)
DEFAULT_BIRTH_DATE = date(1997, 9, 24)
DEFAULT_BIRTH_TIME = time(0, 58, 0)
ONE_MINUTE = 60

PLACES = {
    "Sadulpur, Rajasthan": {
        "lat": 28.640583,
        "lon": 75.386056,
    },
    "Satnali, Haryana": {
        "lat": 28.383000,
        "lon": 75.967000,
    },
"Jhunjhunu, Rajasthan": {
    "lat": 28.128876,
    "lon": 75.399506,
},
    "Hisar, Haryana": {
        "lat": 29.151861,
        "lon": 75.721123,
    },
    "New Delhi": {
        "lat": 28.644800,
        "lon": 77.216721,
    },
    "Surat, Gujarat": {
        "lat": 21.170240,
        "lon": 72.831062,
    },
    "Mumbai, Maharashtra": {
        "lat": 19.076090,
        "lon": 72.877426,
    },
    "Jaipur, Rajasthan": {
        "lat": 26.907524,
        "lon": 75.739639,
    },
    "Kolkata, West Bengal": {
        "lat": 22.572645,
        "lon": 88.363892,
    },
    "Siliguri, West Bengal": {
        "lat": 26.732311,
        "lon": 88.410286,
    },
    "Bangalore / Bengaluru, Karnataka": {
        "lat": 12.971599,
        "lon": 77.594566,
    },
    "Chennai, Tamil Nadu": {
        "lat": 13.067439,
        "lon": 80.237617,
    },
    "Hyderabad, Telangana": {
        "lat": 17.387140,
        "lon": 78.491684,
    },
    "Indore, Madhya Pradesh": {
        "lat": 22.719568,
        "lon": 75.857727,
    },
    "Guwahati, Assam": {
        "lat": 26.115103,
        "lon": 91.703239,
    },
    "Shimla, Himachal Pradesh": {
        "lat": 31.104605,
        "lon": 77.173424,
    },
}

def format_score(value):
    """
    Formats scores cleanly.
    Example:
    24.0 -> 24
    22.5 -> 22.5
    """
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}"


def get_short_verdict(ashtakoot_result):
    total_score = ashtakoot_result["total_score"]
    warnings = ashtakoot_result["warnings"]

    if total_score >= 28:
        verdict = "Strong match by Ashtakoot score."
        tone = "success"
    elif total_score >= 24:
        verdict = "Good match by Ashtakoot score."
        tone = "success"
    elif total_score >= 18:
        verdict = "Acceptable match by Ashtakoot score, but further checks are recommended."
        tone = "warning"
    else:
        verdict = "Low Ashtakoot compatibility. This match needs careful review."
        tone = "error"

    if warnings:
        warning_text = "Important caution: " + ", ".join(warnings)
    else:
        warning_text = "No major Bhakoot or Nadi warning detected in this basic Ashtakoot check."

    return {
        "verdict": verdict,
        "tone": tone,
        "warning_text": warning_text,
    }

st.set_page_config(
    page_title="Kundali Milan Report",
    page_icon="🪔",
    layout="centered"
)

st.title("Kundali Milan Report Generator")

st.write(
    "Enter the birth details of both individuals. "
    "The system will generate an automated Jyotish-based compatibility report."
)

st.warning(
    "This is an automated report based on Amit Bhardwaj's methods of matching charts. Its equivalent to consulting him in person."
)

place_options = sorted(PLACES.keys())

with st.form("kundali_form"):
    st.header("Groom Details")

    p1_name = st.text_input("Groom Name")
    p1_date = st.date_input(
        "Groom Date of Birth",
        value=DEFAULT_BIRTH_DATE,
        min_value=MIN_BIRTH_DATE,
        max_value=MAX_BIRTH_DATE
    )
    p1_time = st.time_input(
        "Groom Time of Birth",
        value=DEFAULT_BIRTH_TIME,
        step=ONE_MINUTE
    )

    place_options = sorted(PLACES.keys())

    p1_place = st.selectbox(
        "Person 1 Birth Place",
        options=place_options,
        index=0
    )

    p1_lat = PLACES[p1_place]["lat"]
    p1_lon = PLACES[p1_place]["lon"]

    # st.caption(f"Using coordinates: {p1_lat:.6f}, {p1_lon:.6f}")

    st.header("Bride Details")

    p2_name = st.text_input("Bride Name")
    p2_date = st.date_input(
        "Bride Date of Birth",
        value=DEFAULT_BIRTH_DATE,
        min_value=MIN_BIRTH_DATE,
        max_value=MAX_BIRTH_DATE
    )
    p2_time = st.time_input(
        "Bride Time of Birth",
        value=DEFAULT_BIRTH_TIME,
        step=ONE_MINUTE
    )

    p2_place = st.selectbox(
        "Person 2 Birth Place",
        options=place_options,
        index=0
    )

    p2_lat = PLACES[p2_place]["lat"]
    p2_lon = PLACES[p2_place]["lon"]

    # st.caption(f"Using coordinates: {p2_lat:.6f}, {p2_lon:.6f}")

    consent = st.checkbox(
        "I consent to processing these birth details for generating this report and "
        "saving the submitted details and generated results for record/review by the app owner."
    )
    submitted = st.form_submit_button("Generate Kundali Milan Report")

if submitted:
    if not consent:
        st.error("Please provide consent before generating the report.")
    else:
        st.divider()
        st.header("Automated Report")

        chart1 = calculate_moon_details(
            p1_date,
            p1_time,
            timezone_offset_hours=5.5,
            latitude=p1_lat,
            longitude=p1_lon
        )

        chart2 = calculate_moon_details(
            p2_date,
            p2_time,
            timezone_offset_hours=5.5,
            latitude=p2_lat,
            longitude=p2_lon
        )

        ashtakoot_result = calculate_ashtakoot(chart1, chart2)
        manglik_result = calculate_manglik_matching(chart1, chart2)
        mangal_shukra_result = calculate_mangal_shukra_sambandha(chart1, chart2)

        summary = get_short_verdict(ashtakoot_result)
        final_tldr = get_final_tldr_verdict(
            ashtakoot_result,
            manglik_result,
            mangal_shukra_result
        )
        nadi_result = get_component_result(ashtakoot_result, "Nadi")

        report_payload = {
            "report_type": "Kundali Milan Report",
            "final_answer": final_tldr["title"],
            "final_message": final_tldr["message"],
            "failed_reasons": ", ".join(final_tldr["failed_reasons"]) if final_tldr["failed_reasons"] else "None",

            "Groom_name": p1_name or "Person 1",
            "Groom_date": str(p1_date),
            "Groom_time": str(p1_time),
            "Groom_place": p1_place,
            "Groom_lat": p1_lat,
            "Groom_lon": p1_lon,
            "Groom_moon_rashi": chart1["moon_rashi"]["rashi_name"],
            "Groom_moon_nakshatra": chart1["moon_nakshatra"]["nakshatra_name"],
            "Groom_moon_pada": chart1["moon_nakshatra"]["pada"],
            "Groom_mars_rashi": chart1["planets"]["Mars"]["rashi"]["rashi_name"],
            "Groom_mars_navamsa": chart1["planets"]["Mars"]["navamsa"]["rashi_name"],
            "Groom_venus_rashi": chart1["planets"]["Venus"]["rashi"]["rashi_name"],
            "Groom_venus_navamsa": chart1["planets"]["Venus"]["navamsa"]["rashi_name"],

            "Bride_name": p2_name or "Person 2",
            "Bride_date": str(p2_date),
            "Bride_time": str(p2_time),
            "Bride_place": p2_place,
            "Bride_lat": p2_lat,
            "Bride_lon": p2_lon,
            "Bride_moon_rashi": chart2["moon_rashi"]["rashi_name"],
            "Bride_moon_nakshatra": chart2["moon_nakshatra"]["nakshatra_name"],
            "Bride_moon_pada": chart2["moon_nakshatra"]["pada"],
            "Bride_mars_rashi": chart2["planets"]["Mars"]["rashi"]["rashi_name"],
            "Bride_mars_navamsa": chart2["planets"]["Mars"]["navamsa"]["rashi_name"],
            "Bride_venus_rashi": chart2["planets"]["Venus"]["rashi"]["rashi_name"],
            "Bride_venus_navamsa": chart2["planets"]["Venus"]["navamsa"]["rashi_name"],

            "ashtakoot_score": f"{format_score(ashtakoot_result['total_score'])} / {ashtakoot_result['max_score']}",
            "nadi_score": f"{format_score(nadi_result['score'])} / {nadi_result['max_score']}" if nadi_result else "Not calculated",
            "nadi_details": nadi_result["details"] if nadi_result else "Not calculated",

            "manglik_verdict": manglik_result["verdict"],
            "manglik_summary": manglik_result["summary"],
            "Groom_manglik_status": manglik_result["person1"]["status"],
            "Groom_mars_house_from_lagna": manglik_result["person1"]["mars_house_from_lagna"],
            "Bride_manglik_status": manglik_result["person2"]["status"],
            "Bride_mars_house_from_lagna": manglik_result["person2"]["mars_house_from_lagna"],

            "mangal_shukra_strength": mangal_shukra_result["strength"],
            "mangal_shukra_summary": mangal_shukra_result["summary"],
            "mangal_shukra_interpretation": mangal_shukra_result["interpretation"],
        }

        submission_key = (
            f"{report_payload['Groom_name']}_{report_payload['Groom_date']}_{report_payload['Groom_time']}_"
            f"{report_payload['Bride_name']}_{report_payload['Bride_date']}_{report_payload['Bride_time']}"
        )

        if st.session_state.get("last_formspree_submission_key") != submission_key:
            try:
                send_report_to_formspree(report_payload)
                st.session_state["last_formspree_submission_key"] = submission_key
            except Exception as formspree_error:
                st.warning(
                    "The report was generated successfully, but the internal report submission could not be saved."
                )
                st.caption(str(formspree_error))

        st.divider()
        st.header("Kundali Milan Summary")

        st.subheader("Final Answer")

        if final_tldr["approved"]:
            st.success(f"✅ {final_tldr['title']}")
        else:
            st.error(f"❌ {final_tldr['title']}")

        st.write(final_tldr["message"])

        if final_tldr["failed_reasons"]:
            st.write("**Reason(s):**")
            for reason in final_tldr["failed_reasons"]:
                st.write(f"- {reason}")

        st.divider()

        st.metric(
            "Ashtakoot / Guna Milan Score",
            f"{format_score(ashtakoot_result['total_score'])} / {ashtakoot_result['max_score']}"
        )

        if summary["tone"] == "success":
            st.success(summary["verdict"])
        elif summary["tone"] == "warning":
            st.warning(summary["verdict"])
        else:
            st.error(summary["verdict"])

        st.subheader("Nadi Dosha")

        if nadi_result is not None:
            if nadi_result["score"] == 0:
                st.error("Nadi Dosha is present.")
                st.write(
                    "Both individuals have the same Nadi according to this Ashtakoot calculation. "
                    "This is traditionally treated as an important caution point."
                )
            else:
                st.success("Nadi Dosha is not present.")
                st.write(
                    "The Nadi score is acceptable according to this Ashtakoot calculation."
                )

            st.caption(
                f"Nadi Score: {format_score(nadi_result['score'])} / {nadi_result['max_score']} "
                f"— {nadi_result['details']}"
            )
        else:
            st.warning("Nadi result could not be calculated.")

        st.write(
            "This is the first-level compatibility score based on the eight traditional "
            "Ashtakoot factors. Detailed reasoning is available below for users who want "
            "to inspect the calculation."
        )

        st.subheader("Manglik Dosha Matching")

        if manglik_result["severity"] == "success":
            st.success(f"{manglik_result['verdict']}: {manglik_result['summary']}")
        else:
            st.error(f"{manglik_result['verdict']}: {manglik_result['summary']}")

        st.write(manglik_result["interpretation"])

        st.subheader("Mangal Shukra Sambandha")

        if mangal_shukra_result["strength"] in ["Very Strong", "Strong", "Good"]:
            st.success(
                f"{mangal_shukra_result['strength']}: "
                f"{mangal_shukra_result['summary']}"
            )
        elif mangal_shukra_result["strength"] == "Moderate":
            st.warning(
                f"{mangal_shukra_result['strength']}: "
                f"{mangal_shukra_result['summary']}"
            )
        else:
            st.info(
                f"{mangal_shukra_result['strength']}: "
                f"{mangal_shukra_result['summary']}"
            )

        st.write(mangal_shukra_result["interpretation"])

        with st.expander("Details"):
            st.subheader("Eight Koota Score Breakdown")

            score_rows = []
            for item in ashtakoot_result["components"]:
                score_rows.append(
                    {
                        "Koota": item["name"],
                        "Score": f"{format_score(item['score'])} / {item['max_score']}",
                        "Details": item["details"],
                    }
                )

            st.table(score_rows)

            st.subheader("Manglik Dosha Details")

            manglik_rows = []

            for person_label, person_result in [
                (p1_name or "Groom", manglik_result["person1"]),
                (p2_name or "Bride", manglik_result["person2"]),
            ]:
                manglik_rows.append(
                    {
                        "Person": person_label,
                        "Status": person_result["status"],
                        "Lagna Rashi": person_result["lagna_rashi"],
                        "Mars Rashi": person_result["mars_rashi"],
                        "Mars House from Lagna": person_result["mars_house_from_lagna"],
                        "Interpretation": person_result["interpretation"],
                    }
                )

            st.table(manglik_rows)

            st.write(
                "Rule used here: Mars in the 1st, 4th, 7th, 8th, or 12th house from Lagna "
                "is treated as Manglik. If both are Manglik or both are Non-Manglik, the status "
                "is treated as balanced. If only one person is Manglik, the match is rejected "
                "by this rule-set."
            )

            st.subheader(f"{p1_name or 'Groom'} Moon Details")

            st.write(f"**Moon Longitude:** {chart1['moon_longitude']:.4f}°")
            st.write(
                f"**Moon Rashi:** "
                f"{chart1['moon_rashi']['rashi_name']} "
                f"({chart1['moon_rashi']['degrees_in_rashi']:.2f}°)"
            )
            st.write(
                f"**Moon Nakshatra:** "
                f"{chart1['moon_nakshatra']['nakshatra_name']}, "
                f"Pada {chart1['moon_nakshatra']['pada']}"
            )

            st.subheader(f"{p2_name or 'Bride'} Moon Details")

            st.write(f"**Moon Longitude:** {chart2['moon_longitude']:.4f}°")
            st.write(
                f"**Moon Rashi:** "
                f"{chart2['moon_rashi']['rashi_name']} "
                f"({chart2['moon_rashi']['degrees_in_rashi']:.2f}°)"
            )
            st.write(
                f"**Moon Nakshatra:** "
                f"{chart2['moon_nakshatra']['nakshatra_name']}, "
                f"Pada {chart2['moon_nakshatra']['pada']}"
            )

            st.subheader("Mangal Shukra Sambandha Details")

            st.write(
                "This rule checks whether Mars and Venus of both people connect through the "
                "same zodiac sign in either Rashi or Navamsa."
            )

            if mangal_shukra_result["matches"]:
                match_rows = []

                for match in mangal_shukra_result["matches"]:
                    match_rows.append(
                        {
                            "Matched Rashi": match["rashi_name"],
                            "Groom Placement": (
                                f"{match['person1_planet']} {match['person1_varga']}"
                            ),
                            "Bride Placement": (
                                f"{match['person2_planet']} {match['person2_varga']}"
                            ),
                        }
                    )

                st.table(match_rows)
            else:
                st.write("No direct Mars/Venus rashi-navamsa overlap found.")

            st.subheader("Mars and Venus Positions")

            planet_rows = []

            for person_label, chart in [
                (p1_name or "Groom", chart1),
                (p2_name or "Bride", chart2),
            ]:
                for planet_name in ["Mars", "Venus"]:
                    planet = chart["planets"][planet_name]

                    planet_rows.append(
                        {
                            "Person": person_label,
                            "Planet": planet_name,
                            "Rashi": planet["rashi"]["rashi_name"],
                            "Navamsa": planet["navamsa"]["rashi_name"],
                            "Longitude": f"{planet['longitude']:.4f}°",
                        }
                    )

            st.table(planet_rows)

            st.subheader("Current Calculation Notes")


            st.write(
                "- Birth times are currently assumed to be in IST."
            )
            st.write(
                "- Bhakoot and Nadi warnings are shown in the summary because people usually "
                "care about these even when the total score is acceptable."
            )