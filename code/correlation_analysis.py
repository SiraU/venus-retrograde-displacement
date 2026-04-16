"""
correlation_analysis.py
=======================

Main correlation analysis. Reproduces the four statistical tests from the paper
"Venus Retrograde and Forced Displacement: A 2,750-Year Correlation Study"
(Uysal, 2026).

For each of the 82 displacement events in data/events_82.csv:
  1. Find the nearest Venus retrograde station
  2. Classify the temporal proximity as DIRECT / PROXIMATE / SAME YEAR / FAR
  3. Assign the matching retrograde to one of five 8-year synodic series

Then run four tests:
  Test 1: Chi-square goodness-of-fit on nearest-retrograde series distribution
  Test 2: Chi-square on DIRECT+PROXIMATE frequency
  Test 3: Monte Carlo distance correlation (5000 simulations, seed=42)
  Test 4: Period-stratified analysis

Usage:
  python correlation_analysis.py

Compare output against results/output_log.txt (should match exactly except
for floating-point rounding in the Monte Carlo p-values).

Requires: pyswisseph 2.10.3
"""

import csv
import os
import random
import swisseph as swe

from compute_retrogrades import (
    SIGNS, ANCHORS, CYCLE,
    compute_all_retrogrades, assign_series, format_year,
)

# Path to events CSV (relative to the repository root)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EVENTS_CSV = os.path.join(SCRIPT_DIR, '..', 'data', 'events_82.csv')


def load_events(csv_path):
    """Load (year, month, day, description) tuples from the CSV."""
    events = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append((
                int(row['year']),
                int(row['month']),
                int(row['day']),
                row['description'],
            ))
    return events


def find_nearest_retrograde(event_jd, retros):
    """
    Find the nearest Venus retrograde to the given event Julian Day.
    Returns (sr, sd, series, level, distance_in_days).

    Levels:
      DIRECT    - event falls between SR and SD
      PROX      - event within 30 days of either station
      YEAR      - event within 31-180 days
      FAR       - more than 180 days from any station
    """
    best = None
    best_distance = 999999
    best_series = '?'

    for sr, sd, series in retros:
        # DIRECT match: event during the retrograde period
        if sr[4] <= event_jd <= sd[4]:
            return sr, sd, series, 'DIRECT', 0

        distance = min(abs(event_jd - sr[4]), abs(event_jd - sd[4]))
        if distance < best_distance:
            best_distance = distance
            best = (sr, sd)
            best_series = series

    sr, sd = best
    if best_distance <= 30:
        level = 'PROX'
    elif best_distance <= 180:
        level = 'YEAR'
    else:
        level = 'FAR'

    return sr, sd, best_series, level, best_distance


def chi_square(observed, expected_each):
    """Compute chi-square statistic given observed counts and expected per cell."""
    return sum((o - expected_each) ** 2 / expected_each for o in observed)


def interpret_chi2_df4(chi2):
    """Return a verbal interpretation of chi-square with df=4."""
    if chi2 > 9.488:
        return "p < 0.05 SIGNIFICANT"
    elif chi2 > 7.779:
        return "p < 0.10 marginal"
    elif chi2 > 5.989:
        return "p < 0.20 weak"
    else:
        return "p > 0.20 not significant"


def min_distance_to_series(event_jd, series_retros):
    """Minimum distance (in days) from event_jd to any retrograde in this series."""
    min_dist = 999999
    for sr_jd, sd_jd in series_retros:
        if sr_jd <= event_jd <= sd_jd:
            return 0
        dist = min(abs(event_jd - sr_jd), abs(event_jd - sd_jd))
        if dist < min_dist:
            min_dist = dist
    return min_dist


def main():
    # ---- Step 1: compute all retrogrades ----
    print("=" * 80)
    print("Step 1: Computing all Venus retrograde stations (800 BCE to 2027 CE)")
    print("=" * 80)
    retros = compute_all_retrogrades()
    print(f"\nTotal retrograde periods: {len(retros)}\n")

    # Build per-series retrograde lists for the distance test
    series_retros = {s: [] for s in 'ABCDE'}
    for sr, sd, series in retros:
        if series in series_retros:
            series_retros[series].append((sr[4], sd[4]))

    # ---- Step 2: load events ----
    events = load_events(EVENTS_CSV)
    n_events = len(events)
    rel_path = os.path.relpath(EVENTS_CSV, start=os.path.dirname(SCRIPT_DIR))
    print(f"Loaded {n_events} displacement events from {rel_path}\n")

    # ---- Step 3: per-event matching ----
    print("=" * 80)
    print(f"Step 2: Event-to-nearest-retrograde matching (n={n_events})")
    print("=" * 80)

    counts = {s: {'DIRECT': 0, 'PROX': 0, 'YEAR': 0, 'FAR': 0} for s in 'ABCDE?'}
    nearest_count = {s: 0 for s in 'ABCDE?'}
    event_results = []

    print(f"\n{'Year':>10} | {'S':>1} | {'Match':>6} | {'Days':>4} | Event")
    print("-" * 90)

    for year, month, day, desc in events:
        event_jd = swe.julday(year, month, day, 12.0)
        sr, sd, series, level, distance = find_nearest_retrograde(event_jd, retros)
        counts[series][level] += 1
        nearest_count[series] += 1
        event_results.append((year, month, day, desc, series, level, distance))

        year_str = format_year(year)
        print(f"{year_str:>10} | {series:>1} | {level:>6} | "
              f"{int(distance):>4} | {desc[:60]}")

    # ---- Test 1: Chi-square on nearest-retrograde series distribution ----
    print(f"\n{'=' * 60}")
    print(f"Test 1: Nearest-retrograde series distribution (n={n_events})")
    print(f"{'=' * 60}")

    expected_each = n_events / 5.0
    observed = [nearest_count[s] for s in 'ABCDE']
    chi2_test1 = chi_square(observed, expected_each)

    print(f"\n{'Series':>6} | {'Observed':>8} | {'Expected':>8} | {'Diff':>6} | {'(O-E)squared/E':>15}")
    print("-" * 60)
    for s in 'ABCDE':
        o = nearest_count[s]
        diff = o - expected_each
        contrib = (o - expected_each) ** 2 / expected_each
        print(f"{s:>6} | {o:>8} | {expected_each:>8.1f} | "
              f"{diff:>+6.1f} | {contrib:>15.3f}")

    print(f"\nChi-square = {chi2_test1:.3f} (df=4)")
    print(f"  -> {interpret_chi2_df4(chi2_test1)}")

    # ---- Test 2: Chi-square on DIRECT+PROXIMATE frequency ----
    print(f"\n{'=' * 60}")
    print(f"Test 2: DIRECT+PROXIMATE frequency by series")
    print(f"{'=' * 60}")

    print(f"\n{'Series':>6} | {'DIRECT':>6} | {'PROX':>4} | {'YEAR':>4} | "
          f"{'FAR':>4} | {'D+P':>4}")
    print("-" * 50)
    for s in 'ABCDE':
        c = counts[s]
        dp = c['DIRECT'] + c['PROX']
        print(f"{s:>6} | {c['DIRECT']:>6} | {c['PROX']:>4} | {c['YEAR']:>4} | "
              f"{c['FAR']:>4} | {dp:>4}")

    dp_counts = [counts[s]['DIRECT'] + counts[s]['PROX'] for s in 'ABCDE']
    total_dp = sum(dp_counts)
    if total_dp >= 5:
        expected_dp = total_dp / 5.0
        chi2_test2 = chi_square(dp_counts, expected_dp)
        print(f"\nChi-square (D+P) = {chi2_test2:.3f} (df=4)")
        print(f"  -> {interpret_chi2_df4(chi2_test2)}")

    # ---- Test 3: Monte Carlo distance correlation ----
    print(f"\n{'=' * 60}")
    print(f"Test 3: Monte Carlo distance correlation (5000 sims, seed=42)")
    print(f"{'=' * 60}")

    # Compute observed mean distance from events to each series
    avg_distance = {}
    for s in 'ABCDE':
        distances = [
            min_distance_to_series(swe.julday(y, m, d, 12), series_retros[s])
            for y, m, d, _ in events
        ]
        avg_distance[s] = sum(distances) / len(distances)

    # Monte Carlo: random event dates uniformly distributed over study period
    min_jd = min(swe.julday(y, m, d, 12) for y, m, d, _ in events)
    max_jd = max(swe.julday(y, m, d, 12) for y, m, d, _ in events)
    random.seed(42)
    N_SIM = 5000

    print(f"\n{'Series':>6} | {'Obs mean':>9} | {'Expected':>9} | "
          f"{'p-value':>8} | {'Result':>15}")
    print("-" * 60)
    for s in 'ABCDE':
        sim_avgs = []
        for _ in range(N_SIM):
            random_jds = [random.uniform(min_jd, max_jd) for _ in range(n_events)]
            random_dists = [
                min_distance_to_series(rj, series_retros[s]) for rj in random_jds
            ]
            sim_avgs.append(sum(random_dists) / len(random_dists))
        mean_sim = sum(sim_avgs) / len(sim_avgs)
        p = sum(1 for x in sim_avgs if x <= avg_distance[s]) / N_SIM

        if p < 0.05:
            verdict = "SIGNIFICANT"
        elif p < 0.10:
            verdict = "marginal"
        else:
            verdict = "not significant"

        print(f"{s:>6} | {avg_distance[s]:>7.0f}d | {mean_sim:>7.0f}d | "
              f"{p:>8.4f} | {verdict:>15}")

    # ---- Test 4: Period-stratified analysis ----
    print(f"\n{'=' * 60}")
    print(f"Test 4: Period-stratified series distribution")
    print(f"{'=' * 60}")

    periods = [
        ("Ancient (734 BCE - 415 CE)", -734, 416),
        ("Medieval (1096-1421)", 1096, 1422),
        ("Early Modern (1492-1755)", 1492, 1756),
        ("19th century (1821-1913)", 1821, 1914),
        ("20th-21st century (1915-2023)", 1915, 2024),
    ]

    for period_name, p_start, p_end in periods:
        period_events = [
            (y, m, d, desc) for y, m, d, desc in events
            if p_start <= y < p_end
        ]
        if not period_events:
            continue

        period_counts = {s: 0 for s in 'ABCDE?'}
        for y, m, d, _ in period_events:
            event_jd = swe.julday(y, m, d, 12)
            _, _, series, _, _ = find_nearest_retrograde(event_jd, retros)
            period_counts[series] += 1

        print(f"\n  {period_name} (n={len(period_events)}):")
        for s in 'ABCDE':
            bar = '#' * period_counts[s]
            print(f"    {s}: {period_counts[s]:>2} {bar}")

    # ---- Summary ----
    print(f"\n{'=' * 80}")
    print("Summary of paper's main findings")
    print(f"{'=' * 80}")
    print(f"  No test reaches p < 0.05.")
    print(f"  Series B and Series E both exceed expected frequency.")
    print(f"  Strongest single correlation: Kristallnacht (1938-11-09), Series E.")
    print(f"  See docs/paper.md or docs/makale-tr.md for full discussion.")
    print(f"  See docs/replication-notes.md for the n=474 follow-up null result.")


if __name__ == "__main__":
    main()
