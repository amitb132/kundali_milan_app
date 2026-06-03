from datetime import datetime, timedelta
import swisseph as swe


RASHI_NAMES = [
    "Mesha",       # Aries
    "Vrishabha",  # Taurus
    "Mithuna",    # Gemini
    "Karka",      # Cancer
    "Simha",      # Leo
    "Kanya",      # Virgo
    "Tula",       # Libra
    "Vrischika",  # Scorpio
    "Dhanu",      # Sagittarius
    "Makara",     # Capricorn
    "Kumbha",     # Aquarius
    "Meena",      # Pisces
]


NAKSHATRA_NAMES = [
    "Ashwini",
    "Bharani",
    "Krittika",
    "Rohini",
    "Mrigashira",
    "Ardra",
    "Punarvasu",
    "Pushya",
    "Ashlesha",
    "Magha",
    "Purva Phalguni",
    "Uttara Phalguni",
    "Hasta",
    "Chitra",
    "Swati",
    "Vishakha",
    "Anuradha",
    "Jyeshtha",
    "Mula",
    "Purva Ashadha",
    "Uttara Ashadha",
    "Shravana",
    "Dhanishta",
    "Shatabhisha",
    "Purva Bhadrapada",
    "Uttara Bhadrapada",
    "Revati",
]


def decimal_hours(dt):
    return dt.hour + dt.minute / 60.0 + dt.second / 3600.0


def normalize_degrees(value):
    return value % 360.0


def get_rashi(longitude):
    longitude = normalize_degrees(longitude)
    rashi_index = int(longitude // 30.0)
    degrees_in_rashi = longitude % 30.0

    return {
        "rashi_index": rashi_index,
        "rashi_name": RASHI_NAMES[rashi_index],
        "degrees_in_rashi": degrees_in_rashi,
    }

def get_navamsa_rashi(longitude):
    """
    Calculates Navamsa rashi from sidereal longitude.

    Formula:
    Navamsa longitude = longitude * 9, normalized to 360 degrees.
    Navamsa rashi = floor(navamsa_longitude / 30)
    """

    longitude = normalize_degrees(longitude)
    navamsa_longitude = normalize_degrees(longitude * 9.0)

    navamsa_rashi_index = int(navamsa_longitude // 30.0)
    degrees_in_navamsa_rashi = navamsa_longitude % 30.0

    return {
        "rashi_index": navamsa_rashi_index,
        "rashi_name": RASHI_NAMES[navamsa_rashi_index],
        "degrees_in_rashi": degrees_in_navamsa_rashi,
    }

def get_nakshatra(longitude):
    longitude = normalize_degrees(longitude)

    nakshatra_span = 360.0 / 27.0
    pada_span = nakshatra_span / 4.0

    nakshatra_index = int(longitude // nakshatra_span)
    degrees_in_nakshatra = longitude - (nakshatra_index * nakshatra_span)
    pada = int(degrees_in_nakshatra // pada_span) + 1

    return {
        "nakshatra_index": nakshatra_index,
        "nakshatra_name": NAKSHATRA_NAMES[nakshatra_index],
        "degrees_in_nakshatra": degrees_in_nakshatra,
        "pada": pada,
    }

def calculate_planet_details_from_jd(jd_ut, planet_id):
    """
    Calculates sidereal planetary longitude, rashi, and navamsa rashi.
    """

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    flags = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    planet_data, ret_flag = swe.calc_ut(jd_ut, planet_id, flags)

    longitude = normalize_degrees(planet_data[0])
    speed = planet_data[3]

    rashi = get_rashi(longitude)
    navamsa = get_navamsa_rashi(longitude)

    return {
        "longitude": longitude,
        "speed": speed,
        "rashi": rashi,
        "navamsa": navamsa,
    }

def calculate_lagna_details(jd_ut, latitude, longitude):
    """
    Calculates Lahiri sidereal Lagna.

    Swiss Ephemeris house calculation gives tropical ascendant.
    We subtract Lahiri ayanamsha to get sidereal Lagna.
    """

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    cusps, ascmc = swe.houses_ex(
        jd_ut,
        latitude,
        longitude,
        b'P'
    )

    tropical_ascendant = normalize_degrees(ascmc[0])
    ayanamsha = swe.get_ayanamsa_ut(jd_ut)
    sidereal_ascendant = normalize_degrees(tropical_ascendant - ayanamsha)

    rashi = get_rashi(sidereal_ascendant)

    return {
        "longitude": sidereal_ascendant,
        "rashi": rashi,
    }

def calculate_moon_details(
    date_value,
    time_value,
    timezone_offset_hours=5.5,
    latitude=None,
    longitude=None
):
    """
    Calculates sidereal Moon longitude using Lahiri ayanamsha.

    date_value: datetime.date
    time_value: datetime.time
    timezone_offset_hours: default 5.5 for IST
    """

    local_dt = datetime.combine(date_value, time_value)
    utc_dt = local_dt - timedelta(hours=timezone_offset_hours)

    jd_ut = swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        decimal_hours(utc_dt)
    )

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    flags = swe.FLG_MOSEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    moon_data, ret_flag = swe.calc_ut(jd_ut, swe.MOON, flags)

    moon_longitude = normalize_degrees(moon_data[0])
    moon_speed = moon_data[3]

    rashi = get_rashi(moon_longitude)
    nakshatra = get_nakshatra(moon_longitude)

    mars_details = calculate_planet_details_from_jd(jd_ut, swe.MARS)
    venus_details = calculate_planet_details_from_jd(jd_ut, swe.VENUS)

    lagna_details = None

    if latitude is not None and longitude is not None:
        lagna_details = calculate_lagna_details(jd_ut, latitude, longitude)

    return {
        "julian_day_ut": jd_ut,
        "moon_longitude": moon_longitude,
        "moon_speed": moon_speed,
        "moon_rashi": rashi,
        "moon_nakshatra": nakshatra,
        "lagna": lagna_details,
        "planets": {
            "Mars": mars_details,
            "Venus": venus_details,
        },
    }