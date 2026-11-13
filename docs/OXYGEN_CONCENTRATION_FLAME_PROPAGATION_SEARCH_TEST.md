# Real-World Search Test 03: Oxygen Concentration & Flame Propagation

## Test scope and preservation

This report records a read-only execution of the existing FlameGuard AI search services. No production code, ranking logic, datasets, benchmark fixtures, search configuration, stash, or Git history was modified. No NASA PDFs were downloaded. Relevance assessments are provisional QA assessments, not expert scientific judgments.

Execution date: 2026-10-31. NASA retrieval timestamps are preserved on each returned NASA record.

## Search methods and scientific evidence rules

- **Local:** `build_evidence_brief(query, limit=5)` against the local research intelligence store.
- **Combined:** `search_research_with_fallback(query, limit=5)`; local first, NASA NTRS only when configured local sufficiency checks fail.
- **BASS-II:** `search_bass2_records(query, limit=5)` run separately using the existing dataset schema.
- NASA records are catalogue metadata and abstracts only: `evidence_type=bibliographic_metadata_and_abstract`, `scientific_findings_verified=false`, and `review_status=not_scientifically_reviewed`.
- Mentioning oxygen is not evidence of a quantitative oxygen measurement, an extinction threshold, or a causal flame-propagation relationship.
- Repeated source IDs represent multiple passages from one research source, not independent papers.

## 1. Effect of oxygen concentration on flame propagation

- **Local result count:** 5
- **NASA NTRS result count:** 0; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 5
- **Unique independent local/NASA source count:** 4
- **Duplicate source count:** 1
- **Latency:** local `171.72 ms`; combined/NASA `14.44 ms`; BASS-II `17.24 ms`
- **NASA fallback:** not triggered; reason: local evidence met configured sufficiency thresholds

### Actual local results (top five)

1. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.48`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Thin Fuel: 1.1 Spread Rate: The experimental flame spread rates, Vf.,_,, over the thin cellulosic fuel in five different quiescent environments, at three different ambient pressures and two oxygen levels, are plotted in Fig.
   - Match explanation: matched terms: flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.48`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: However, one of the most important results is that, in microgravity, the extinction of the polyethylene occurs almost immediately when the flow of relatively low oxygen concentration (C = 21 percent) stops.
   - Match explanation: matched terms: concentration, oxygen; scientific concepts: oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: effect, flame; scientific concepts: flame spread
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Passage: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the measure the soot concentration (laser extinction) andmaterial.
   - Match explanation: matched terms: concentration, flame; scientific concepts: flame spread, oxygen concentration
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.48`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: concentration, oxygen; scientific concepts: oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

### Actual NASA NTRS fallback results (top five)

No NASA NTRS records were returned or fallback was not requested.

### Actual BASS-II results

No BASS-II records matched this query. The BASS-II dataset was searched without inventing fields for extinction, gravity, pressure, or temperature.

### Query-specific relevance and condition assessment

- A result was treated as potentially relevant only when its returned title/excerpt/abstract addressed oxygen, flame propagation/spread/extinction, and the requested material or environment.
- Oxygen mentions without a numeric concentration, measurement context, comparison, or extinction condition were explicitly treated as insufficient for a quantitative oxygen claim.
- PMMA-specific queries require PMMA evidence; generic solid-fuel or spacecraft passages are not interchangeable with PMMA.
- Spacecraft oxygen-availability queries require spacecraft/environment context; generic combustion evidence is not spacecraft-specific evidence.
- Multiple passages with one NASA/source ID were counted as one independent source for diversity purposes.

## 2. Oxygen concentration and flame spread in microgravity

- **Local result count:** 5
- **NASA NTRS result count:** 0; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 5
- **Unique independent local/NASA source count:** 4
- **Duplicate source count:** 1
- **Latency:** local `24.82 ms`; combined/NASA `16.65 ms`; BASS-II `21.77 ms`
- **NASA fallback:** not triggered; reason: local evidence met configured sufficiency thresholds

### Actual local results (top five)

1. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.57`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: N96- 15553 Solid Surface Combustion Experiment Flame Spread in a Quiescent, Microgravity Environment Implications of Spread Rate and Flame Structure Matthew Bundy, Jeff West, Peter C.
   - Match explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.57`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: However, one of the most important results is that, in microgravity, the extinction of the polyethylene occurs almost immediately when the flow of relatively low oxygen concentration (C = 21 percent) stops.
   - Match explanation: matched terms: concentration, microgravity, oxygen; scientific concepts: microgravity, oxygen concentration; conditions: microgravity, oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Passage: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the measure the soot concentration (laser extinction) andmaterial.
   - Match explanation: matched terms: concentration, flame; scientific concepts: flame spread, oxygen concentration
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

5. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.57`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Thin Fuel: 1.1 Spread Rate: The experimental flame spread rates, Vf.,_,, over the thin cellulosic fuel in five different quiescent environments, at three different ambient pressures and two oxygen levels, are plotted in Fig.
   - Match explanation: matched terms: flame, oxygen, spread; scientific concepts: flame spread, oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

### Actual NASA NTRS fallback results (top five)

No NASA NTRS records were returned or fallback was not requested.

### Actual BASS-II results

No BASS-II records matched this query. The BASS-II dataset was searched without inventing fields for extinction, gravity, pressure, or temperature.

### Query-specific relevance and condition assessment

- A result was treated as potentially relevant only when its returned title/excerpt/abstract addressed oxygen, flame propagation/spread/extinction, and the requested material or environment.
- Oxygen mentions without a numeric concentration, measurement context, comparison, or extinction condition were explicitly treated as insufficient for a quantitative oxygen claim.
- PMMA-specific queries require PMMA evidence; generic solid-fuel or spacecraft passages are not interchangeable with PMMA.
- Spacecraft oxygen-availability queries require spacecraft/environment context; generic combustion evidence is not spacecraft-specific evidence.
- Multiple passages with one NASA/source ID were counted as one independent source for diversity purposes.

## 3. Limiting oxygen concentration for flame extinction

- **Local result count:** 5
- **NASA NTRS result count:** 0; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 5
- **Unique independent local/NASA source count:** 4
- **Duplicate source count:** 1
- **Latency:** local `14.95 ms`; combined/NASA `17.54 ms`; BASS-II `17.71 ms`
- **NASA fallback:** not triggered; reason: local evidence met configured sufficiency thresholds

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.57`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: However, one of the most important results is that, in microgravity, the extinction of the polyethylene occurs almost immediately when the flow of relatively low oxygen concentration (C = 21 percent) stops.
   - Match explanation: matched terms: concentration, extinction, oxygen; scientific concepts: oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

2. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.52`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Passage: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the measure the soot concentration (laser extinction) andmaterial.
   - Match explanation: matched terms: concentration, extinction, flame; scientific concepts: flame spread, oxygen concentration
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

3. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.48`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Thin Fuel: 1.1 Spread Rate: The experimental flame spread rates, Vf.,_,, over the thin cellulosic fuel in five different quiescent environments, at three different ambient pressures and two oxygen levels, are plotted in Fig.
   - Match explanation: matched terms: flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

4. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.34`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: flame; scientific concepts: flame spread
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.57`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: concentration, limiting, oxygen; scientific concepts: oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

### Actual NASA NTRS fallback results (top five)

No NASA NTRS records were returned or fallback was not requested.

### Actual BASS-II results

No BASS-II records matched this query. The BASS-II dataset was searched without inventing fields for extinction, gravity, pressure, or temperature.

### Query-specific relevance and condition assessment

- A result was treated as potentially relevant only when its returned title/excerpt/abstract addressed oxygen, flame propagation/spread/extinction, and the requested material or environment.
- Oxygen mentions without a numeric concentration, measurement context, comparison, or extinction condition were explicitly treated as insufficient for a quantitative oxygen claim.
- PMMA-specific queries require PMMA evidence; generic solid-fuel or spacecraft passages are not interchangeable with PMMA.
- Spacecraft oxygen-availability queries require spacecraft/environment context; generic combustion evidence is not spacecraft-specific evidence.
- Multiple passages with one NASA/source ID were counted as one independent source for diversity purposes.

## 4. Effect of oxygen percentage on solid material combustion

- **Local result count:** 5
- **NASA NTRS result count:** 1; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 6
- **Unique independent local/NASA source count:** 4
- **Duplicate source count:** 2
- **Latency:** local `18.8 ms`; combined/NASA `3980.0 ms`; BASS-II `36.71 ms`
- **NASA fallback:** triggered; reason: insufficient_local_source_coverage

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: TABLE 1.2.--GROUND-TESTING RESULTS OF U.S.-PROVIDED MATERIAL FLAMMABILITY -- LIMITING VELOCITY [Vb,,,' ) DETERMINED IN APPARATUSES WITH SUPPRESSED CONVECTION Number Material Vi.., cm/sec Narrow channel Vertical combustion chamber C =21% C =23% Q=21% Low-density Polyethylene 16.9 6.8 HiLzh-density Polyethylene 8.3 3.6 4.5 3 PMMA 3.3 2.3 1.1 4 Delrin 0.5 0.3 1.1 Nylon 6/6 16.4 5.3 R iLzid Polyurethane 15.5 4.7 Glass-epoxy composite >25 >25 TABLE 1.3.--GROUND-TESTING RESULTS OF U.S.-PROVIDED MATERIAL FLAMMABILITY- FLA
   - Match explanation: matched terms: combustion, material; scientific concepts: polyethylene, solid fuel combustion; material: polyethylene
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

2. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.1`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: N96- 15553 Solid Surface Combustion Experiment Flame Spread in a Quiescent, Microgravity Environment Implications of Spread Rate and Flame Structure Matthew Bundy, Jeff West, Peter C.
   - Match explanation: matched terms: combustion, solid; scientific concepts: solid fuel combustion; material mismatch penalty
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.0813`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Passage: From the figure, it is seen that as ambient pressure is reduced, the flame spread rate over the solid approaches that obtained at standard ambient pressure (100 kPa) in reduced gravity.
   - Match explanation: matched terms: solid; scientific concepts: solid fuel combustion; material mismatch penalty
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

4. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.525`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: However, one of the most important results is that, in microgravity, the extinction of the polyethylene occurs almost immediately when the flow of relatively low oxygen concentration (C = 21 percent) stops.
   - Match explanation: matched terms: oxygen; scientific concepts: oxygen concentration, polyethylene; material: polyethylene; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.475`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: The rates of material burning-out for Russian-made PMMA and polyethylene are less than 0.05 mm/s at a flow velocity V = 10 cm/s and C, x= 21 percent, i.e., 5 to 10 times lower than the flame-spread rates measured for the melting materials that were tested.
   - Match explanation: matched terms: material; scientific concepts: polyethylene; material: polyethylene
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

### Actual NASA NTRS fallback results (top five)

1. **Solid Inflammability Boundary at Low-Speed (SIBAL)** ? NASA ID `20010073996`; score `0.1875`; URL: https://ntrs.nasa.gov/citations/20010073996; retrieved `2026-10-31T09:37:51.023248+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: This research program is concerned with the effect of low-speed, concurrent flow on the spreading and extinction processes of flames over solid fuels. The primary objective is to verify the theoretically predicted extinction boundary, using oxygen percentage and flow velocity as coordinates. Of particular interest are the low-speed quenching limits and the existence of the critical oxygen flammability limit. Detailed flame spread characteristics, including flame spread rate, flame size, and flame structure are soug
   - Oxygen-condition check: oxygen-related wording appears, but no threshold or causal finding is accepted from metadata/abstract alone.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

### Actual BASS-II results

No BASS-II records matched this query. The BASS-II dataset was searched without inventing fields for extinction, gravity, pressure, or temperature.

### Query-specific relevance and condition assessment

- A result was treated as potentially relevant only when its returned title/excerpt/abstract addressed oxygen, flame propagation/spread/extinction, and the requested material or environment.
- Oxygen mentions without a numeric concentration, measurement context, comparison, or extinction condition were explicitly treated as insufficient for a quantitative oxygen claim.
- PMMA-specific queries require PMMA evidence; generic solid-fuel or spacecraft passages are not interchangeable with PMMA.
- Spacecraft oxygen-availability queries require spacecraft/environment context; generic combustion evidence is not spacecraft-specific evidence.
- Multiple passages with one NASA/source ID were counted as one independent source for diversity purposes.

## 5. Oxygen concentration effects on PMMA flame spread

- **Local result count:** 5
- **NASA NTRS result count:** 4; error: `none`
- **BASS-II result count:** 5
- **Final combined local/NASA record count:** 9
- **Unique independent local/NASA source count:** 8
- **Duplicate source count:** 1
- **Latency:** local `43.75 ms`; combined/NASA `3904.96 ms`; BASS-II `32.23 ms`
- **NASA fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage, required_experimental_conditions_not_covered, required_scientific_concepts_not_covered

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.625`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: The rates of material burning-out for Russian-made PMMA and polyethylene are less than 0.05 mm/s at a flow velocity V = 10 cm/s and C, x= 21 percent, i.e., 5 to 10 times lower than the flame-spread rates measured for the melting materials that were tested.
   - Match explanation: matched terms: flame, pmma, spread; scientific concepts: flame spread, polymethyl methacrylate; material: polymethyl methacrylate
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

2. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.1313`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Thin Fuel: 1.1 Spread Rate: The experimental flame spread rates, Vf.,_,, over the thin cellulosic fuel in five different quiescent environments, at three different ambient pressures and two oxygen levels, are plotted in Fig.
   - Match explanation: matched terms: flame, oxygen, spread; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; material mismatch penalty
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.1187`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: effect, flame, spread; scientific concepts: flame spread; material mismatch penalty
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.1`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Passage: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the measure the soot concentration (laser extinction) andmaterial.
   - Match explanation: matched terms: concentration, flame; scientific concepts: flame spread, oxygen concentration; material mismatch penalty
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.625`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: TABLE 1.2.--GROUND-TESTING RESULTS OF U.S.-PROVIDED MATERIAL FLAMMABILITY -- LIMITING VELOCITY [Vb,,,' ) DETERMINED IN APPARATUSES WITH SUPPRESSED CONVECTION Number Material Vi.., cm/sec Narrow channel Vertical combustion chamber C =21% C =23% Q=21% Low-density Polyethylene 16.9 6.8 HiLzh-density Polyethylene 8.3 3.6 4.5 3 PMMA 3.3 2.3 1.1 4 Delrin 0.5 0.3 1.1 Nylon 6/6 16.4 5.3 R iLzid Polyurethane 15.5 4.7 Glass-epoxy composite >25 >25 TABLE 1.3.--GROUND-TESTING RESULTS OF U.S.-PROVIDED MATERIAL FLAMMABILITY- FLA
   - Match explanation: matched terms: flame, pmma, spread; scientific concepts: flame spread, polymethyl methacrylate; material: polymethyl methacrylate
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

### Actual NASA NTRS fallback results (top five)

1. **Flow Effects on the Flammability Diagrams of Solid Fuels: Microgravity Influence on Ignition Delay** ? NASA ID `19990053973`; score `0.9`; URL: https://ntrs.nasa.gov/citations/19990053973; retrieved `2026-10-31T09:37:55.085996+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: The possibility of an accidental fire in space-based facilities is a primary concern of space exploration programs. Spacecraft environments generally present low velocity air currents produced by ventilation and heating systems (of the order of 0.1 m/s), and fluctuating oxygen concentrations around that of air due to CO2 removal systems. Recent experiments of flame spread in microgravity show the spread rate to be faster and the limiting oxygen concentration lower than in normal-gravity. To date, there is not a mat
   - Oxygen-condition check: oxygen-related wording appears, but no threshold or causal finding is accepted from metadata/abstract alone.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

2. **Strategic Research to Enable NASA's Exploration Missions Conference and Workshop: Poster Session** ? NASA ID `20040161185`; score `0.0187`; URL: https://ntrs.nasa.gov/citations/20040161185; retrieved `2026-10-31T09:37:55.085996+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Reports are presented from volume 2 of the conference titled Strategic Research to Enable NASA's Exploration Missions, poster session. Topics included spacecraft fire suppression and fire extinguishing agents,materials flammability, various topics on the effects of microgravity including crystal growth, fluid mechanics, electric particulate suspension, melting and solidification, bubble formation, the sloshing of liquid fuels, biological studies, separation of carbon dioxide and carbon monoxide for Mars ISRU.
   - Oxygen-condition check: no explicit oxygen measurement is visible in the returned abstract excerpt.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

3. **Strategic Research to Enable NASA's Exploration Missions Conference** ? NASA ID `20040084137`; score `0.0187`; URL: https://ntrs.nasa.gov/citations/20040084137; retrieved `2026-10-31T09:37:55.085996+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Abstracts are presented from a conference sponsored by the NASA Office of Biological and Physical Research and hosted by NASA Glenn Research Center and the National Center for Microgravity Research on Fluids and Combustion, held in Cleveland, Ohio, June 22-23, 2004. Topics pertained to the behavior of processes and materials in microgravity as well as physiological-biological studies and microgravity effects.
   - Oxygen-condition check: no explicit oxygen measurement is visible in the returned abstract excerpt.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

4. **The 3rd International Microgravity Combustion Workshop** ? NASA ID `19960008386`; score `0.0`; URL: https://ntrs.nasa.gov/citations/19960008386; retrieved `2026-10-31T09:37:55.085996+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: This Conference Publication contains 71 papers presented at the Third International Microgravity Combustion Workshop held in Cleveland, Ohio, from April 11 to 13, 1995. The purpose of the workshop was twofold: to exchange information about the progress and promise of combustion science in microgravity and to provide a forum to discuss which areas in microgravity combustion science need to be expanded profitably and which should be included in upcoming NASA Research Announcements (NRA).
   - Oxygen-condition check: no explicit oxygen measurement is visible in the returned abstract excerpt.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

### Actual BASS-II results

1. **PI `Bhattacharjee`, Test `B1`, material `100 micron PMMA film   2 cm wide`**; score `0.475`; matched terms `pmma`; available oxygen/combustion fields: `{'Calibrated  initial O2 % by vol ': '22.2', 'Calibrated final O2 % by vol': '22.2', 'Initial CO2 % by vol': '0.44', 'Final CO2 % by vol': '0.44', 'Initial CO (ppm)': '0', 'Final CO (ppm)': '6', 'Total Frames Shot': '57', 'Fan display': '62', 'Air display': '5', 'Flow restrictor': '2'}`.
   - Assessment: **Partially relevant or insufficient information** unless the returned structured record is independently linked to the requested propagation question. These fields are measurements/metadata in the source dataset, not an automatically verified causal conclusion.

2. **PI `Bhattacharjee`, Test `B2`, material `200 micron PMMA film   2 cm wide`**; score `0.475`; matched terms `pmma`; available oxygen/combustion fields: `{'Calibrated  initial O2 % by vol ': '22.2', 'Calibrated final O2 % by vol': '1.6', 'Initial CO2 % by vol': '0.44', 'Final CO2 % by vol': '', 'Initial CO (ppm)': '6', 'Final CO (ppm)': '', 'Total Frames Shot': 'none', 'Fan display': '62', 'Air display': '5', 'Flow restrictor': '2'}`.
   - Assessment: **Partially relevant or insufficient information** unless the returned structured record is independently linked to the requested propagation question. These fields are measurements/metadata in the source dataset, not an automatically verified causal conclusion.

3. **PI `Bhattacharjee`, Test `B4`, material `300 micron PMMA film   2 cm wide `**; score `0.475`; matched terms `pmma`; available oxygen/combustion fields: `{'Calibrated  initial O2 % by vol ': '22.2', 'Calibrated final O2 % by vol': '22.2', 'Initial CO2 % by vol': '0.44', 'Final CO2 % by vol': '0.51', 'Initial CO (ppm)': '-1', 'Final CO (ppm)': '10', 'Total Frames Shot': '137', 'Fan display': '61', 'Air display': '5', 'Flow restrictor': '2'}`.
   - Assessment: **Partially relevant or insufficient information** unless the returned structured record is independently linked to the requested propagation question. These fields are measurements/metadata in the source dataset, not an automatically verified causal conclusion.

4. **PI `Bhattacharjee`, Test `B6`, material `2 cm 0.1 mm PMMA film`**; score `0.475`; matched terms `pmma`; available oxygen/combustion fields: `{'Calibrated  initial O2 % by vol ': '21', 'Calibrated final O2 % by vol': '20.9', 'Initial CO2 % by vol': '0.33', 'Final CO2 % by vol': '0.41', 'Initial CO (ppm)': '0', 'Final CO (ppm)': '0.3', 'Total Frames Shot': '80', 'Fan display': '0.9   1.3   2.75', 'Air display': '3   5   approaching 10', 'Flow restrictor': '2'}`.
   - Assessment: **Partially relevant or insufficient information** unless the returned structured record is independently linked to the requested propagation question. These fields are measurements/metadata in the source dataset, not an automatically verified causal conclusion.

5. **PI `Bhattacharjee`, Test `B8`, material `2 cm   0.2 mm PMMA film`**; score `0.475`; matched terms `pmma`; available oxygen/combustion fields: `{'Calibrated  initial O2 % by vol ': '21', 'Calibrated final O2 % by vol': '20.5', 'Initial CO2 % by vol': '0.33', 'Final CO2 % by vol': '0.58', 'Initial CO (ppm)': '0', 'Final CO (ppm)': '131', 'Total Frames Shot': '226', 'Fan display': '1.4    incr to 10.0', 'Air display': '10   max', 'Flow restrictor': '0'}`.
   - Assessment: **Partially relevant or insufficient information** unless the returned structured record is independently linked to the requested propagation question. These fields are measurements/metadata in the source dataset, not an automatically verified causal conclusion.

### Query-specific relevance and condition assessment

- A result was treated as potentially relevant only when its returned title/excerpt/abstract addressed oxygen, flame propagation/spread/extinction, and the requested material or environment.
- Oxygen mentions without a numeric concentration, measurement context, comparison, or extinction condition were explicitly treated as insufficient for a quantitative oxygen claim.
- PMMA-specific queries require PMMA evidence; generic solid-fuel or spacecraft passages are not interchangeable with PMMA.
- Spacecraft oxygen-availability queries require spacecraft/environment context; generic combustion evidence is not spacecraft-specific evidence.
- Multiple passages with one NASA/source ID were counted as one independent source for diversity purposes.

## 6. Oxygen availability and spacecraft fire propagation

- **Local result count:** 5
- **NASA NTRS result count:** 0; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 5
- **Unique independent local/NASA source count:** 4
- **Duplicate source count:** 1
- **Latency:** local `33.15 ms`; combined/NASA `28.8 ms`; BASS-II `29.22 ms`
- **NASA fallback:** not triggered; reason: local evidence met configured sufficiency thresholds

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.48`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: oxygen, spacecraft; scientific concepts: oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

2. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.39`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Thin Fuel: 1.1 Spread Rate: The experimental flame spread rates, Vf.,_,, over the thin cellulosic fuel in five different quiescent environments, at three different ambient pressures and two oxygen levels, are plotted in Fig.
   - Match explanation: matched terms: oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.34`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `simulation`; review `requires_manual_review`.
   - Passage: It should be noted that under this condition only partial burning of the sample near the igniter region was observed in the FDS simulations done at 50 kPa, and the flame would eventually blow off about 11 mm away from the igniter, thus no spread rate was determined for that condition due to the very short propagation length.
   - Match explanation: matched terms: propagation; scientific concepts: flame spread
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.34`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Considering that the initial purpose of the computed from a Monte Carlo propagation analysis, images recorded during the experiments was to use considering a conservative error of 5% on the signal the data to visualize the flame and track its evolu- ratio ΘG/R, resulting in 117 K of uncertainty for tem- tion over time, i.e., pyrolysis length, flame size, etc., perature determination.
   - Match explanation: matched terms: propagation; scientific concepts: flame spread
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: NUMBER OF PAGES 62 Extinction; Fire safety; Flammability; Flammability limits; Flame propagation; 16.
   - Match explanation: matched terms: fire, propagation; scientific concepts: flame spread
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

### Actual NASA NTRS fallback results (top five)

No NASA NTRS records were returned or fallback was not requested.

### Actual BASS-II results

No BASS-II records matched this query. The BASS-II dataset was searched without inventing fields for extinction, gravity, pressure, or temperature.

### Query-specific relevance and condition assessment

- A result was treated as potentially relevant only when its returned title/excerpt/abstract addressed oxygen, flame propagation/spread/extinction, and the requested material or environment.
- Oxygen mentions without a numeric concentration, measurement context, comparison, or extinction condition were explicitly treated as insufficient for a quantitative oxygen claim.
- PMMA-specific queries require PMMA evidence; generic solid-fuel or spacecraft passages are not interchangeable with PMMA.
- Spacecraft oxygen-availability queries require spacecraft/environment context; generic combustion evidence is not spacecraft-specific evidence.
- Multiple passages with one NASA/source ID were counted as one independent source for diversity purposes.

## 7. NASA experiments on oxygen concentration and flame behavior

- **Local result count:** 5
- **NASA NTRS result count:** 5; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 10
- **Unique independent local/NASA source count:** 9
- **Duplicate source count:** 1
- **Latency:** local `32.47 ms`; combined/NASA `3045.84 ms`; BASS-II `55.25 ms`
- **NASA fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage, required_scientific_concepts_not_covered

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.6`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: However, one of the most important results is that, in microgravity, the extinction of the polyethylene occurs almost immediately when the flow of relatively low oxygen concentration (C = 21 percent) stops.
   - Match explanation: matched terms: concentration, oxygen; scientific concepts: oxygen concentration, polyethylene; material: polyethylene; conditions: oxygen
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

2. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Thin Fuel: 1.1 Spread Rate: The experimental flame spread rates, Vf.,_,, over the thin cellulosic fuel in five different quiescent environments, at three different ambient pressures and two oxygen levels, are plotted in Fig.
   - Match explanation: matched terms: flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; material mismatch penalty
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

3. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.1`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Passage: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the measure the soot concentration (laser extinction) andmaterial.
   - Match explanation: matched terms: concentration, flame; scientific concepts: flame spread, oxygen concentration; material mismatch penalty
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

4. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.0813`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: flame; scientific concepts: flame spread; material mismatch penalty
   - Oxygen-condition check: mentions oxygen-related text; no quantitative oxygen value established in this excerpt.
   - Provisional QA category: **Partially relevant**; this is not expert-validated.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Preliminary results of polyethylene-insulation flammability in microgravity were obtained in the NASA Wire Insulation Flammability (WIF) experiment during the Space Shuttle flight STS-50 (refs.
   - Match explanation: matched terms: experiment, nasa; scientific concepts: polyethylene; material: polyethylene
   - Oxygen-condition check: does not show an oxygen measurement in this excerpt.
   - Provisional QA category: **Relevant**; this is not expert-validated.

### Actual NASA NTRS fallback results (top five)

1. **The Effect of Velocity on the Extinction Behavior of a Diffusion Flame during Transient Depressurization** ? NASA ID `20000000189`; score `0.1875`; URL: https://ntrs.nasa.gov/citations/20000000189; retrieved `2026-10-31T09:37:59.141881+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Current fire suppression plans for the International Space Station include the use of venting (depressurization) as a method for extinguishing a fire. Until recently this process had only been examined as part of a material flammability experiment performed on Skylab in the early 1970's. Due to the low initial pressure (0.35 Atm) and high oxygen concentration (65%), the Skylab experimental results are not applicable for understanding the effects of venting on a fire in a space station environment (21%O2, 1 Atm). Re
   - Oxygen-condition check: oxygen-related wording appears, but no threshold or causal finding is accepted from metadata/abstract alone.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

2. **Buoyant Effects on the Flammability of Silicone Samples Planned for the Spacecraft Fire Experiment (Saffire)** ? NASA ID `20150022421`; score `0.1875`; URL: https://ntrs.nasa.gov/citations/20150022421; retrieved `2026-10-31T09:37:59.141881+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Flammability experiments on silicone samples were conducted in anticipation of the Spacecraft Fire Experiment (Saffire). The sample geometry was chosen to match the NASA 6001 Test 1 specification, namely 5 cm wide by 30 cm tall. Four thicknesses of silicone (0.25, 0.36, 0.61 and 1.00 mm) were examined. Tests included traditional upward buoyant flame spread using Test 1 procedures, downward opposed-flow flame spread, horizontal and angled flame spread, and forced-flow upward and downward flame spread. In addition to
   - Oxygen-condition check: oxygen-related wording appears, but no threshold or causal finding is accepted from metadata/abstract alone.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

3. **Buoyant Effects on the Flammability of Silicone Samples Planned for the Spacecraft Fire Experiment (Saffire)** ? NASA ID `20150022123`; score `0.1875`; URL: https://ntrs.nasa.gov/citations/20150022123; retrieved `2026-10-31T09:37:59.141881+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Flammability experiments on silicone samples were conducted in anticipation of the Spacecraft Fire Experiment (Saffire). The sample geometry was chosen to match the NASA 6001 Test 1 specification, namely 5 cm wide by 30 cm tall. Four thicknesses of silicone (0.25, 0.36, 0.61 and 1.00 mm) were examined. Tests included traditional upward buoyant flame spread using Test 1 procedures, downward opposed flow flame spread, horizontal and angled flame spread, forced flow upward and downward flame spread. In addition to the
   - Oxygen-condition check: oxygen-related wording appears, but no threshold or causal finding is accepted from metadata/abstract alone.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

4. **Transition from Ignition to Flame Growth under External Radiation in 3D** ? NASA ID `20040161260`; score `0.1688`; URL: https://ntrs.nasa.gov/citations/20040161260; retrieved `2026-10-31T09:37:59.141881+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: This study focuses on localized ignition by external radiant flux and subsequent flame growth over thin polymeric materials (plastic and paper) in microgravity. Two transition stages were observed. The first transition stage covers the period from the onset of ignition to the formation of stabilized flame near the ignited area. This is followed by the second transition of the flame growth stage from the initial stabilized flame to sustained fire growth away from the ignited area. For the first stage, ignition exper
   - Oxygen-condition check: oxygen-related wording appears, but no threshold or causal finding is accepted from metadata/abstract alone.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

5. **Candle Flames in Non-Buoyant Atmospheres** ? NASA ID `20000005087`; score `0.1688`; URL: https://ntrs.nasa.gov/citations/20000005087; retrieved `2026-10-31T09:37:59.141881+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: This paper addresses the behavior of a candle flame in a long-duration, quiescent microgravity environment both on the space Shuttle and the Mir Orbiting Station (OS). On the Shuttle, the flames became dim blue after an initial transient where there was significant yellow (presumably soot) in the flame. The flame lifetimes were typically less than 60 seconds. The safety-mandated candlebox that contained the candle flame inhibited oxygen transport to the flame and thus limited the flame lifetime. 'Me flames on the M
   - Oxygen-condition check: oxygen-related wording appears, but no threshold or causal finding is accepted from metadata/abstract alone.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract does not prove a scientific finding.

### Actual BASS-II results

No BASS-II records matched this query. The BASS-II dataset was searched without inventing fields for extinction, gravity, pressure, or temperature.

### Query-specific relevance and condition assessment

- A result was treated as potentially relevant only when its returned title/excerpt/abstract addressed oxygen, flame propagation/spread/extinction, and the requested material or environment.
- Oxygen mentions without a numeric concentration, measurement context, comparison, or extinction condition were explicitly treated as insufficient for a quantitative oxygen claim.
- PMMA-specific queries require PMMA evidence; generic solid-fuel or spacecraft passages are not interchangeable with PMMA.
- Spacecraft oxygen-availability queries require spacecraft/environment context; generic combustion evidence is not spacecraft-specific evidence.
- Multiple passages with one NASA/source ID were counted as one independent source for diversity purposes.

## Overall assessment

**PARTIAL PASS: Search execution and provenance worked, but oxygen-specific scientific relevance remains limited.** All seven local searches completed, NASA fallback returned live catalogue metadata for three locally insufficient queries, and BASS-II was queried separately. The system preserved source identity and evidence scope. However, lexical oxygen matches do not establish quantitative oxygen effects or extinction limits, NASA results are metadata/abstract-only, repeated passages reduce independent-source diversity, and no expert reviewed the result judgments.

## Scientific and technical limitations

- No oxygen threshold, limiting oxygen concentration, or flame-extinction value was invented or inferred.
- No result was treated as an independently verified scientific finding.
- No PDFs or full-text documents were downloaded.
- No expert relevance judgments or ground-truth precision/recall metrics were produced.
- BASS-II support is limited to actual schema fields; no unsupported filters were introduced.
- No mission-specific recommendation was generated.
- Search scores measure lexical/entity overlap, not scientific validity or causal support.

## Preservation verification

Only this report was created for the test. Existing user changes, the existing stash, original datasets, benchmark fixtures, and Git history were preserved. Final Git status, data-directory diff, stash listing, and `git diff --check` were run after report generation.
