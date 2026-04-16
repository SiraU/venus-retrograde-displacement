# Replication Notes: The n=474 Follow-Up Study

This document records a follow-up replication attempt conducted after the original n=82 paper. It is included here in the interest of full transparency.

## Summary

The original paper (n=82) found no statistically significant series-level effect, but reported that two series (B and E) were elevated above expectation, with the strongest individual correlation being Kristallnacht (1938) falling within a Series E retrograde.

A follow-up replication built a much larger displacement event database (n=474, spanning 1066–2024 CE) and re-ran the test using a stricter retrograde definition. **The replication produced a clear null result.**

## What changed

| Aspect | Original paper (n=82) | Replication (n=474) |
|--------|----------------------|--------------------|
| Date range | 734 BCE – 2023 CE | 1066–2024 CE |
| Event count | 82 | 474 |
| Retrograde definition | Strict (between SR and SD only) | Strict + ±6-day buffer at each station |
| Baseline retrograde probability | ~7.19% | ~9.27% |
| Geographic scope | Selected major events | Wikipedia "List of ethnic cleansing campaigns" + expansions |

The buffer addition reflects the classical observation that retrograde-related effects often manifest in the shadow period immediately around the stations, not only between them. Adding ±6 days raised the chance baseline from ~7.2% to ~9.3% per event.

## Results of the replication

### Full n=474 sample (with ±6-day buffer)

| Test | Observed retrogrades | Expected | Ratio | z-score |
|------|---------------------|----------|-------|---------|
| All 474 events | 43/474 = 9.07% | 43.9 | 0.98x | -0.15 |
| "High-confidence" subset (n=310) | 31/310 = 10.00% | 28.8 | 1.08x | +0.44 |

Neither result is statistically distinguishable from chance.

### Replication using the original paper's strict definition (no buffer)

To check whether the buffer was driving the difference, the replication was re-run with the original paper's strict retrograde definition (no shadow-period buffer, ~7.19% baseline):

| Test | n | Retrograde events | Ratio | p |
|------|---|-------------------|-------|---|
| Original paper's 82 events | 82 | 11 | 1.87x | 0.033 |
| Replication n=474 (strict) | 474 | 35 | 1.03x | 0.461 |
| Replication "high-confidence" 310 (strict) | 310 | 25 | 1.12x | 0.306 |

The signal does not survive in the larger sample.

### What about the original 11 retrograde events?

All 11 of the original paper's "DIRECT" retrograde matches (Assyria 734 BCE, Antiochus 167 BCE, Rhineland 1096, Jerusalem 1099, Cromwell 1652, Russia 1881, Nuremberg 1935, Kristallnacht 1938, Wannsee 1942, Internment 1942, Baku 1990) remain in retrograde periods in the n=474 analysis. The signal at n=82 was not produced by errors in event-retrograde matching; it was produced by the **selection** of events.

When the database is expanded to include hundreds of equally well-documented displacement events that the author had not initially selected, the signal washes out toward chance.

## Subgroup analysis (post-hoc, exploratory)

A post-hoc subgroup analysis on pogroms within the n=474 dataset showed marginal significance:

- Original 62 pogrom subset: 10/62 = 16.1%, ratio 1.74x, p = 0.058 (marginal)

A second replication added 37 newly compiled pogroms from the same period, drawn from independent sources:

- New 37-pogrom subset: 3/37 = 8.1%, ratio 0.87x, p = 0.679 (null)
- Combined 99 pogroms: 13/99 = 13.1%, ratio 1.42x, p = 0.127 (not significant)

The marginal pogrom signal in the original subset did not replicate in the independently compiled extension.

## Period-stratified pattern (suggestive, requires testing)

A separate intermediate dataset (n=384) showed a notable period-stratified pattern that the n=82 paper also exhibited:

| Period | Retro/n | Ratio |
|--------|---------|-------|
| 19th century (1801-1913) | 7/52 = 13.5% | 1.89x |
| Interbellum-WWII (1924-1945) | 8/78 = 10.3% | 1.43x |
| Post-Cold-War (1990-1999) | 4/40 = 10.0% | 1.39x |
| Cold War (1946-1989) | 3/89 = 3.4% | 0.47x |

The pre-modern (19th c. + WWII-era) signal is approximately 1.7-1.9x baseline, while the Cold War period is well below baseline (0.47x). This bimodal pattern explains why aggregating all periods yields a ratio close to 1.0.

This period-stratified pattern is **consistent across multiple independent dataset compilations** but has not been formally tested with pre-registered hypotheses on independent data. It is a candidate for follow-up work, not a finding.

## Honest assessment

The original n=82 paper's main numerical claim (Series B and E elevated, Kristallnacht in Series E) is reproducible from the supplied data and code. However, the n=474 replication shows that the elevation does not survive sample expansion, and the original paper's own "sensitivity finding" (the dominant series shifted from E to B when n grew from 64 to 82) was an early warning of this instability.

The author's previous earthquake study (Uysal, 2026) similarly produced a null result on a much larger sample (n=3,475). The pattern is consistent: **astrological signals that appear in small, post-hoc samples tend to disappear when tested on larger, independently compiled databases.**

This replication is included in the repository so that any reader can see the full picture, not only the original paper's positive-leaning summary.

## Future work

A genuinely confirmatory test would require:
- Pre-registration of the specific hypothesis to be tested
- An independently compiled event database (not curated by the same researcher who proposed the hypothesis)
- A pre-specified definition of "retrograde proximity" with no post-hoc buffer adjustments
- A sample size large enough to detect plausible effect sizes (probably n > 200)
- Cross-validation across multiple planetary cycles (Mars retrograde, Saturn-Neptune, eclipse families)

Until such a test is conducted, the present study should be read as **exploratory pattern-finding**, not as evidence that Venus retrograde correlates with forced displacement.

---

*Author: Şira Nur Uysal*
*Last updated: April 2026*
