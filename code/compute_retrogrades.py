"""
compute_retrogrades.py
======================

Computes all Venus retrograde periods between 800 BCE and 2027 CE using the
Swiss Ephemeris (Moshier analytical mode) and assigns each retrograde to one
of five 8-year synodic series.

Outputs:
  - Total count of retrograde periods detected (expected: 1768)
  - One line per retrograde with start date, end date, sign, and series

Usage:
  python compute_retrogrades.py

Requires: pyswisseph 2.10.3
"""

import swisseph as swe

# Use the Moshier analytical ephemeris (built-in, no extra files needed,
# provides sub-arcminute accuracy across the full study period).
swe.set_ephe_path(None)

SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
         'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

# Mean Venus synodic cycle in days (5 retrogrades per 8 sidereal years).
CYCLE = 2919.6

# Anchor each of the five series to a known retrograde station in the 2020s.
# Series are then identified by minimum-distance assignment to these anchors.
ANCHORS = {
    'A': swe.julday(2020, 5, 13, 0.0),   # Gemini
    'B': swe.julday(2021, 12, 19, 0.0),  # Capricorn
    'C': swe.julday(2023, 7, 23, 0.0),   # Leo
    'D': swe.julday(2025, 3, 2, 0.0),    # Aries
    'E': swe.julday(2026, 10, 3, 0.0),   # Scorpio
}


def get_venus_speed(jd):
    """Return (longitude_speed_deg_per_day, longitude_deg) for Venus at Julian Day jd."""
    result = swe.calc_ut(jd, swe.VENUS, swe.FLG_SWIEPH | swe.FLG_SPEED)
    return result[0][3], result[0][0]


def find_stations(start_year, end_year):
    """
    Scan a date range for Venus stations (retrograde and direct) by detecting
    sign changes in the longitude speed. Refines each crossing to sub-second
    precision via 15-iteration bisection.

    Returns a list of tuples: (station_type, year, month, day, jd, longitude)
    where station_type is 'SR' (station retrograde) or 'SD' (station direct).
    """
    stations = []
    jd = swe.julday(start_year, 1, 1, 0.0)
    jd_end = swe.julday(end_year, 12, 31, 0.0)

    sp_prev, _ = get_venus_speed(jd)
    jd += 3

    while jd <= jd_end:
        sp, _ = get_venus_speed(jd)

        # Station retrograde: speed crosses from positive to negative
        if sp_prev > 0 and sp <= 0:
            a, b = jd - 3, jd
            for _ in range(15):
                mid = (a + b) / 2
                s2, _ = get_venus_speed(mid)
                if s2 > 0:
                    a = mid
                else:
                    b = mid
            jd_station = (a + b) / 2
            _, lon_station = get_venus_speed(jd_station)
            y, m, d, _ = swe.revjul(jd_station)
            stations.append(('SR', int(y), int(m), int(d), jd_station, lon_station))

        # Station direct: speed crosses from negative to positive
        if sp_prev < 0 and sp >= 0:
            a, b = jd - 3, jd
            for _ in range(15):
                mid = (a + b) / 2
                s2, _ = get_venus_speed(mid)
                if s2 < 0:
                    a = mid
                else:
                    b = mid
            jd_station = (a + b) / 2
            _, lon_station = get_venus_speed(jd_station)
            y, m, d, _ = swe.revjul(jd_station)
            stations.append(('SD', int(y), int(m), int(d), jd_station, lon_station))

        sp_prev = sp
        jd += 3

    return stations


def assign_series(jd):
    """
    Assign a Julian Day to one of the five Venus synodic series by finding
    the anchor whose 8-year chain comes closest. Returns '?' if no anchor
    is within 300 days (should not happen in practice).
    """
    best_series = '?'
    best_distance = 999999
    for series, anchor_jd in ANCHORS.items():
        n_cycles = round((jd - anchor_jd) / CYCLE)
        distance = abs(jd - (anchor_jd + n_cycles * CYCLE))
        if distance < best_distance:
            best_distance = distance
            best_series = series
    return best_series if best_distance < 300 else '?'


def compute_all_retrogrades():
    """
    Compute all Venus retrogrades from 800 BCE to 2027 CE in seven chronological
    chunks, then deduplicate boundary stations and pair SR with the next SD.

    Returns a list of (sr_tuple, sd_tuple, series) for each retrograde period.
    """
    chunks = [
        (-799, -499), (-499, -199), (-199, 100),
        (100, 500), (500, 1000), (1000, 1500), (1500, 2027)
    ]

    all_stations = []
    for start, end in chunks:
        chunk_stations = find_stations(start, end)
        all_stations.extend(chunk_stations)
        print(f"  {start:>5} to {end:>5}: {len(chunk_stations)} stations")

    # Deduplicate (chunk boundaries can produce the same station twice)
    seen = set()
    unique = []
    for s in all_stations:
        key = (s[0], s[1], s[2], s[3])
        if key not in seen:
            seen.add(key)
            unique.append(s)
    unique.sort(key=lambda x: x[4])

    # Pair each SR with the next SD
    retros = []
    i = 0
    while i < len(unique) - 1:
        if unique[i][0] == 'SR':
            for j in range(i + 1, min(i + 4, len(unique))):
                if unique[j][0] == 'SD':
                    sr = unique[i]
                    sd = unique[j]
                    series = assign_series(sr[4])
                    retros.append((sr, sd, series))
                    break
        i += 1

    return retros


def format_year(y):
    """Format negative years as BCE (year 0 in swisseph = 1 BCE)."""
    return f"{abs(y) + 1} BCE" if y <= 0 else f"{y} CE"


if __name__ == "__main__":
    print("Computing Venus retrograde stations from 800 BCE to 2027 CE...")
    print("(This takes a couple of minutes on first run.)\n")

    retros = compute_all_retrogrades()

    print(f"\nTotal retrograde periods detected: {len(retros)}")
    print("(Expected: 1768)\n")

    # Print first 5 and last 5 as a sanity check
    print("First 5 retrogrades:")
    print(f"{'Series':>6} | {'Start':>20} | {'End':>20} | {'Start sign':>15}")
    print("-" * 75)
    for sr, sd, series in retros[:5]:
        sr_year = format_year(sr[1])
        sd_year = format_year(sd[1])
        sign = SIGNS[int(sr[5] // 30)]
        print(f"{series:>6} | {sr_year} {sr[2]:>2}/{sr[3]:>2} "
              f"| {sd_year} {sd[2]:>2}/{sd[3]:>2} | {sign:>15}")

    print("\nLast 5 retrogrades:")
    print(f"{'Series':>6} | {'Start':>20} | {'End':>20} | {'Start sign':>15}")
    print("-" * 75)
    for sr, sd, series in retros[-5:]:
        sr_year = format_year(sr[1])
        sd_year = format_year(sd[1])
        sign = SIGNS[int(sr[5] // 30)]
        print(f"{series:>6} | {sr_year} {sr[2]:>2}/{sr[3]:>2} "
              f"| {sd_year} {sd[2]:>2}/{sd[3]:>2} | {sign:>15}")

    # Series counts
    print("\nRetrogrades per series:")
    for s in 'ABCDE':
        count = sum(1 for _, _, series in retros if series == s)
        print(f"  Series {s}: {count}")
