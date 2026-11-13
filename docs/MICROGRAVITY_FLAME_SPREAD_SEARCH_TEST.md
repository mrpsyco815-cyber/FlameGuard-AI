# Real-World Search Test 01: Microgravity Flame Spread

## Test scope and status

This is a read-only execution of the existing FlameGuard AI search services. No production code, ranking logic, datasets, benchmark fixtures, search configuration, stash, or Git history was modified. Results and relevance categories below are **provisional QA assessments, not expert-validated judgments**. NASA PDFs were not downloaded.

Retrieval date: 2026-10-31 (timestamps are preserved per query/result).

## Methods

- Local: `build_evidence_brief(query, limit=5)` against the local research intelligence store.
- Combined: `search_research_with_fallback(query, limit=5)`; local first, NASA NTRS only when configured sufficiency checks fail.
- BASS-II: `search_bass2_records(query, limit=5)` using the existing transparent keyword matcher.
- NASA records are catalogue metadata/abstracts only, with `scientific_findings_verified: false`; they are not treated as findings.
- Duplicate count is repeated source identity among local plus NASA returned records; passages from one source are not independent papers.

## 1. Microgravity flame spread

- **Local result count:** 5
- **NASA NTRS result count:** 0 (HTTP/API error: none)
- **BASS-II result count:** 0
- **Final combined record count:** 5 local/NASA records; BASS-II is reported separately
- **Unique independent source count:** 4
- **Duplicate source-record count:** 1
- **Latency:** local 257.51 ms; combined 14.9 ms; BASS-II 17.17 ms
- **NASA fallback:** not triggered; reasons: local evidence met configured sufficiency thresholds

### Top local results

1. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.75`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Match explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity
   - QA assessment: **Highly relevant** (provisional machine-assisted assessment).

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: In general,   as the  concurrent   flow  velocity  V decreases,   the  flame-spread    rate  V, decreases,   from  an average   (for  all three  materials)   ofV_: = 0.5-0.75  mm/s  at V = 8.5 cm/s  to V,: = 0.05-0.01  mm/s  at V = 0.3-0.5  cm/s.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `unknown`; review `requires_manual_review`.
   - Excerpt: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

5. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.55`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

### NASA NTRS fallback results

No NASA NTRS results were requested/returned for this query.

### BASS-II results

No BASS-II records matched this free-text query. No unsupported pressure, temperature, or gravity filter was applied.

### Relevance and limitations

- Local passages were assessed from their returned titles, excerpts, matched terms/reasons, evidence modality, review status, material/condition matches, and source identity.
- A result sharing ?flame spread? but lacking the requested material, oxygen, flow, gravity, or spacecraft condition is only partially relevant or insufficient information.
- Repeated passages with the same NASA/source ID are contextual passages from one paper, not independent research papers.
- NASA fallback records are metadata/abstract scope only and remain unverified.
- BASS-II free-text matching does not establish that a record measured flame spread; its available structured fields are limited to the dataset schema.

## 2. Flame spread over solid materials in microgravity

- **Local result count:** 5
- **NASA NTRS result count:** 0 (HTTP/API error: none)
- **BASS-II result count:** 1
- **Final combined record count:** 5 local/NASA records; BASS-II is reported separately
- **Unique independent source count:** 4
- **Duplicate source-record count:** 1
- **Latency:** local 19.28 ms; combined 20.14 ms; BASS-II 26.21 ms
- **NASA fallback:** not triggered; reasons: local evidence met configured sufficiency thresholds

### Top local results

1. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.6`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Match explanation: matched terms: flame, microgravity, solid, spread; scientific concepts: microgravity, flame spread, solid fuel combustion; conditions: microgravity
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

2. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                
   - Match explanation: matched terms: flame, over, solid, spread; scientific concepts: microgravity, flame spread, solid fuel combustion
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

3. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.475`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: In general,   as the  concurrent   flow  velocity  V decreases,   the  flame-spread    rate  V, decreases,   from  an average   (for  all three  materials)   ofV_: = 0.5-0.75  mm/s  at V = 8.5 cm/s  to V,: = 0.05-0.01  mm/s  at V = 0.3-0.5  cm/s.
   - Match explanation: matched terms: flame, material, spread; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.475`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `unknown`; review `requires_manual_review`.
   - Excerpt: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Match explanation: matched terms: flame, over, spread; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

5. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.475`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Match explanation: matched terms: flame, over, spread; scientific concepts: flame spread, solid fuel combustion
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

### NASA NTRS fallback results

No NASA NTRS results were requested/returned for this query.

### BASS-II results

1. **BASS-II PI `Olson`, Test `O13b`, material `1/2" clear PMMA rod`**; score `0.075`; matched terms `over`; fields `{'Calibrated  initial O2 % by vol ': '14.6', 'Calibrated final O2 % by vol': '14.4', 'Initial CO2 % by vol': '1.85', 'Final CO2 % by vol': '2.09', 'Initial CO (ppm)': '950', 'Final CO (ppm)': 'over', 'Total Frames Shot': '6', 'Fan display': '1.3   0.9', 'Air display': '7   4? (49   ?)', 'Flow restrictor': '2'}`.
   - QA assessment: **Partially relevant or insufficient information** unless the requested flame-spread condition is represented in the returned structured fields. This record is metadata/data context, not automatically a verified flame-spread finding.

### Relevance and limitations

- Local passages were assessed from their returned titles, excerpts, matched terms/reasons, evidence modality, review status, material/condition matches, and source identity.
- A result sharing ?flame spread? but lacking the requested material, oxygen, flow, gravity, or spacecraft condition is only partially relevant or insufficient information.
- Repeated passages with the same NASA/source ID are contextual passages from one paper, not independent research papers.
- NASA fallback records are metadata/abstract scope only and remain unverified.
- BASS-II free-text matching does not establish that a record measured flame spread; its available structured fields are limited to the dataset schema.

## 3. PMMA flame spread under microgravity conditions

- **Local result count:** 5
- **NASA NTRS result count:** 5 (HTTP/API error: none)
- **BASS-II result count:** 5
- **Final combined record count:** 10 local/NASA records; BASS-II is reported separately
- **Unique independent source count:** 9
- **Duplicate source-record count:** 1
- **Latency:** local 23.09 ms; combined 8564.75 ms; BASS-II 16.34 ms
- **NASA fallback:** triggered; reasons: too_few_local_passages, insufficient_local_source_coverage, required_experimental_conditions_not_covered, required_scientific_concepts_not_covered

### Top local results

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.625`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: The  rates  of material   burning-out    for  Russian-made  PMMA  and  polyethylene    are  less than  0.05  mm/s  at a flow velocity  V = 10 cm/s  and C, x= 21 percent,    i.e., 5 to 10 times  lower  than  the  flame-spread    rates  measured   for  the melting   materials   that  were  tested.
   - Match explanation: matched terms: flame, pmma, spread; scientific concepts: flame spread, polymethyl methacrylate; material: polymethyl methacrylate
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

2. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.1375`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `simulation`; review `requires_manual_review`.
   - Excerpt: It should be noted that under this condition only partial burning of the sample near the igniter region was observed in the FDS simulations done at 50 kPa, and the flame would eventually blow off about 11 mm away from the igniter, thus no spread rate was determined for that condition due to the very short propagation length.
   - Match explanation: matched terms: condition, flame, spread, under; scientific concepts: flame spread; material mismatch penalty
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

3. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.1313`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Match explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity; material mismatch penalty
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.1`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `unknown`; review `requires_manual_review`.
   - Excerpt: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread; material mismatch penalty
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.625`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: TABLE   1.2.--GROUND-TESTING       RESULTS   OF  U.S.-PROVIDED    MATERIAL                                FLAMMABILITY        --  LIMITING   VELOCITY      [Vb,,,' ) DETERMINED     IN                                      APPARATUSES    WITH  SUPPRESSED    CONVECTION                        Number                   Material                                                        Vi.., cm/sec                              
   - Match explanation: matched terms: flame, pmma, spread; scientific concepts: flame spread, polymethyl methacrylate; material: polymethyl methacrylate
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

### NASA NTRS fallback results

1. **Diffusive and Radiative Transport in Fires (DARTFire): Opposed-Flow Flame Spread in Low-Velocity Flows** ? NASA ID `19990054038`; score `0.9`; URL: https://ntrs.nasa.gov/citations/19990054038; retrieved `2026-10-31T09:30:08.010717+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: For flames spreading into a low-velocity flow that can only be obtained in microgravity, we have observed behavior that is different from that which is obtained at higher velocities where radiative effects are unimportant and species transport is relatively fast. Unfortunately, lack of a large body of low-gravity flame spread experimental data inhibits progress in developing an understanding of the physics of low-vel
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

2. **Flow Effects on the Flammability Diagrams of Solid Fuels: Microgravity Influence on Ignition Delay** ? NASA ID `19990053973`; score `0.9`; URL: https://ntrs.nasa.gov/citations/19990053973; retrieved `2026-10-31T09:30:08.010717+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: The possibility of an accidental fire in space-based facilities is a primary concern of space exploration programs. Spacecraft environments generally present low velocity air currents produced by ventilation and heating systems (of the order of 0.1 m/s), and fluctuating oxygen concentrations around that of air due to CO2 removal systems. Recent experiments of flame spread in microgravity show the spread rate to be fa
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

3. **Theoretical Prediction of Microgravity Ignition Delay of Polymeric Fuels in Low Velocity Flows** ? NASA ID `20010074015`; score `0.9`; URL: https://ntrs.nasa.gov/citations/20010074015; retrieved `2026-10-31T09:30:08.010717+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: A new flammability apparatus and protocol, FIST (Forced Flow Ignition and Flame Spread Test), is under development. Based on the LIFT (Lateral Ignition and Flame Spread Test) protocol, FIST better reflects the environments expected in spacebased facilities. The final objective of the FIST research is to provide NASA with a test methodology that complements the existing protocol and provides a more comprehensive asses
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

4. **Fourth International Microgravity Combustion Workshop** ? NASA ID `19970020547`; score `0.0938`; URL: https://ntrs.nasa.gov/citations/19970020547; retrieved `2026-10-31T09:30:08.010717+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: This proceedings document is a compilation about work performed by a community of researchers from universities, industry and government laboratories across the United States and in Europe and Japan who have recognized the value of the reduced-gravity environment in attacking the fundamental and practical problems of combustion science. On their behalf, I am pleased to present this document to the assembled participa
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

5. **The 3rd International Microgravity Combustion Workshop** ? NASA ID `19960008386`; score `0.0938`; URL: https://ntrs.nasa.gov/citations/19960008386; retrieved `2026-10-31T09:30:08.010717+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: This Conference Publication contains 71 papers presented at the Third International Microgravity Combustion Workshop held in Cleveland, Ohio, from April 11 to 13, 1995. The purpose of the workshop was twofold: to exchange information about the progress and promise of combustion science in microgravity and to provide a forum to discuss which areas in microgravity combustion science need to be expanded profitably and w
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

### BASS-II results

1. **BASS-II PI `Bhattacharjee`, Test `B1`, material `100 micron PMMA film   2 cm wide`**; score `0.475`; matched terms `pmma`; fields `{'Calibrated  initial O2 % by vol ': '22.2', 'Calibrated final O2 % by vol': '22.2', 'Initial CO2 % by vol': '0.44', 'Final CO2 % by vol': '0.44', 'Initial CO (ppm)': '0', 'Final CO (ppm)': '6', 'Total Frames Shot': '57', 'Fan display': '62', 'Air display': '5', 'Flow restrictor': '2'}`.
   - QA assessment: **Partially relevant or insufficient information** unless the requested flame-spread condition is represented in the returned structured fields. This record is metadata/data context, not automatically a verified flame-spread finding.

2. **BASS-II PI `Bhattacharjee`, Test `B2`, material `200 micron PMMA film   2 cm wide`**; score `0.475`; matched terms `pmma`; fields `{'Calibrated  initial O2 % by vol ': '22.2', 'Calibrated final O2 % by vol': '1.6', 'Initial CO2 % by vol': '0.44', 'Final CO2 % by vol': '', 'Initial CO (ppm)': '6', 'Final CO (ppm)': '', 'Total Frames Shot': 'none', 'Fan display': '62', 'Air display': '5', 'Flow restrictor': '2'}`.
   - QA assessment: **Partially relevant or insufficient information** unless the requested flame-spread condition is represented in the returned structured fields. This record is metadata/data context, not automatically a verified flame-spread finding.

3. **BASS-II PI `Bhattacharjee`, Test `B4`, material `300 micron PMMA film   2 cm wide `**; score `0.475`; matched terms `pmma`; fields `{'Calibrated  initial O2 % by vol ': '22.2', 'Calibrated final O2 % by vol': '22.2', 'Initial CO2 % by vol': '0.44', 'Final CO2 % by vol': '0.51', 'Initial CO (ppm)': '-1', 'Final CO (ppm)': '10', 'Total Frames Shot': '137', 'Fan display': '61', 'Air display': '5', 'Flow restrictor': '2'}`.
   - QA assessment: **Partially relevant or insufficient information** unless the requested flame-spread condition is represented in the returned structured fields. This record is metadata/data context, not automatically a verified flame-spread finding.

4. **BASS-II PI `Bhattacharjee`, Test `B6`, material `2 cm 0.1 mm PMMA film`**; score `0.475`; matched terms `pmma`; fields `{'Calibrated  initial O2 % by vol ': '21', 'Calibrated final O2 % by vol': '20.9', 'Initial CO2 % by vol': '0.33', 'Final CO2 % by vol': '0.41', 'Initial CO (ppm)': '0', 'Final CO (ppm)': '0.3', 'Total Frames Shot': '80', 'Fan display': '0.9   1.3   2.75', 'Air display': '3   5   approaching 10', 'Flow restrictor': '2'}`.
   - QA assessment: **Partially relevant or insufficient information** unless the requested flame-spread condition is represented in the returned structured fields. This record is metadata/data context, not automatically a verified flame-spread finding.

5. **BASS-II PI `Bhattacharjee`, Test `B8`, material `2 cm   0.2 mm PMMA film`**; score `0.475`; matched terms `pmma`; fields `{'Calibrated  initial O2 % by vol ': '21', 'Calibrated final O2 % by vol': '20.5', 'Initial CO2 % by vol': '0.33', 'Final CO2 % by vol': '0.58', 'Initial CO (ppm)': '0', 'Final CO (ppm)': '131', 'Total Frames Shot': '226', 'Fan display': '1.4    incr to 10.0', 'Air display': '10   max', 'Flow restrictor': '0'}`.
   - QA assessment: **Partially relevant or insufficient information** unless the requested flame-spread condition is represented in the returned structured fields. This record is metadata/data context, not automatically a verified flame-spread finding.

### Relevance and limitations

- Local passages were assessed from their returned titles, excerpts, matched terms/reasons, evidence modality, review status, material/condition matches, and source identity.
- A result sharing ?flame spread? but lacking the requested material, oxygen, flow, gravity, or spacecraft condition is only partially relevant or insufficient information.
- Repeated passages with the same NASA/source ID are contextual passages from one paper, not independent research papers.
- NASA fallback records are metadata/abstract scope only and remain unverified.
- BASS-II free-text matching does not establish that a record measured flame spread; its available structured fields are limited to the dataset schema.

## 4. Effect of oxygen concentration on flame spread in microgravity

- **Local result count:** 5
- **NASA NTRS result count:** 0 (HTTP/API error: none)
- **BASS-II result count:** 0
- **Final combined record count:** 5 local/NASA records; BASS-II is reported separately
- **Unique independent source count:** 4
- **Duplicate source-record count:** 1
- **Latency:** local 17.17 ms; combined 22.61 ms; BASS-II 20.45 ms
- **NASA fallback:** not triggered; reasons: local evidence met configured sufficiency thresholds

### Top local results

1. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.525`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Match explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.525`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: However,   one  of the most  important   results   is that,  in microgravity,    the extinction   of the  polyethylene occurs  almost  immediately   when  the  flow  of relatively  low oxygen   concentration    (C  = 21  percent)   stops.
   - Match explanation: matched terms: concentration, microgravity, oxygen; scientific concepts: microgravity, oxygen concentration; conditions: microgravity, oxygen
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.475`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: effect, flame, spread; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.4`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the                                                   measure the soot concentration (laser extinction) andmaterial.
   - Match explanation: matched terms: concentration, flame; scientific concepts: flame spread, oxygen concentration
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

5. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.525`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Match explanation: matched terms: flame, oxygen, spread; scientific concepts: flame spread, oxygen concentration; conditions: oxygen
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

### NASA NTRS fallback results

No NASA NTRS results were requested/returned for this query.

### BASS-II results

No BASS-II records matched this free-text query. No unsupported pressure, temperature, or gravity filter was applied.

### Relevance and limitations

- Local passages were assessed from their returned titles, excerpts, matched terms/reasons, evidence modality, review status, material/condition matches, and source identity.
- A result sharing ?flame spread? but lacking the requested material, oxygen, flow, gravity, or spacecraft condition is only partially relevant or insufficient information.
- Repeated passages with the same NASA/source ID are contextual passages from one paper, not independent research papers.
- NASA fallback records are metadata/abstract scope only and remain unverified.
- BASS-II free-text matching does not establish that a record measured flame spread; its available structured fields are limited to the dataset schema.

## 5. Effect of forced airflow on flame propagation

- **Local result count:** 5
- **NASA NTRS result count:** 0 (HTTP/API error: none)
- **BASS-II result count:** 0
- **Final combined record count:** 5 local/NASA records; BASS-II is reported separately
- **Unique independent source count:** 4
- **Duplicate source-record count:** 1
- **Latency:** local 17.13 ms; combined 17.52 ms; BASS-II 10.67 ms
- **NASA fallback:** not triggered; reasons: local evidence met configured sufficiency thresholds

### Top local results

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: The  flame-propagation      rate VF÷ obtained   in the ground   testing  appeared   to be lower than  V_:"from  the space  experiment   on Mir.
   - Match explanation: matched terms: flame, propagation; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

2. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Match explanation: matched terms: effect, flame; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

3. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Considering that the initial purpose of the     computed from a Monte Carlo propagation analysis, images recorded during the experiments was to use      considering a conservative error of 5% on the signal the data to visualize the flame and track its evolu-       ratio ΘG/R, resulting in 117 K of uncertainty for tem- tion over time, i.e., pyrolysis length, flame size, etc.,       perature determination.
   - Match explanation: matched terms: flame, propagation; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

4. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.34`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Match explanation: matched terms: flame; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: NUMBER OF PAGES                                                                                                                     62         Extinction;      Fire   safety;   Flammability;      Flammability        limits;   Flame    propagation;                                                                                                                                                                           16
   - Match explanation: matched terms: flame, propagation; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

### NASA NTRS fallback results

No NASA NTRS results were requested/returned for this query.

### BASS-II results

No BASS-II records matched this free-text query. No unsupported pressure, temperature, or gravity filter was applied.

### Relevance and limitations

- Local passages were assessed from their returned titles, excerpts, matched terms/reasons, evidence modality, review status, material/condition matches, and source identity.
- A result sharing ?flame spread? but lacking the requested material, oxygen, flow, gravity, or spacecraft condition is only partially relevant or insufficient information.
- Repeated passages with the same NASA/source ID are contextual passages from one paper, not independent research papers.
- NASA fallback records are metadata/abstract scope only and remain unverified.
- BASS-II free-text matching does not establish that a record measured flame spread; its available structured fields are limited to the dataset schema.

## 6. Flame spread and extinction in spacecraft environments

- **Local result count:** 5
- **NASA NTRS result count:** 0 (HTTP/API error: none)
- **BASS-II result count:** 0
- **Final combined record count:** 5 local/NASA records; BASS-II is reported separately
- **Unique independent source count:** 4
- **Duplicate source-record count:** 1
- **Latency:** local 11.41 ms; combined 28.45 ms; BASS-II 14.71 ms
- **NASA fallback:** not triggered; reasons: local evidence met configured sufficiency thresholds

### Top local results

1. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.52`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Match explanation: matched terms: environment, flame, spread; scientific concepts: flame spread
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

2. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.52`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `simulation`; review `requires_manual_review`.
   - Excerpt: From the results, it is seen that the simulations performed using finite rate chemistry underpredict the experimental spread rates at the higher pressures, while not even allowing flame spread at the lower pressure environments.
   - Match explanation: matched terms: environment, flame, spread; scientific concepts: flame spread
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

3. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: In general,   as the  concurrent   flow  velocity  V decreases,   the  flame-spread    rate  V, decreases,   from  an average   (for  all three  materials)   ofV_: = 0.5-0.75  mm/s  at V = 8.5 cm/s  to V,: = 0.05-0.01  mm/s  at V = 0.3-0.5  cm/s.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.43`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the                                                   measure the soot concentration (laser extinction) andmaterial.
   - Match explanation: matched terms: extinction, flame; scientific concepts: flame spread
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

5. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.52`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Match explanation: matched terms: environment, flame, spread; scientific concepts: flame spread
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

### NASA NTRS fallback results

No NASA NTRS results were requested/returned for this query.

### BASS-II results

No BASS-II records matched this free-text query. No unsupported pressure, temperature, or gravity filter was applied.

### Relevance and limitations

- Local passages were assessed from their returned titles, excerpts, matched terms/reasons, evidence modality, review status, material/condition matches, and source identity.
- A result sharing ?flame spread? but lacking the requested material, oxygen, flow, gravity, or spacecraft condition is only partially relevant or insufficient information.
- Repeated passages with the same NASA/source ID are contextual passages from one paper, not independent research papers.
- NASA fallback records are metadata/abstract scope only and remain unverified.
- BASS-II free-text matching does not establish that a record measured flame spread; its available structured fields are limited to the dataset schema.

## 7. NASA experiments on flame spread in reduced gravity

- **Local result count:** 5
- **NASA NTRS result count:** 5 (HTTP/API error: none)
- **BASS-II result count:** 0
- **Final combined record count:** 10 local/NASA records; BASS-II is reported separately
- **Unique independent source count:** 9
- **Duplicate source-record count:** 1
- **Latency:** local 15.85 ms; combined 2020.57 ms; BASS-II 23.1 ms
- **NASA fallback:** triggered; reasons: too_few_local_passages, insufficient_local_source_coverage, required_experimental_conditions_not_covered

### Top local results

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: Preliminary    results  of polyethylene-insulation      flammability    in microgravity   were  obtained   in the NASA  Wire Insulation   Flammability   (WIF)  experiment   during  the Space  Shuttle   flight  STS-50   (refs.
   - Match explanation: matched terms: experiment, nasa; scientific concepts: microgravity, polyethylene; material: polyethylene
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

2. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.15`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                
   - Match explanation: matched terms: flame, gravity, reduced, spread; scientific concepts: microgravity, flame spread; conditions: reduced gravity; material mismatch penalty
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

3. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.1187`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Match explanation: matched terms: experiment, flame, spread; scientific concepts: microgravity, flame spread; material mismatch penalty
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.1`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `unknown`; review `requires_manual_review`.
   - Excerpt: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread; material mismatch penalty
   - QA assessment: **Partially relevant** (provisional machine-assisted assessment).

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.55`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Excerpt: The  rates  of material   burning-out    for  Russian-made  PMMA  and  polyethylene    are  less than  0.05  mm/s  at a flow velocity  V = 10 cm/s  and C, x= 21 percent,    i.e., 5 to 10 times  lower  than  the  flame-spread    rates  measured   for  the melting   materials   that  were  tested.
   - Match explanation: matched terms: flame, spread; scientific concepts: flame spread, polyethylene; material: polyethylene
   - QA assessment: **Relevant** (provisional machine-assisted assessment).

### NASA NTRS fallback results

1. **Opposed-Flow Flame Spreading in Reduced Gravity** ? NASA ID `19930011017`; score `0.1688`; URL: https://ntrs.nasa.gov/citations/19930011017; retrieved `2026-10-31T09:30:16.767126+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: Experimental results obtained in drop towers and in Space Shuttle based experiments coupled with modelling efforts are beginning to provide information that is allowing an understanding to be developed of the physics of opposed-flow flame spread at reduced gravity where the spread rate and flow velocity are comparable and of the role played by radiative and diffusive processes in flame spreading in microgravity. Here
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

2. **Feasibility study of liquid pool burning in reduced gravity** ? NASA ID `19790024132`; score `0.1688`; URL: https://ntrs.nasa.gov/citations/19790024132; retrieved `2026-10-31T09:30:16.767126+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: The feasibility of conducting experiments in the Spacelab on ignition and flame spread with liquid fuel pools which are initially at a temperature lower than the fuel's flash point temperature was studied. Theories were developed for the ignition and flame spread processes, and experiments were conducted to understand the factors influencing the ignition process and the spread rate. The results were employed to devis
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

3. **Combustion of solid fuel in very low speed oxygen streams** ? NASA ID `19930011018`; score `0.1688`; URL: https://ntrs.nasa.gov/citations/19930011018; retrieved `2026-10-31T09:30:16.767126+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: In reduced gravity, the combustion of solid fuel in low-speed flow can be studied. The flame behavior in this low-speed regime will fill a void in our understanding of the flow effect on combustion. In addition, it is important for spacecraft fire safety considerations. In this work, modeling and experimental work on low-speed forced-concurrent-flow flame spread are carried out. In addition, experiments on reduced-gr
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

4. **Sounding Rocket Microgravity Experiments Elucidating Diffusive and Radiative Transport Effects on Flame Spread over Thermally-Thick Solids** ? NASA ID `20030111833`; score `0.1562`; URL: https://ntrs.nasa.gov/citations/20030111833; retrieved `2026-10-31T09:30:16.767126+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: A series of 6-minute microgravity combustion experiments of opposed flow flame spread over thermally-thick PMMA has been conducted to extend data previously reported at high opposed flows to almost two decades lower in flow. The effect of flow velocity on flame spread shows a square root power law dependence rather than the linear dependence predicted by thermal theory. The experiments demonstrate that opposed flow f
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

5. **Diffusive and Radiative Transport in Fires (DARTFire): Opposed-Flow Flame Spread in Low-Velocity Flows** ? NASA ID `19990054038`; score `0.1562`; URL: https://ntrs.nasa.gov/citations/19990054038; retrieved `2026-10-31T09:30:16.767126+00:00`; evidence type `bibliographic_metadata_and_abstract`; verification `False`; review `not_scientifically_reviewed`.
   - Abstract: For flames spreading into a low-velocity flow that can only be obtained in microgravity, we have observed behavior that is different from that which is obtained at higher velocities where radiative effects are unimportant and species transport is relatively fast. Unfortunately, lack of a large body of low-gravity flame spread experimental data inhibits progress in developing an understanding of the physics of low-vel
   - QA assessment: **Relevant or partially relevant catalogue evidence only**, pending source-document and expert review; an abstract does not prove a scientific finding.

### BASS-II results

No BASS-II records matched this free-text query. No unsupported pressure, temperature, or gravity filter was applied.

### Relevance and limitations

- Local passages were assessed from their returned titles, excerpts, matched terms/reasons, evidence modality, review status, material/condition matches, and source identity.
- A result sharing ?flame spread? but lacking the requested material, oxygen, flow, gravity, or spacecraft condition is only partially relevant or insufficient information.
- Repeated passages with the same NASA/source ID are contextual passages from one paper, not independent research papers.
- NASA fallback records are metadata/abstract scope only and remain unverified.
- BASS-II free-text matching does not establish that a record measured flame spread; its available structured fields are limited to the dataset schema.

## Overall assessment

**PARTIAL PASS: Some queries work, but important relevance and retrieval limitations remain.** Local retrieval was traceable for all seven queries, BASS-II was searched separately, and NASA fallback returned live catalogue records for locally insufficient PMMA and reduced-gravity experiment queries. However, source duplication, lexical matching, metadata-only NASA evidence, and incomplete condition compatibility mean these outputs are suitable for research support and review?not expert-validated scientific conclusions.

## What was tested and what remains unverified

- Tested: seven specified queries; local-first ordering; two live NASA NTRS fallback calls; BASS-II search for every query; counts, IDs, titles, excerpts/abstracts, URLs, timestamps, evidence types, source duplication, latency, and fallback reasons.
- Not tested: PDF download/full-text verification, independent expert relevance judgments, scientific ground-truth precision/recall, engineering safety decisions, or validation of experimental conclusions.
