# Venus Retrograde and Forced Displacement: A Correlation Study

**Author:** Şira Nur Uysal
**Affiliation:** Independent researcher, classical astrology
**Contact:** info@sirauysal.com | [sirauysal.com](https://sirauysal.com)
**License:** MIT (code) / CC-BY-4.0 (data and paper)

---

This repository contains the data, code, and results for the study:

> **Venus Retrograde and Forced Displacement: A 2,750-Year Correlation Study with Ephemeris-Verified Control Groups**

The paper tests whether 82 documented forced displacement events (734 BCE – 2023 CE) cluster preferentially within one of the five 8-year Venus synodic series. The full paper is in `docs/paper.md` (English) and `docs/makale-tr.md` (Turkish).

## Summary of findings

- **No series reaches conventional statistical significance (p < 0.05).**
- Two series emerge above expected frequency: **Series B** (Capricorn, 22/82 nearest assignments, driven by the 1941–42 Holocaust cluster) and **Series E** (Scorpio-Libra, 17/82, broader historical distribution).
- The strongest single correlation is **Kristallnacht (9–10 November 1938)**, falling 10 days into a Series E retrograde.
- **Critical methodological finding:** expanding the database from 64 to 82 events shifted the dominant series from E to B, demonstrating the sensitivity of exploratory correlation studies to event selection. This sensitivity is itself the most robust finding.
- A subsequent independent replication using a much larger displacement database (n = 474, with a stricter ±6-day buffer definition of retrograde) found no significant correlation. See `docs/replication-notes.md`.

The study is presented as **exploratory**, not confirmatory.

---

## Repository contents

```
venus-retrograde-displacement/
├── README.md                       This file
├── LICENSE                         MIT for code, CC-BY-4.0 for data
├── requirements.txt                Python dependencies
├── data/
│   └── events_82.csv               The 82 displacement events
├── code/
│   ├── compute_retrogrades.py      Compute Venus retrograde periods
│   └── correlation_analysis.py     Run the four statistical tests
├── results/
│   └── output_log.txt              Expected output of correlation_analysis.py
└── docs/
    ├── paper.md                    Full English paper
    ├── makale-tr.md                Full Turkish paper
    └── replication-notes.md        Notes on the n=474 replication
```

## How to reproduce the analysis

### 1. Set up environment

```bash
pip install -r requirements.txt
```

Requires Python 3.9+ and `pyswisseph` 2.10.3 (Swiss Ephemeris bindings, Moshier analytical ephemeris).

### 2. Run the correlation analysis

```bash
python code/correlation_analysis.py > my_results.txt
```

This computes all 1,768 Venus retrograde periods between 800 BCE and 2027 CE, assigns each to one of five 8-year synodic series, matches each of the 82 displacement events to its nearest retrograde, and runs four statistical tests (chi-square, DIRECT+PROXIMATE frequency, Monte Carlo distance correlation, period-stratified analysis).

Compare your output against `results/output_log.txt`. They should match exactly except for floating-point Monte Carlo p-values (which are seeded for reproducibility).

### 3. Compute Venus retrograde periods only (no event matching)

```bash
python code/compute_retrogrades.py
```

This produces a list of all Venus retrograde stations (start retrograde, end retrograde) for the study period.

---

## Methodology summary

**Astronomical computation:**
- Library: `pyswisseph` 2.10.3
- Ephemeris: Moshier analytical (sub-arcminute accuracy across 2,827 years)
- Coordinate system: geocentric tropical longitude
- Station detection: 3-day Venus speed scan, 15-iteration bisection refinement
- Total retrograde periods identified: 1,768 (800 BCE – 2027 CE)

**Five Venus synodic series (anchored to 2020s retrogrades):**

| Series | 2020s anchor | Current sign |
|--------|--------------|--------------|
| A | 13 May 2020 | Gemini |
| B | 19 Dec 2021 | Capricorn |
| C | 23 Jul 2023 | Leo |
| D | 2 Mar 2025 | Aries |
| E | 3 Oct 2026 | Scorpio |

Each retrograde recurs approximately every 2,919.6 days (about 8 years), shifted roughly 2–3 degrees backward in zodiacal longitude.

**Event-retrograde matching levels:**

| Level | Definition |
|-------|-----------|
| DIRECT | Event occurs between station retrograde and station direct |
| PROXIMATE | Event within 30 days of either station |
| SAME YEAR | Event in the same calendar year as a series retrograde |
| FAR | No proximity |

**Statistical tests:**
1. Chi-square goodness-of-fit on nearest-retrograde series distribution
2. Chi-square on DIRECT+PROXIMATE frequency
3. Monte Carlo distance correlation (5,000 simulations, seed=42)
4. Period-stratified analysis (Ancient, Medieval, Early Modern, 19th c., 20th–21st c.)

---

## Limitations

This is a **post-hoc exploratory study**, not a confirmatory one:

- The hypothesis (clustering in Series E) was generated from the data, then tested on the same data
- Event selection is biased toward European, Middle Eastern, and post-1900 events, reflecting both better documentation and the author's expertise
- East Asian, sub-Saharan African, and pre-Columbian American forced displacements are underrepresented
- n = 82 is too small for stable conclusions, as demonstrated by the 64→82 sensitivity analysis
- A subsequent n = 474 replication with stricter retrograde definition produced a null result

These caveats are discussed in detail in §4 of the paper.

---

## Author note

The author has previously published an empirical study of 3,475 earthquakes against astrological parameters, finding no significant correlations (Uysal, 2026). The present work applies the same empirical ethos: the goal is to document what the data shows, including null and ambiguous results, rather than to confirm a predetermined thesis.

---

## How to cite

```
Uysal, Ş. N. (2026). Venus Retrograde and Forced Displacement:
A 2,750-Year Correlation Study with Ephemeris-Verified Control Groups.
Self-published, sirauysal.com.
GitHub: https://github.com/SiraU/venus-retrograde-displacement
```

---

## Acknowledgements

- Swiss Ephemeris team (Dieter Koch, Alois Treindl) for the computational tools
