# Data quality report — FlameGuard AI v2 (2026-10-30)

## What was selected and why
Verified core (10 records, from opened PDFs, for the first prototype as in Task 2):
BASS-II 2014 presentation, SAFFIRE-IV/V 2021, SAFFIRE-VI 2024, SPICE Dotson 2011, SPICE NASA summary, SoFIE-GEL extinction manuscript, SoFIE-GEL Task Book, SAME final report 2010, FLEX methanol 2013, FLEX detailed results 2015.
These were chosen because their PDFs are openly downloadable from NASA/NTRS/NIST, are ISS/Cygnus flight data (except summaries/task book, labelled as such), and cover the three core assignment investigations (BASS-II, SAFFIRE, SPICE) plus GEL, SAME and FLEX.

## Files accessed
- 11 core PDFs downloaded and opened, total 63,289,402 bytes in data/raw/ (including the 41 MB FLEX detailed report, 314 pages).
- PSI records verified live 2026-10-30: PSI-25 (255.77 GB total, DOI 10.60555/4qc4-de67, CC0-1.0), PSI-98 (11.41 GB, DOI 10.60555/0t15-1z43, CC0-1.0), PSI-107 (6.47 GB, DOI 10.60555/9kbh-e962, CC0-1.0). Whole PSI datasets were NOT downloaded.
- PSI search also found PSI-99 (SAFFIRE-II) and PSI-100 (SAFFIRE-III).
- Journal papers NOT opened (paywalled): Urban et al. 2019 (SAFFIRE I/III, DOI 10.1016/j.combustflame.2018.10.012), Olson & Ferkul 2017 (BASS-II rods, DOI 10.1016/j.combustflame.2017.03.001), James/T'ien GEL extinction-map journal paper 2025, FLEX cool-flame journal papers 2012/2015. Nothing from them is quoted.

## Records extracted
- Verified core: 10 records, 68 evidence passages, all under 40 words, all checked as contiguous text on the stated PDF page.
- Extended set: 176 headed entries, 0 new evidence passages in v2 (summary-level only, from earlier harvests).
- Evidence passages total in this package: 68.

## Fields available / missing (core)
- Available for all core records: title, investigation, source URL, file name/size, experiment conditions as stated in the PDF, evidence passages with page refs.
- Missing for most core records: full abstract (null for all 10), DOI (only SPICE Dotson has a DOI printed in its file; PSI rows have PSI DOIs), licence (null for all PDF records; CC0-1.0 only for PSI rows).
- Per-test tables: GEL Table 1 cases and SAFFIRE Table 1/2 per-test conditions are recorded in experiment_conditions; SAME Table 1 per-material values were noted but not transcribed in v2; FLEX per-test LOI tables were not transcribed (the detailed report states it does not interpret results).

## Cleaning and validation performed
- Passages checked by exact text search on the stated PDF page; two candidate passages in the SAME/FLEX pass that failed exact matching were dropped and replaced.
- File sizes, page counts, NTRS IDs and DOIs taken from the files/records themselves, not from summaries.
- Conflicts flagged, never averaged or merged (see below).
- Title-based deduplication of the extended set found 0 exact title+investigation duplicates, because standards entries use different entry titles for the same studies. True unique-study deduplication therefore still requires manual mapping and is NOT claimed in v2. The extended set must not be counted as 176 studies.

## Conflicts resolved in v2 from primary PDFs
- SAFFIRE per-test conditions (VI paper Table 1 p.3; IV/V paper Table 2 p.8, consistent): IV-1 SIBAL 22.0% O2 / 100.0 kPa; V-2 cotton 26.2% / 70.7 kPa; V-3 one-sided PMMA 25.4% O2; VI-2 SIBAL 31.0% / 54.1 kPa; VI-3 two-sided PMMA 30.3% / 54.6 kPa; VI-4 one-sided PMMA 28.8% / 55.2 kPa. Use these, not the 21% nominal or 23.1% secondary figures for IV-1, and not the 34% secondary figure for SAFFIRE-V.
- SAFFIRE-VI smoke detection: typical alarm threshold only achieved at 981 seconds (VI paper conclusion p.6; VI-3 discussion p.5).
- SAFFIRE-VI hazard ranking: temperature/pressure rise less significant than CO/CO2 increase; allowable CO2 exceeded by both PMMA tests (VI paper pp.2,5,6).
- FLEX report number: NASA/TP-2015-216046 (cover p.1, NTRS 20150023456), NOT 2013-216046 as cited in earlier summaries and in the methanol paper's reference list.
- SPICE counts kept separate: Dotson subset 55 smoke points; NASA summary 250 tests / >70 smoke points; PSI-107 record 526 flames / 470 table records. None is another.

## Conflicts still open (do not present as resolved)
- BASS-II wind-tunnel max: 40 cm/s (presentation p.3) vs 0-55 cm/s (p.7, same file).
- SAFFIRE duct height for I-III: 46 cm (IV/V Table 2 p.8) vs 50 cm implied by VI paper p.2 (half-height 25 cm). IV-VI value 30 cm agrees in both.
- SAFFIRE-VI scope: VI paper presents "one test" in its abstract but tables three successful ignitions (VI-2, VI-3, VI-4) plus a Nomex sample that did not ignite. The "19 runs" news figure is not in these PDFs.
- SAME 1.7x vs 1.9x diameter-of-average-mass factor: not in the passages extracted here, still open.
- SAFFIRE I/III spread rates from the 2019 journal paper: not extracted (paywalled).
- Current NASA-STD-6001 revision: not confirmed in v2; check standards.nasa.gov before citing as current.
- Test 1 criterion: 6 in / 15.2 cm in 6001 text vs 12 in in an older scenarios paper — version difference, do not merge.

## Licensing / access restrictions
- PSI rows: CC0-1.0 as shown on PSI records.
- PDF records: licence null where the file does not print a licence. NTRS "Public" distribution is an access note, not a licence, and is not recorded as one. One SAFFIRE file carries an NTRS note that portions may include copyright-protected material; passages from it are short (under 40 words) for that reason.
- Do not commit very large files to GitHub. The 41 MB FLEX detailed report is in this zip for completeness, but the team lead should decide whether it belongs in version control; the dataset JSON/CSV alone is sufficient for backend loading.

## What the AI must not conclude
See data_dictionary.md. In short: no safe/unsafe verdicts, no single cross-study limit, no fan-off = fire-out rule, no droplet/gas numbers as solid limits, no planned/simulated data as flight data.
