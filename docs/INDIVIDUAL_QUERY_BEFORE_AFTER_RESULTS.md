# Individual Query Before/After Results

All 21 queries were run individually before and after the correction. Baseline and final records below are actual service outputs. Relevance wording is provisional QA assessment, not expert validation.

## Aggregate comparison

| ID | Local before/after | NASA before/after | BASS-II before/after | Sources before/after | Duplicates before/after | Fallback before/after | |
|---|---:|---:|---:|---:|---:|---|
| T1-01 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T1-02 | 5/5 | 0/0 | 1/1 | 4/4 | 1/1 | False/False |
| T1-03 | 5/5 | 5/5 | 5/5 | 9/9 | 1/1 | True/True |
| T1-04 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T1-05 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T1-06 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T1-07 | 5/5 | 5/0 | 0/0 | 9/4 | 1/1 | True/False |
| T2-01 | 2/2 | 5/5 | 0/0 | 6/6 | 1/1 | True/True |
| T2-02 | 2/2 | 5/5 | 0/0 | 6/6 | 1/1 | True/True |
| T2-03 | 2/2 | 5/5 | 0/0 | 6/6 | 1/1 | True/True |
| T2-04 | 5/5 | 2/2 | 0/0 | 5/5 | 2/2 | True/True |
| T2-05 | 5/5 | 5/5 | 0/0 | 9/9 | 1/1 | True/True |
| T2-06 | 5/5 | 2/2 | 0/0 | 5/5 | 2/2 | True/True |
| T2-07 | 5/5 | 0/0 | 0/0 | 2/2 | 3/3 | False/True |
| T3-01 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T3-02 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T3-03 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T3-04 | 5/5 | 1/1 | 0/0 | 4/4 | 2/2 | True/True |
| T3-05 | 5/5 | 4/4 | 5/5 | 8/8 | 1/1 | True/True |
| T3-06 | 5/5 | 0/0 | 0/0 | 4/4 | 1/1 | False/False |
| T3-07 | 5/5 | 5/5 | 0/0 | 9/9 | 1/1 | True/True |

## Per-query actual records

### T1-01 ? Microgravity flame spread

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `243.14/18.09/16.43 ms`.

**Final local top five:**
1. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.95` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity; phenomena: flame spread; environments: microgravity
2. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.75` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                      pressure (100 kPa)  in reduced  gravity.
   - Explanation: matched terms: flame, spread; scientific concepts: microgravity, flame spread; phenomena: flame spread; environments: microgravity
3. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.55` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Preliminary    results  of polyethylene-insulation      flammability    in microgravity   were  obtained   in the NASA  Wire Insulation   Flammability   (WIF)  experiment   during  the Space  Shuttle   flight  STS-50   (refs.
   - Explanation: matched terms: microgravity; scientific concepts: microgravity; conditions: microgravity; environments: microgravity
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.2925` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Explanation: matched terms: flame, spread; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty
5. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.75` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `mixed` | review `requires_manual_review`
   - Excerpt/fields: These  results indicate  that                                                                     concurrent flame spread in low pressure and                                                              normal    gravity,   may   have    similar                                                                             characteristics as those in reduced gravity.
   - Explanation: matched terms: flame, spread; scientific concepts: microgravity, flame spread; phenomena: flame spread; environments: microgravity

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `156.76/13.28/10.56 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T1-02 ? Flame spread over solid materials in microgravity

**Baseline:** local 5, NASA 0, BASS-II 1, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `13.76/12.5/12.77 ms`.

**Final local top five:**
1. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.8` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: flame, microgravity, solid, spread; scientific concepts: microgravity, flame spread, solid fuel combustion; conditions: microgravity; phenomena: flame spread; environments: microgravity
2. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.75` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                      pressure (100 kPa)  in reduced  gravity.
   - Explanation: matched terms: flame, over, solid, spread; scientific concepts: microgravity, flame spread, solid fuel combustion; phenomena: flame spread; environments: microgravity
3. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.55` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: material, microgravity; scientific concepts: microgravity; conditions: microgravity; environments: microgravity
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.2587` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Explanation: matched terms: flame, over, spread; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty
5. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.6` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `mixed` | review `requires_manual_review`
   - Excerpt/fields: These  results indicate  that                                                                     concurrent flame spread in low pressure and                                                              normal    gravity,   may   have    similar                                                                             characteristics as those in reduced gravity.
   - Explanation: matched terms: flame, spread; scientific concepts: microgravity, flame spread; phenomena: flame spread; environments: microgravity

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
1. `Olson:O13b` **PI Olson / Test O13b / 1/2" clear PMMA rod** | score `0.0338` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "14.6", "Calibrated final O2 % by vol": "14.4", "Initial CO2 % by vol": "1.85", "Final CO2 % by vol": "2.09", "Initial CO (ppm)": "950", "Final CO (ppm)": "over", "Total Frames Shot": "6", "Fan display": "1.3   0.9", "Air display": "7   4? (49   ?)", "Flow restrictor": "2"}
   - Explanation: matched terms: over; environment mismatch penalty

**Final:** local 5, NASA 0, BASS-II 1, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `21.19/19.39/22.84 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T1-03 ? PMMA flame spread under microgravity conditions

**Baseline:** local 5, NASA 5, BASS-II 5, combined 10, unique sources 9, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_experimental_conditions_not_covered, required_scientific_concepts_not_covered), latency local/combined/BASS-II `32.25/7424.17/25.97 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.7` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: 3.4 Non-Steadiness    and Other  Characteristics    of Combustion    in Microgravity      The  nonsteadiness    of polymer   combustion    observed   in the space  experiment   might  be explained   by two reasons:   (1)  the formation   of the  melt  drop,  which   is almost   spherical   tbr  Delrin  and PMMA   (see  figs.
   - Explanation: matched terms: microgravity, pmma; scientific concepts: microgravity, polymethyl methacrylate; material: polymethyl methacrylate; conditions: microgravity; environments: microgravity
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.1812` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity; phenomena: flame spread; environments: microgravity; material mismatch penalty
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.15` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                      pressure (100 kPa)  in reduced  gravity.
   - Explanation: matched terms: flame, spread; scientific concepts: microgravity, flame spread; phenomena: flame spread; environments: microgravity; material mismatch penalty
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.0563` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Explanation: matched terms: flame, spread; scientific concepts: flame spread; phenomena: flame spread; material mismatch penalty; environment mismatch penalty
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.3262` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: The  rates  of material   burning-out    for  Russian-made  PMMA  and  polyethylene    are  less than  0.05  mm/s  at a flow velocity  V = 10 cm/s  and C, x= 21 percent,    i.e., 5 to 10 times  lower  than  the  flame-spread    rates  measured   for  the melting   materials   that  were  tested.
   - Explanation: matched terms: flame, pmma, spread; scientific concepts: flame spread, polymethyl methacrylate; material: polymethyl methacrylate; phenomena: flame spread; environment mismatch penalty

**Final NASA top five:**
1. `19990054038` **Diffusive and Radiative Transport in Fires (DARTFire): Opposed-Flow Flame Spread in Low-Velocity Flows** | score `1.0` | URL `https://ntrs.nasa.gov/citations/19990054038` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: For flames spreading into a low-velocity flow that can only be obtained in microgravity, we have observed behavior that is different from that which is obtained at higher velocities where radiative effects are unimportant and species transport is relatively fast. Unfortunately, lack of a large body of low-gravity flame spread experimental data inhibits progress in developing an understanding of the physics of low-velocity, opposed-flow flame spread phenomena. Recent DARTFire sounding rocket expe
   - Explanation: matched terms: condition, flame, microgravity, pmma, spread, under; scientific concepts: microgravity, flame spread, polymethyl methacrylate; material: polymethyl methacrylate; conditions: microgravity; phenomena: flame spread; environments: microgravity
2. `19990053973` **Flow Effects on the Flammability Diagrams of Solid Fuels: Microgravity Influence on Ignition Delay** | score `1.0` | URL `https://ntrs.nasa.gov/citations/19990053973` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: The possibility of an accidental fire in space-based facilities is a primary concern of space exploration programs. Spacecraft environments generally present low velocity air currents produced by ventilation and heating systems (of the order of 0.1 m/s), and fluctuating oxygen concentrations around that of air due to CO2 removal systems. Recent experiments of flame spread in microgravity show the spread rate to be faster and the limiting oxygen concentration lower than in normal-gravity. To date
   - Explanation: matched terms: condition, flame, microgravity, pmma, spread, under; scientific concepts: microgravity, flame spread, polymethyl methacrylate; material: polymethyl methacrylate; conditions: microgravity; phenomena: flame spread; environments: microgravity
3. `20010074015` **Theoretical Prediction of Microgravity Ignition Delay of Polymeric Fuels in Low Velocity Flows** | score `1.0` | URL `https://ntrs.nasa.gov/citations/20010074015` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: A new flammability apparatus and protocol, FIST (Forced Flow Ignition and Flame Spread Test), is under development. Based on the LIFT (Lateral Ignition and Flame Spread Test) protocol, FIST better reflects the environments expected in spacebased facilities. The final objective of the FIST research is to provide NASA with a test methodology that complements the existing protocol and provides a more comprehensive assessment of material flammability of practical materials for space applications. Th
   - Explanation: matched terms: condition, flame, microgravity, pmma, spread, under; scientific concepts: microgravity, flame spread, polymethyl methacrylate; material: polymethyl methacrylate; conditions: microgravity; phenomena: flame spread; environments: microgravity
4. `19970020547` **Fourth International Microgravity Combustion Workshop** | score `0.1187` | URL `https://ntrs.nasa.gov/citations/19970020547` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This proceedings document is a compilation about work performed by a community of researchers from universities, industry and government laboratories across the United States and in Europe and Japan who have recognized the value of the reduced-gravity environment in attacking the fundamental and practical problems of combustion science. On their behalf, I am pleased to present this document to the assembled participants at the Fourth International Microgravity Combustion Workshop, to be held nea
   - Explanation: matched terms: microgravity; scientific concepts: microgravity; conditions: microgravity; environments: microgravity; material mismatch penalty
5. `19960008386` **The 3rd International Microgravity Combustion Workshop** | score `0.1187` | URL `https://ntrs.nasa.gov/citations/19960008386` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This Conference Publication contains 71 papers presented at the Third International Microgravity Combustion Workshop held in Cleveland, Ohio, from April 11 to 13, 1995. The purpose of the workshop was twofold: to exchange information about the progress and promise of combustion science in microgravity and to provide a forum to discuss which areas in microgravity combustion science need to be expanded profitably and which should be included in upcoming NASA Research Announcements (NRA).
   - Explanation: matched terms: microgravity; scientific concepts: microgravity; conditions: microgravity; environments: microgravity; material mismatch penalty

**Final BASS-II top five:**
1. `Bhattacharjee:B1` **PI Bhattacharjee / Test B1 / 100 micron PMMA film   2 cm wide** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "22.2", "Calibrated final O2 % by vol": "22.2", "Initial CO2 % by vol": "0.44", "Final CO2 % by vol": "0.44", "Initial CO (ppm)": "0", "Final CO (ppm)": "6", "Total Frames Shot": "57", "Fan display": "62", "Air display": "5", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; environment mismatch penalty
2. `Bhattacharjee:B2` **PI Bhattacharjee / Test B2 / 200 micron PMMA film   2 cm wide** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "22.2", "Calibrated final O2 % by vol": "1.6", "Initial CO2 % by vol": "0.44", "Final CO2 % by vol": "", "Initial CO (ppm)": "6", "Final CO (ppm)": "", "Total Frames Shot": "none", "Fan display": "62", "Air display": "5", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; environment mismatch penalty
3. `Bhattacharjee:B4` **PI Bhattacharjee / Test B4 / 300 micron PMMA film   2 cm wide** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "22.2", "Calibrated final O2 % by vol": "22.2", "Initial CO2 % by vol": "0.44", "Final CO2 % by vol": "0.51", "Initial CO (ppm)": "-1", "Final CO (ppm)": "10", "Total Frames Shot": "137", "Fan display": "61", "Air display": "5", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; environment mismatch penalty
4. `Bhattacharjee:B6` **PI Bhattacharjee / Test B6 / 2 cm 0.1 mm PMMA film** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "21", "Calibrated final O2 % by vol": "20.9", "Initial CO2 % by vol": "0.33", "Final CO2 % by vol": "0.41", "Initial CO (ppm)": "0", "Final CO (ppm)": "0.3", "Total Frames Shot": "80", "Fan display": "0.9   1.3   2.75", "Air display": "3   5   approaching 10", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; environment mismatch penalty
5. `Bhattacharjee:B8` **PI Bhattacharjee / Test B8 / 2 cm   0.2 mm PMMA film** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "21", "Calibrated final O2 % by vol": "20.5", "Initial CO2 % by vol": "0.33", "Final CO2 % by vol": "0.58", "Initial CO (ppm)": "0", "Final CO (ppm)": "131", "Total Frames Shot": "226", "Fan display": "1.4    incr to 10.0", "Air display": "10   max", "Flow restrictor": "0"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; environment mismatch penalty

**Final:** local 5, NASA 5, BASS-II 5, combined 10, unique sources 9, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `27.31/6000.69/32.26 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T1-04 ? Effect of oxygen concentration on flame spread in microgravity

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `35.28/24.43/36.04 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.725` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: However,   one  of the most  important   results   is that,  in microgravity,    the extinction   of the  polyethylene occurs  almost  immediately   when  the  flow  of relatively  low oxygen   concentration    (C  = 21  percent)   stops.
   - Explanation: matched terms: concentration, microgravity, oxygen; scientific concepts: microgravity, oxygen concentration; conditions: microgravity, oxygen; environments: microgravity; quantitative oxygen measurement context
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.3262` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity; phenomena: flame spread; environments: microgravity; quantitative measurement context missing
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.27` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                      pressure (100 kPa)  in reduced  gravity.
   - Explanation: matched terms: flame, spread; scientific concepts: microgravity, flame spread; phenomena: flame spread; environments: microgravity; quantitative measurement context missing
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.1013` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Explanation: matched terms: flame, spread; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty; quantitative measurement context missing
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2812` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: concentration, microgravity, oxygen; scientific concepts: microgravity, oxygen concentration; conditions: microgravity, oxygen; environments: microgravity; quantitative measurement context missing

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `32.52/39.11/19.83 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T1-05 ? Effect of forced airflow on flame propagation

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `34.4/11.82/16.11 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.53` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: The  flame-propagation      rate VF÷ obtained   in the ground   testing  appeared   to be lower than  V_:"from  the space  experiment   on Mir.
   - Explanation: matched terms: flame, propagation; scientific concepts: flame spread; phenomena: flame spread
2. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.53` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Explanation: matched terms: effect, flame; scientific concepts: flame spread; phenomena: flame spread
3. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.53` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Considering that the initial purpose of the     computed from a Monte Carlo propagation analysis, images recorded during the experiments was to use      considering a conservative error of 5% on the signal the data to visualize the flame and track its evolu-       ratio ΘG/R, resulting in 117 K of uncertainty for tem- tion over time, i.e., pyrolysis length, flame size, etc.,       perature determination.
   - Explanation: matched terms: flame, propagation; scientific concepts: flame spread; phenomena: flame spread
4. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.44` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: flame; scientific concepts: flame spread; phenomena: flame spread
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.53` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: NUMBER OF PAGES                                                                                                                     62         Extinction;      Fire   safety;   Flammability;      Flammability        limits;   Flame    propagation;                                                                                                                                                                           16.
   - Explanation: matched terms: flame, propagation; scientific concepts: flame spread; phenomena: flame spread

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `18.29/15.08/8.26 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T1-06 ? Flame spread and extinction in spacecraft environments

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `15.89/10.22/8.6 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.28` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: environment, spacecraft; environments: spacecraft
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.279` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: environment, flame, spread; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.279` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `simulation` | review `requires_manual_review`
   - Excerpt/fields: From the results, it is seen that the simulations performed using finite rate chemistry underpredict the experimental spread rates at the higher pressures, while not even allowing flame spread at the lower pressure environments.
   - Explanation: matched terms: environment, flame, spread; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.2385` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the                                                   measure the soot concentration (laser extinction) andmaterial.
   - Explanation: matched terms: extinction, flame; scientific concepts: flame spread, flame extinction; phenomena: flame extinction; environment mismatch penalty
5. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.279` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Explanation: matched terms: environment, flame, spread; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `21.57/11.54/10.03 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T1-07 ? NASA experiments on flame spread in reduced gravity

**Baseline:** local 5, NASA 5, BASS-II 0, combined 10, unique sources 9, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_experimental_conditions_not_covered), latency local/combined/BASS-II `26.84/2415.12/33.02 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.65` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Preliminary    results  of polyethylene-insulation      flammability    in microgravity   were  obtained   in the NASA  Wire Insulation   Flammability   (WIF)  experiment   during  the Space  Shuttle   flight  STS-50   (refs.
   - Explanation: matched terms: experiment, nasa; scientific concepts: microgravity, polyethylene; material: polyethylene; environments: microgravity
2. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.2` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                      pressure (100 kPa)  in reduced  gravity.
   - Explanation: matched terms: flame, gravity, reduced, spread; scientific concepts: microgravity, flame spread; conditions: reduced gravity; phenomena: flame spread; environments: microgravity; material mismatch penalty
3. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.1687` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: experiment, flame, spread; scientific concepts: microgravity, flame spread; phenomena: flame spread; environments: microgravity; material mismatch penalty
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.0563` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Explanation: matched terms: flame, spread; scientific concepts: flame spread; phenomena: flame spread; material mismatch penalty; environment mismatch penalty
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2925` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: The  rates  of material   burning-out    for  Russian-made  PMMA  and  polyethylene    are  less than  0.05  mm/s  at a flow velocity  V = 10 cm/s  and C, x= 21 percent,    i.e., 5 to 10 times  lower  than  the  flame-spread    rates  measured   for  the melting   materials   that  were  tested.
   - Explanation: matched terms: flame, spread; scientific concepts: flame spread, polyethylene; material: polyethylene; phenomena: flame spread; environment mismatch penalty

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `16.22/32.2/10.9 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T2-01 ? Spacecraft fire safety research

**Baseline:** local 2, NASA 5, BASS-II 0, combined 7, unique sources 6, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `31.41/2837.24/20.56 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2137` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: NUMBER OF PAGES                                                                                                                     62         Extinction;      Fire   safety;   Flammability;      Flammability        limits;   Flame    propagation;                                                                                                                                                                           16.
   - Explanation: matched terms: fire, safety; scientific concepts: fire hazard; environment mismatch penalty
2. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2125` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: spacecraft; environments: spacecraft

**Final NASA top five:**
1. `20150000894` **Large-Scale Spacecraft Fire Safety Tests** | score `0.8` | URL `https://ntrs.nasa.gov/citations/20150000894` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: An international collaborative program is underway to address open issues in spacecraft fire safety. Because of limited access to long-term low-gravity conditions and the small volume generally allotted for these experiments, there have been relatively few experiments that directly study spacecraft fire safety under low-gravity conditions. Furthermore, none of these experiments have studied sample sizes and environment conditions typical of those expected in a spacecraft fire. The major constrai
   - Explanation: matched terms: fire, research, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft
2. `20130001713` **Large Scale Experiments on Spacecraft Fire Safety** | score `0.8` | URL `https://ntrs.nasa.gov/citations/20130001713` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Full scale fire testing complemented by computer modelling has provided significant knowhow about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour i
   - Explanation: matched terms: fire, research, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft
3. `20130000677` **Large Scale Experiments on Spacecraft Fire Safety** | score `0.8` | URL `https://ntrs.nasa.gov/citations/20130000677` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Full scale fire testing complemented by computer modelling has provided significant know how about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour 
   - Explanation: matched terms: fire, research, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft
4. `20140011433` **Large-Scale Spacecraft Fire Safety Experiments in ISS Resupply Vehicles** | score `0.8` | URL `https://ntrs.nasa.gov/citations/20140011433` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Our understanding of the fire safety risk in manned spacecraft has been limited by the small scale of the testing we have been able to conduct in low-gravity. Fire growth and spread cannot be expected to scale linearly with sample size so we cannot make accurate predictions of the behavior of realistic scale fires in spacecraft based on the limited low-g testing to date. As a result, spacecraft fire safety protocols are necessarily very conservative and costly. Future crewed missions are expecte
   - Explanation: matched terms: fire, research, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft
5. `20170007283` **Spacecraft Fire Safety Research at NASA Glenn Research Center** | score `0.8` | URL `https://ntrs.nasa.gov/citations/20170007283` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Appropriate design of fire detection systems requires knowledge of both the expected fire signature and the background aerosol levels. Terrestrial fire detection systems have been developed based on extensive study of terrestrial fires. Unfortunately there is no corresponding data set for spacecraft fires and consequently the fire detectors in current spacecraft were developed based upon terrestrial designs. In low gravity, buoyant flow is negligible which causes particles to concentrate at the 
   - Explanation: matched terms: fire, research, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft

**Final BASS-II top five:**
No records returned.

**Final:** local 2, NASA 5, BASS-II 0, combined 7, unique sources 6, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `11.14/2258.64/29.87 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T2-02 ? Fire hazards aboard spacecraft

**Baseline:** local 2, NASA 5, BASS-II 0, combined 7, unique sources 6, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `35.07/2208.36/26.96 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2125` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: spacecraft; environments: spacecraft
2. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.1631` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: NUMBER OF PAGES                                                                                                                     62         Extinction;      Fire   safety;   Flammability;      Flammability        limits;   Flame    propagation;                                                                                                                                                                           16.
   - Explanation: matched terms: fire; scientific concepts: fire hazard; environment mismatch penalty

**Final NASA top five:**
1. `19930074562` **Fire safety design considerations for advanced space vehicles** | score `0.8` | URL `https://ntrs.nasa.gov/citations/19930074562` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: The desire to understand and explore space has driven man to overcome the confines of the Earth's atmosphere and accept the challenge of spaceflight. With our increasing ability to travel, work, and explore in space comes a need for a better understanding of the hazards in this relatively new endeavor. One of the most important and immediate needs is to be able to predict the ignition, spread, and growth of fire on board spacecraft. Fire safety aboard spacecraft has always been a concern; howeve
   - Explanation: matched terms: aboard, fire, hazard, spacecraft; scientific concepts: fire hazard; environments: spacecraft
2. `19880003145` **Space station internal environmental and safety concerns** | score `0.8` | URL `https://ntrs.nasa.gov/citations/19880003145` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Space station environmental and safety concerns, especially those involving fires, are discussed. Several types of space station modules and the particular hazards associated with each are briefly surveyed. A brief history of fire detection and suppression aboard spacecraft is given. Microgravity fire behavior, spacecraft fire detector systems, space station fire suppression equipment and procedures, and fire safety in hyperbaric chambers are discussed.
   - Explanation: matched terms: aboard, fire, hazard, spacecraft; scientific concepts: fire hazard; environments: spacecraft
3. `20020064975` **No Moving Parts** | score `0.8` | URL `https://ntrs.nasa.gov/citations/20020064975` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Under a NASA SBIR (Small Business Innovative Research), Research International developed the solid state micromachined pump used for cooling electronics in space, circulation of heat transfer fluids on spacecraft, and monitoring fire and gas hazards aboard naval warships. Incorporating Lewis Research Center's pumping technology, commercial applications for this product include both detection of toxins and pollutants in coal mines, and early warning smoke detectors for industrial applications.
   - Explanation: matched terms: aboard, fire, hazard, spacecraft; scientific concepts: fire hazard; environments: spacecraft
4. `20150008051` **Portable 4.6 Micrometers Laser Absorption Spectrometer for Carbon Monoxide Monitoring and Fire Detection** | score `0.8` | URL `https://ntrs.nasa.gov/citations/20150008051` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: The air quality aboard manned spacecraft must be continuously monitored to ensure crew safety and identify equipment malfunctions. In particular, accurate real-time monitoring of carbon monoxide (CO) levels helps to prevent chronic exposure and can also provide early detection of combustion-related hazards. For long-duration missions, environmental monitoring grows in importance, but the mass and volume of monitoring instruments must be minimized. Furthermore, environmental analysis beyond low-E
   - Explanation: matched terms: aboard, fire, hazard, spacecraft; scientific concepts: fire hazard; environments: spacecraft
5. `19970020602` **Gravitational Influences on Flame Propagation Through Non-Uniform Premixed Gas Systems** | score `0.8` | URL `https://ntrs.nasa.gov/citations/19970020602` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Flame spread through uniformly premixed gas systems, while not completely understood, is nevertheless a well-studied problem in combustion science. In contrast, flame propagation through non-uniform premixed gas systems (also called "'layered systems") has been the subject of relatively few previous studies. In a recent theoretical paper Talley lists sprays, flame spread over liquids, and the leading edge of lifted turbulent diffusion flames as applications where flame behavior in layers is impo
   - Explanation: matched terms: aboard, fire, hazard, spacecraft; scientific concepts: fire hazard; environments: spacecraft

**Final BASS-II top five:**
No records returned.

**Final:** local 2, NASA 5, BASS-II 0, combined 7, unique sources 6, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_scientific_concepts_not_covered), latency local/combined/BASS-II `26.19/1703.54/23.7 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T2-03 ? Fire detection and suppression in spacecraft

**Baseline:** local 2, NASA 5, BASS-II 0, combined 7, unique sources 6, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `35.58/2477.0/21.65 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2125` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: spacecraft; environments: spacecraft
2. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.0506` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: NUMBER OF PAGES                                                                                                                     62         Extinction;      Fire   safety;   Flammability;      Flammability        limits;   Flame    propagation;                                                                                                                                                                           16.
   - Explanation: matched terms: fire; environment mismatch penalty

**Final NASA top five:**
1. `20000120278` **Progress in Fire Detection and Suppression Technology for Future Space Missions** | score `0.9` | URL `https://ntrs.nasa.gov/citations/20000120278` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Fire intervention technology (detection and suppression) is a critical part of the strategy of spacecraft fire safety. This paper reviews the status, trends, and issues in fire intervention, particularly the technology applied to the protection of the International Space Station and future missions beyond Earth orbit. An important contribution to improvements in spacecraft fire safety is the understanding of the behavior of fires in the non-convective (microgravity) environment of Earth-orbiting
   - Explanation: matched terms: detection, fire, spacecraft, suppression; scientific concepts: fire detection, fire suppression; phenomena: fire detection, fire suppression; environments: spacecraft
2. `19890015042` **Fire safety applications for spacecraft** | score `0.9` | URL `https://ntrs.nasa.gov/citations/19890015042` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Fire safety for spacecraft is reviewed by first describing current practices, many of which are adapted directly from aircraft. Then, current analyses and experimental knowledge in low-gravity combustion, with implications for fire safety are discussed. In orbiting spacecraft, the detection and suppression of flames are strongly affected by the large reduction in buoyant flows under low gravity. Generally, combustion intensity is reduced in low gravity. There are some notable exceptions, however
   - Explanation: matched terms: detection, fire, spacecraft, suppression; scientific concepts: fire detection, fire suppression; phenomena: fire detection, fire suppression; environments: spacecraft
3. `20150000894` **Large-Scale Spacecraft Fire Safety Tests** | score `0.9` | URL `https://ntrs.nasa.gov/citations/20150000894` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: An international collaborative program is underway to address open issues in spacecraft fire safety. Because of limited access to long-term low-gravity conditions and the small volume generally allotted for these experiments, there have been relatively few experiments that directly study spacecraft fire safety under low-gravity conditions. Furthermore, none of these experiments have studied sample sizes and environment conditions typical of those expected in a spacecraft fire. The major constrai
   - Explanation: matched terms: detection, fire, spacecraft, suppression; scientific concepts: fire detection, fire suppression; phenomena: fire detection, fire suppression; environments: spacecraft
4. `20030053427` **Spacecraft Fire Safety: A Human Space Flight Program Perspective** | score `0.9` | URL `https://ntrs.nasa.gov/citations/20030053427` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This paper presents viewgraphs on the International Space Station's fire safety program from a human space flight perspective. The topics include: 1) Typical Manned Spacecraft Materials; 2) Typical Flammable Hardware Protection; 3) Materials Flammability; 4) Fire Retardants; 5) Nonflammable Foam Cushion Material; 6) Electrical Wire and Cable; 7) Russian Solid-Fuel Oxygen Generator (SFOG); 8) GOX Ignition Mechanisms; 9) Fire Detection; and 10) Fire Suppression.
   - Explanation: matched terms: detection, fire, spacecraft, suppression; scientific concepts: fire detection, fire suppression; phenomena: fire detection, fire suppression; environments: spacecraft
5. `20070010766` **Technology Development for Fire Safety in Exploration Spacecraft and Habitats** | score `0.9` | URL `https://ntrs.nasa.gov/citations/20070010766` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Fire during an exploration mission far from Earth is a particularly critical risk for exploration vehicles and habitats. The Fire Prevention, Detection, and Suppression (FPDS) project is part of the Exploration Technology Development Program (ETDP) and has the goal to enhance crew health and safety on exploration missions by reducing the likelihood of a fire, or, if one does occur, minimizing the risk to the mission, crew, or system. Within the past year, the FPDS project has been formalized wit
   - Explanation: matched terms: detection, fire, spacecraft, suppression; scientific concepts: fire detection, fire suppression; phenomena: fire detection, fire suppression; environments: spacecraft

**Final BASS-II top five:**
No records returned.

**Final:** local 2, NASA 5, BASS-II 0, combined 7, unique sources 6, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_scientific_concepts_not_covered), latency local/combined/BASS-II `25.12/6416.12/31.19 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T2-04 ? Material flammability in spacecraft cabin environments

**Baseline:** local 5, NASA 2, BASS-II 0, combined 7, unique sources 5, duplicates 2, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `19.34/1696.23/25.71 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.37` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: environment, material, spacecraft; environments: spacecraft, spacecraft cabin
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.0405` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: environment; environment mismatch penalty
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.0405` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `simulation` | review `requires_manual_review`
   - Excerpt/fields: From the results, it is seen that the simulations performed using finite rate chemistry underpredict the experimental spread rates at the higher pressures, while not even allowing flame spread at the lower pressure environments.
   - Explanation: matched terms: environment; environment mismatch penalty
4. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.081` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: 1.3.2 Procedure   and  Results   of Narrow  Channel   Testing.--The    Narrow  Channel   test  in the  apparatus   on  fig- ure  1.7 evaluates   material   flammability    in terms  of  V,,,,, determined    at a prescribed   oxygen   concentration   C   (greater than  C,,m).
   - Explanation: matched terms: flammability, material; environment mismatch penalty
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.081` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: TABLE   1.2.--GROUND-TESTING       RESULTS   OF  U.S.-PROVIDED    MATERIAL                                FLAMMABILITY        --  LIMITING   VELOCITY      [Vb,,,' ) DETERMINED     IN                                      APPARATUSES    WITH  SUPPRESSED    CONVECTION                        Number                   Material                                                        Vi.., cm/sec                                                                        Narrow   channel              Vertical
   - Explanation: matched terms: flammability, material; environment mismatch penalty

**Final NASA top five:**
1. `20260003042` **Fire-Resistant Textile Development for Exploration Vehicles With Enriched-Oxygen Cabin Environments** | score `0.55` | URL `https://ntrs.nasa.gov/citations/20260003042` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Material selection is a key part of the National Aeronautics and Space Administration (NASA) spacecraft fire safety management plan. Non-flammable textiles are necessary to ensure large-scale flame propagation events do not occur inside a spacecraft. An increased use of textiles and other softgood material is crucial to the pursuit of exploration spaceflight to reduce mass and volume. Exploration spaceflight missions benefit from enriched oxygen cabin environments (>21% O2) by allowing a reduced
   - Explanation: matched terms: cabin, environment, flammability, material, spacecraft; environments: spacecraft, spacecraft cabin
2. `20100019472` **Operational Considerations for Oxygen Flammability Risks: Concentrated Oxygen Diffusion and Permeation Behaviors** | score `0.55` | URL `https://ntrs.nasa.gov/citations/20100019472` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Increased human spaceflight operations utilize oxygen concentrations that are frequently varied with use of concentrations up to 100 percent oxygen. Even after exiting a higher percentage oxygen environment, high oxygen concentrations can still be maintained due to material saturation and oxygen entrapment between barrier materials. This paper examines the material flammability concerns that arise from changing oxygen environments during spaceflight operations. We examine the time required for c
   - Explanation: matched terms: cabin, environment, flammability, material, spacecraft; environments: spacecraft, spacecraft cabin

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 2, BASS-II 0, combined 7, unique sources 5, duplicates 2, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `36.28/1666.93/33.34 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T2-05 ? NASA spacecraft fire safety experiments

**Baseline:** local 5, NASA 5, BASS-II 0, combined 10, unique sources 9, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `33.55/2765.72/32.43 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.261` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Preliminary    results  of polyethylene-insulation      flammability    in microgravity   were  obtained   in the NASA  Wire Insulation   Flammability   (WIF)  experiment   during  the Space  Shuttle   flight  STS-50   (refs.
   - Explanation: matched terms: experiment, nasa; scientific concepts: polyethylene; material: polyethylene; environment mismatch penalty
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.0101` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: experiment; material mismatch penalty; environment mismatch penalty
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.0101` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `simulation` | review `requires_manual_review`
   - Excerpt/fields: It is seen that, in spite of the simplifications included in the model, the simulations are able to qualitatively reproduce the overall behavior observed during the experiments: at lower ambient pressures the time evolution of the pyrolysis front and burnout front positions over the sample length  is slower, i.e.
   - Explanation: matched terms: experiment; material mismatch penalty; environment mismatch penalty
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.0101` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Considering that the initial purpose of the     computed from a Monte Carlo propagation analysis, images recorded during the experiments was to use      considering a conservative error of 5% on the signal the data to visualize the flame and track its evolu-       ratio ΘG/R, resulting in 117 K of uncertainty for tem- tion over time, i.e., pyrolysis length, flame size, etc.,       perature determination.
   - Explanation: matched terms: experiment; material mismatch penalty; environment mismatch penalty
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.07` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: experiment, spacecraft; environments: spacecraft; material mismatch penalty

**Final NASA top five:**
1. `20150000894` **Large-Scale Spacecraft Fire Safety Tests** | score `0.2` | URL `https://ntrs.nasa.gov/citations/20150000894` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: An international collaborative program is underway to address open issues in spacecraft fire safety. Because of limited access to long-term low-gravity conditions and the small volume generally allotted for these experiments, there have been relatively few experiments that directly study spacecraft fire safety under low-gravity conditions. Furthermore, none of these experiments have studied sample sizes and environment conditions typical of those expected in a spacecraft fire. The major constrai
   - Explanation: matched terms: experiment, fire, nasa, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft; material mismatch penalty
2. `20140006578` **Development of Large-Scale Spacecraft Fire Safety Experiments** | score `0.2` | URL `https://ntrs.nasa.gov/citations/20140006578` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: The status is presented of a spacecraft fire safety research project that is under development to reduce the uncertainty and risk in the design of spacecraft fire safety systems by testing at nearly full scale in low-gravity. Future crewed missions are expected to be more complex and longer in duration than previous exploration missions outside of low-earth orbit. This will increase the challenge of ensuring a fire-safe environment for the crew throughout the mission. Based on our fundamental un
   - Explanation: matched terms: experiment, fire, nasa, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft; material mismatch penalty
3. `19930019549` **Risk-based Spacecraft Fire Safety Experiments** | score `0.1775` | URL `https://ntrs.nasa.gov/citations/19930019549` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Viewgraphs on risk-based spacecraft fire safety experiments are presented. Spacecraft fire risk can never be reduced to a zero probability. Probabilistic risk assessment is a tool to reduce risk to an acceptable level.
   - Explanation: matched terms: experiment, fire, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft; material mismatch penalty
4. `20130000677` **Large Scale Experiments on Spacecraft Fire Safety** | score `0.1775` | URL `https://ntrs.nasa.gov/citations/20130000677` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Full scale fire testing complemented by computer modelling has provided significant know how about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour 
   - Explanation: matched terms: experiment, fire, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft; material mismatch penalty
5. `20130001713` **Large Scale Experiments on Spacecraft Fire Safety** | score `0.1775` | URL `https://ntrs.nasa.gov/citations/20130001713` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Full scale fire testing complemented by computer modelling has provided significant knowhow about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour i
   - Explanation: matched terms: experiment, fire, safety, spacecraft; scientific concepts: fire hazard; environments: spacecraft; material mismatch penalty

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 5, BASS-II 0, combined 10, unique sources 9, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_environment_not_covered, required_scientific_concepts_not_covered), latency local/combined/BASS-II `38.97/2597.87/27.64 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T2-06 ? Fire behavior in enclosed spacecraft environments

**Baseline:** local 5, NASA 2, BASS-II 0, combined 7, unique sources 5, duplicates 2, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `15.49/3581.69/28.66 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.28` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: environment, spacecraft; environments: spacecraft, spacecraft cabin
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.0405` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: environment; environment mismatch penalty
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.0405` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `simulation` | review `requires_manual_review`
   - Excerpt/fields: It is seen that, in spite of the simplifications included in the model, the simulations are able to qualitatively reproduce the overall behavior observed during the experiments: at lower ambient pressures the time evolution of the pyrolysis front and burnout front positions over the sample length  is slower, i.e.
   - Explanation: matched terms: behavior; environment mismatch penalty
4. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.0405` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Explanation: matched terms: environment; environment mismatch penalty
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.0405` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: NUMBER OF PAGES                                                                                                                     62         Extinction;      Fire   safety;   Flammability;      Flammability        limits;   Flame    propagation;                                                                                                                                                                           16.
   - Explanation: matched terms: fire; environment mismatch penalty

**Final NASA top five:**
1. `20040053504` **Seventh International Workshop on Microgravity Combustion and Chemically Reacting Systems** | score `0.28` | URL `https://ntrs.nasa.gov/citations/20040053504` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: The Seventh International Workshop on Microgravity Combustion and Chemically Reacting Systems was planned for June 3-6, 2003, in Cleveland, Ohio, near the NASA John H. Glenn Research Center at Lewis Field. The new name for the workshop is based on the decision to broaden our scope to encompass support for future space exploration through basic and applied research in reacting systems that in some cases may not look like combustion. The workshop has been lengthened to 4 days with focus sessions o
   - Explanation: matched terms: fire, spacecraft; environments: spacecraft
2. `20010073993` **Sixth International Microgravity Combustion Workshop** | score `0.081` | URL `https://ntrs.nasa.gov/citations/20010073993` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This conference proceedings document is a compilation of papers presented orally or as poster displays to the Sixth International Microgravity Combustion Workshop held in Cleveland, Ohio on May 22-24, 2001. The purpose of the workshop is to present and exchange research results from theoretical and experimental work in combustion science using the reduced-gravity environment as a research tool. The results are contributed by researchers funded by NASA throughout the United States at universities
   - Explanation: matched terms: environment, fire; environment mismatch penalty

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 2, BASS-II 0, combined 7, unique sources 5, duplicates 2, fallback `True` (too_few_local_passages, insufficient_local_source_coverage), latency local/combined/BASS-II `31.86/4464.74/21.79 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T2-07 ? Spacecraft cabin atmosphere and combustion hazards

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 2, duplicates 3, fallback `False` (none), latency local/combined/BASS-II `28.56/33.5/35.53 ms`.

**Final local top five:**
1. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.198` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: combustion; scientific concepts: solid fuel combustion; phenomena: combustion; environment mismatch penalty
2. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.198` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: When  velocity   is  1.1 cm/s,  both combustion   and  extinction   are observed.
   - Explanation: matched terms: combustion; scientific concepts: solid fuel combustion; phenomena: combustion; environment mismatch penalty
3. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.198` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: These  measurements    were  obtained   during  the  initial  phase  of combustion    (the  first 15 to 20 sec  alter  ignition),  when  the samples    still  keep  their  original   shape.
   - Explanation: matched terms: combustion; scientific concepts: solid fuel combustion; phenomena: combustion; environment mismatch penalty
4. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.198` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: 3.4 Non-Steadiness    and Other  Characteristics    of Combustion    in Microgravity      The  nonsteadiness    of polymer   combustion    observed   in the space  experiment   might  be explained   by two reasons:   (1)  the formation   of the  melt  drop,  which   is almost   spherical   tbr  Delrin  and PMMA   (see  figs.
   - Explanation: matched terms: combustion; scientific concepts: solid fuel combustion; phenomena: combustion; environment mismatch penalty
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.198` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: By the end  of the  experiment, the diameter   of the melt  ball  is 2 to 2.5 times  greater  than  the  initial  diameter   of the  cylindrical   sample,  and  the shape  of the sample  changes   drastically   during  combustion.
   - Explanation: matched terms: combustion; scientific concepts: solid fuel combustion; phenomena: combustion; environment mismatch penalty

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 2, duplicates 3, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_environment_not_covered, required_scientific_concepts_not_covered), latency local/combined/BASS-II `41.45/1284.59/24.38 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T3-01 ? Effect of oxygen concentration on flame propagation

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `34.63/43.12/16.19 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.58` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: However,   one  of the most  important   results   is that,  in microgravity,    the extinction   of the  polyethylene occurs  almost  immediately   when  the  flow  of relatively  low oxygen   concentration    (C  = 21  percent)   stops.
   - Explanation: matched terms: concentration, oxygen; scientific concepts: oxygen concentration; conditions: oxygen; quantitative oxygen measurement context
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.261` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Explanation: matched terms: flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; phenomena: flame spread; quantitative measurement context missing
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.2385` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Explanation: matched terms: effect, flame; scientific concepts: flame spread; phenomena: flame spread; quantitative measurement context missing
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.2385` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Considering that the initial purpose of the     computed from a Monte Carlo propagation analysis, images recorded during the experiments was to use      considering a conservative error of 5% on the signal the data to visualize the flame and track its evolu-       ratio ΘG/R, resulting in 117 K of uncertainty for tem- tion over time, i.e., pyrolysis length, flame size, etc.,       perature determination.
   - Explanation: matched terms: flame, propagation; scientific concepts: flame spread; phenomena: flame spread; quantitative measurement context missing
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.58` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: This  discrep- ancy  might  be explained   by higher  oxygen   concentration     at the  test times  (23.6  percent   instead   of 22.5  percent).
   - Explanation: matched terms: concentration, oxygen; scientific concepts: oxygen concentration; conditions: oxygen; quantitative oxygen measurement context

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `29.91/29.88/44.76 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T3-02 ? Oxygen concentration and flame spread in microgravity

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `25.81/32.76/44.5 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.77` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: However,   one  of the most  important   results   is that,  in microgravity,    the extinction   of the  polyethylene occurs  almost  immediately   when  the  flow  of relatively  low oxygen   concentration    (C  = 21  percent)   stops.
   - Explanation: matched terms: concentration, microgravity, oxygen; scientific concepts: microgravity, oxygen concentration; conditions: microgravity, oxygen; environments: microgravity; quantitative oxygen measurement context
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.3465` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: flame, microgravity, spread; scientific concepts: microgravity, flame spread; conditions: microgravity; phenomena: flame spread; environments: microgravity; quantitative measurement context missing
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.2835` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                      pressure (100 kPa)  in reduced  gravity.
   - Explanation: matched terms: flame, spread; scientific concepts: microgravity, flame spread; phenomena: flame spread; environments: microgravity; quantitative measurement context missing
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.1073` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Explanation: matched terms: flame, spread; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty; quantitative measurement context missing
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.3015` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: concentration, microgravity, oxygen; scientific concepts: microgravity, oxygen concentration; conditions: microgravity, oxygen; environments: microgravity; quantitative measurement context missing

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `32.15/22.84/14.86 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T3-03 ? Limiting oxygen concentration for flame extinction

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `42.06/30.13/28.38 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.77` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: However,   one  of the most  important   results   is that,  in microgravity,    the extinction   of the  polyethylene occurs  almost  immediately   when  the  flow  of relatively  low oxygen   concentration    (C  = 21  percent)   stops.
   - Explanation: matched terms: concentration, extinction, oxygen; scientific concepts: oxygen concentration, flame extinction; conditions: oxygen; phenomena: flame extinction; quantitative oxygen measurement context
2. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.279` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the                                                   measure the soot concentration (laser extinction) andmaterial.
   - Explanation: matched terms: concentration, extinction, flame; scientific concepts: flame spread, oxygen concentration, flame extinction; phenomena: flame extinction; quantitative measurement context missing
3. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.216` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Explanation: matched terms: flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; quantitative measurement context missing
4. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.153` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Explanation: matched terms: flame; scientific concepts: flame spread; quantitative measurement context missing
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.58` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: This  discrep- ancy  might  be explained   by higher  oxygen   concentration     at the  test times  (23.6  percent   instead   of 22.5  percent).
   - Explanation: matched terms: concentration, oxygen; scientific concepts: oxygen concentration; conditions: oxygen; quantitative oxygen measurement context

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `19.93/12.75/16.66 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T3-04 ? Effect of oxygen percentage on solid material combustion

**Baseline:** local 5, NASA 1, BASS-II 0, combined 6, unique sources 4, duplicates 2, fallback `True` (insufficient_local_source_coverage), latency local/combined/BASS-II `60.65/1488.03/38.78 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.625` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: However,   one  of the most  important   results   is that,  in microgravity,    the extinction   of the  polyethylene occurs  almost  immediately   when  the  flow  of relatively  low oxygen   concentration    (C  = 21  percent)   stops.
   - Explanation: matched terms: oxygen; scientific concepts: oxygen concentration, polyethylene; material: polyethylene; conditions: oxygen; quantitative oxygen measurement context
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.0563` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: N96- 15553                                     Solid  Surface  Combustion   Experiment                     Flame  Spread  in a Quiescent,   Microgravity   Environment                             Implications    of Spread  Rate and Flame  Structure                        Matthew   Bundy,    Jeff West,  Peter  C.
   - Explanation: matched terms: combustion, solid; scientific concepts: solid fuel combustion; phenomena: combustion; material mismatch penalty; quantitative measurement context missing
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.0366` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: From the                                                                              figure,  it is seen that as ambient pressure is                                                                     reduced, the flame spread rate over the solid                                                                 approaches that obtained at standard ambient                                                                      pressure (100 kPa)  in reduced  gravity.
   - Explanation: matched terms: solid; scientific concepts: solid fuel combustion; material mismatch penalty; quantitative measurement context missing
4. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2925` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: TABLE   1.2.--GROUND-TESTING       RESULTS   OF  U.S.-PROVIDED    MATERIAL                                FLAMMABILITY        --  LIMITING   VELOCITY      [Vb,,,' ) DETERMINED     IN                                      APPARATUSES    WITH  SUPPRESSED    CONVECTION                        Number                   Material                                                        Vi.., cm/sec                                                                        Narrow   channel              Vertical
   - Explanation: matched terms: combustion, material; scientific concepts: polyethylene, solid fuel combustion; material: polyethylene; phenomena: combustion; quantitative measurement context missing
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2587` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: The  rates  of material   burning-out    for  Russian-made  PMMA  and  polyethylene    are  less than  0.05  mm/s  at a flow velocity  V = 10 cm/s  and C, x= 21 percent,    i.e., 5 to 10 times  lower  than  the  flame-spread    rates  measured   for  the melting   materials   that  were  tested.
   - Explanation: matched terms: material; scientific concepts: polyethylene; material: polyethylene; phenomena: combustion; quantitative measurement context missing

**Final NASA top five:**
1. `20010073996` **Solid Inflammability Boundary at Low-Speed (SIBAL)** | score `0.0956` | URL `https://ntrs.nasa.gov/citations/20010073996` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This research program is concerned with the effect of low-speed, concurrent flow on the spreading and extinction processes of flames over solid fuels. The primary objective is to verify the theoretically predicted extinction boundary, using oxygen percentage and flow velocity as coordinates. Of particular interest are the low-speed quenching limits and the existence of the critical oxygen flammability limit. Detailed flame spread characteristics, including flame spread rate, flame size, and flam
   - Explanation: matched terms: combustion, effect, material, oxygen, percentage, solid; scientific concepts: oxygen concentration, solid fuel combustion; conditions: oxygen; phenomena: combustion; material mismatch penalty; quantitative measurement context missing

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 1, BASS-II 0, combined 6, unique sources 4, duplicates 2, fallback `True` (insufficient_local_source_coverage), latency local/combined/BASS-II `49.87/1407.94/36.35 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T3-05 ? Oxygen concentration effects on PMMA flame spread

**Baseline:** local 5, NASA 4, BASS-II 5, combined 9, unique sources 8, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_experimental_conditions_not_covered, required_scientific_concepts_not_covered), latency local/combined/BASS-II `37.63/2530.02/29.76 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.3262` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: The  rates  of material   burning-out    for  Russian-made  PMMA  and  polyethylene    are  less than  0.05  mm/s  at a flow velocity  V = 10 cm/s  and C, x= 21 percent,    i.e., 5 to 10 times  lower  than  the  flame-spread    rates  measured   for  the melting   materials   that  were  tested.
   - Explanation: matched terms: flame, pmma, spread; scientific concepts: flame spread, polymethyl methacrylate; material: polymethyl methacrylate; phenomena: flame spread; quantitative measurement context missing
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.0703` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Explanation: matched terms: flame, oxygen, spread; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; phenomena: flame spread; material mismatch penalty; quantitative measurement context missing
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.0647` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Explanation: matched terms: effect, flame, spread; scientific concepts: flame spread; phenomena: flame spread; material mismatch penalty; quantitative measurement context missing
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.0563` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `unknown` | review `requires_manual_review`
   - Excerpt/fields: The relative uncertainty asso- the flame spreads over the composite fabric, it con-       ciated with the thermocouple reading has been esti- sumes most of the cotton, leaving behind the fiber-     mated following the work of Ren et al.
   - Explanation: matched terms: flame, spread; scientific concepts: flame spread; phenomena: flame spread; material mismatch penalty; quantitative measurement context missing
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.3262` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: TABLE   1.2.--GROUND-TESTING       RESULTS   OF  U.S.-PROVIDED    MATERIAL                                FLAMMABILITY        --  LIMITING   VELOCITY      [Vb,,,' ) DETERMINED     IN                                      APPARATUSES    WITH  SUPPRESSED    CONVECTION                        Number                   Material                                                        Vi.., cm/sec                                                                        Narrow   channel              Vertical
   - Explanation: matched terms: flame, pmma, spread; scientific concepts: flame spread, polymethyl methacrylate; material: polymethyl methacrylate; phenomena: flame spread; quantitative measurement context missing

**Final NASA top five:**
1. `19990053973` **Flow Effects on the Flammability Diagrams of Solid Fuels: Microgravity Influence on Ignition Delay** | score `0.45` | URL `https://ntrs.nasa.gov/citations/19990053973` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: The possibility of an accidental fire in space-based facilities is a primary concern of space exploration programs. Spacecraft environments generally present low velocity air currents produced by ventilation and heating systems (of the order of 0.1 m/s), and fluctuating oxygen concentrations around that of air due to CO2 removal systems. Recent experiments of flame spread in microgravity show the spread rate to be faster and the limiting oxygen concentration lower than in normal-gravity. To date
   - Explanation: matched terms: concentration, effect, flame, oxygen, pmma, spread; scientific concepts: flame spread, oxygen concentration, polymethyl methacrylate; material: polymethyl methacrylate; conditions: oxygen; phenomena: flame spread; quantitative measurement context missing
2. `20040161185` **Strategic Research to Enable NASA's Exploration Missions Conference and Workshop: Poster Session** | score `0.0084` | URL `https://ntrs.nasa.gov/citations/20040161185` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Reports are presented from volume 2 of the conference titled Strategic Research to Enable NASA's Exploration Missions, poster session. Topics included spacecraft fire suppression and fire extinguishing agents,materials flammability, various topics on the effects of microgravity including crystal growth, fluid mechanics, electric particulate suspension, melting and solidification, bubble formation, the sloshing of liquid fuels, biological studies, separation of carbon dioxide and carbon monoxide 
   - Explanation: matched terms: effect; material mismatch penalty; quantitative measurement context missing
3. `20040084137` **Strategic Research to Enable NASA's Exploration Missions Conference** | score `0.0084` | URL `https://ntrs.nasa.gov/citations/20040084137` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Abstracts are presented from a conference sponsored by the NASA Office of Biological and Physical Research and hosted by NASA Glenn Research Center and the National Center for Microgravity Research on Fluids and Combustion, held in Cleveland, Ohio, June 22-23, 2004. Topics pertained to the behavior of processes and materials in microgravity as well as physiological-biological studies and microgravity effects.
   - Explanation: matched terms: effect; material mismatch penalty; quantitative measurement context missing
4. `19960008386` **The 3rd International Microgravity Combustion Workshop** | score `0.0` | URL `https://ntrs.nasa.gov/citations/19960008386` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This Conference Publication contains 71 papers presented at the Third International Microgravity Combustion Workshop held in Cleveland, Ohio, from April 11 to 13, 1995. The purpose of the workshop was twofold: to exchange information about the progress and promise of combustion science in microgravity and to provide a forum to discuss which areas in microgravity combustion science need to be expanded profitably and which should be included in upcoming NASA Research Announcements (NRA).
   - Explanation: material mismatch penalty; quantitative measurement context missing

**Final BASS-II top five:**
1. `Bhattacharjee:B1` **PI Bhattacharjee / Test B1 / 100 micron PMMA film   2 cm wide** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "22.2", "Calibrated final O2 % by vol": "22.2", "Initial CO2 % by vol": "0.44", "Final CO2 % by vol": "0.44", "Initial CO (ppm)": "0", "Final CO (ppm)": "6", "Total Frames Shot": "57", "Fan display": "62", "Air display": "5", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; quantitative measurement context missing
2. `Bhattacharjee:B2` **PI Bhattacharjee / Test B2 / 200 micron PMMA film   2 cm wide** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "22.2", "Calibrated final O2 % by vol": "1.6", "Initial CO2 % by vol": "0.44", "Final CO2 % by vol": "", "Initial CO (ppm)": "6", "Final CO (ppm)": "", "Total Frames Shot": "none", "Fan display": "62", "Air display": "5", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; quantitative measurement context missing
3. `Bhattacharjee:B4` **PI Bhattacharjee / Test B4 / 300 micron PMMA film   2 cm wide** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "22.2", "Calibrated final O2 % by vol": "22.2", "Initial CO2 % by vol": "0.44", "Final CO2 % by vol": "0.51", "Initial CO (ppm)": "-1", "Final CO (ppm)": "10", "Total Frames Shot": "137", "Fan display": "61", "Air display": "5", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; quantitative measurement context missing
4. `Bhattacharjee:B6` **PI Bhattacharjee / Test B6 / 2 cm 0.1 mm PMMA film** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "21", "Calibrated final O2 % by vol": "20.9", "Initial CO2 % by vol": "0.33", "Final CO2 % by vol": "0.41", "Initial CO (ppm)": "0", "Final CO (ppm)": "0.3", "Total Frames Shot": "80", "Fan display": "0.9   1.3   2.75", "Air display": "3   5   approaching 10", "Flow restrictor": "2"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; quantitative measurement context missing
5. `Bhattacharjee:B8` **PI Bhattacharjee / Test B8 / 2 cm   0.2 mm PMMA film** | score `0.2137` | URL `BASS-II dataset` | evidence `structured BASS-II record` | review `not_scientifically_verified`
   - Excerpt/fields: {"Calibrated  initial O2 % by vol ": "21", "Calibrated final O2 % by vol": "20.5", "Initial CO2 % by vol": "0.33", "Final CO2 % by vol": "0.58", "Initial CO (ppm)": "0", "Final CO (ppm)": "131", "Total Frames Shot": "226", "Fan display": "1.4    incr to 10.0", "Air display": "10   max", "Flow restrictor": "0"}
   - Explanation: matched terms: pmma; scientific concepts: polymethyl methacrylate; material: polymethyl methacrylate; quantitative measurement context missing

**Final:** local 5, NASA 4, BASS-II 5, combined 9, unique sources 8, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_experimental_conditions_not_covered, required_quantitative_measurement_not_covered, required_scientific_concepts_not_covered), latency local/combined/BASS-II `28.97/2296.58/39.67 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T3-06 ? Oxygen availability and spacecraft fire propagation

**Baseline:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `30.99/24.18/20.52 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.58` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Measurements    of V,m and  Vvare  possible   in the microgravity   environment    of spacecraft,   however,    if the  material   is flammable   in the given  oxygen   concentration    in the  spacecraft   compartment    at the time  of the space  experiment   and  if the flow  velocity   in the  apparatus  chamber    is higher  than  a limiting   velocity   for the  material.
   - Explanation: matched terms: oxygen, spacecraft; scientific concepts: oxygen concentration; conditions: oxygen; environments: spacecraft
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.2205` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Explanation: matched terms: oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; phenomena: flame spread; environment mismatch penalty
3. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.198` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `simulation` | review `requires_manual_review`
   - Excerpt/fields: It should be noted that under this condition only partial burning of the sample near the igniter region was observed in the FDS simulations done at 50 kPa, and the flame would eventually blow off about 11 mm away from the igniter, thus no spread rate was determined for that condition due to the very short propagation length.
   - Explanation: matched terms: propagation; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty
4. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.198` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Considering that the initial purpose of the     computed from a Monte Carlo propagation analysis, images recorded during the experiments was to use      considering a conservative error of 5% on the signal the data to visualize the flame and track its evolu-       ratio ΘG/R, resulting in 117 K of uncertainty for tem- tion over time, i.e., pyrolysis length, flame size, etc.,       perature determination.
   - Explanation: matched terms: propagation; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2385` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: NUMBER OF PAGES                                                                                                                     62         Extinction;      Fire   safety;   Flammability;      Flammability        limits;   Flame    propagation;                                                                                                                                                                           16.
   - Explanation: matched terms: fire, propagation; scientific concepts: flame spread; phenomena: flame spread; environment mismatch penalty

**Final NASA top five:**
No records returned.

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 0, BASS-II 0, combined 5, unique sources 4, duplicates 1, fallback `False` (none), latency local/combined/BASS-II `37.77/30.05/26.4 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.

### T3-07 ? NASA experiments on oxygen concentration and flame behavior

**Baseline:** local 5, NASA 5, BASS-II 0, combined 10, unique sources 9, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_scientific_concepts_not_covered), latency local/combined/BASS-II `30.47/4447.47/17.81 ms`.

**Final local top five:**
1. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.7` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: However,   one  of the most  important   results   is that,  in microgravity,    the extinction   of the  polyethylene occurs  almost  immediately   when  the  flow  of relatively  low oxygen   concentration    (C  = 21  percent)   stops.
   - Explanation: matched terms: concentration, oxygen; scientific concepts: oxygen concentration, polyethylene; material: polyethylene; conditions: oxygen; quantitative oxygen measurement context
2. `19960008387` **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** | score `0.0506` | URL `https://ntrs.nasa.gov/citations/19960008387` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Thin  Fuel:   1.1 Spread  Rate: The  experimental   flame  spread  rates,   Vf.,_,,  over  the  thin cellulosic   fuel  in five different  quiescent  environments,    at three  different  ambient  pressures   and  two oxygen  levels,  are plotted  in Fig.
   - Explanation: matched terms: flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; material mismatch penalty; quantitative measurement context missing
3. `20220012861` **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** | score `0.045` | URL `https://ntrs.nasa.gov/citations/20220012861` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: [16] uses a pulsed laser to sequentiallyto observe the full development of the flame over the                                                   measure the soot concentration (laser extinction) andmaterial.
   - Explanation: matched terms: concentration, flame; scientific concepts: flame spread, oxygen concentration; material mismatch penalty; quantitative measurement context missing
4. `20210017787` **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** | score `0.0366` | URL `https://ntrs.nasa.gov/citations/20210017787` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Because of the size of the samples, and the accelerative characteristics of the flame, an averaged spread rate over the last 50% of the sample is presented so that the data are closer to the steady state value and transient effects are minimized, as explained in section A.
   - Explanation: matched terms: flame; scientific concepts: flame spread; material mismatch penalty; quantitative measurement context missing
5. `20000024924` **Experimental Verification of Material Flammability in Space** | score `0.2475` | URL `https://ntrs.nasa.gov/citations/20000024924` | evidence `experiment` | review `requires_manual_review`
   - Excerpt/fields: Preliminary    results  of polyethylene-insulation      flammability    in microgravity   were  obtained   in the NASA  Wire Insulation   Flammability   (WIF)  experiment   during  the Space  Shuttle   flight  STS-50   (refs.
   - Explanation: matched terms: experiment, nasa; scientific concepts: polyethylene; material: polyethylene; quantitative measurement context missing

**Final NASA top five:**
1. `20000000189` **The Effect of Velocity on the Extinction Behavior of a Diffusion Flame during Transient Depressurization** | score `0.2125` | URL `https://ntrs.nasa.gov/citations/20000000189` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Current fire suppression plans for the International Space Station include the use of venting (depressurization) as a method for extinguishing a fire. Until recently this process had only been examined as part of a material flammability experiment performed on Skylab in the early 1970's. Due to the low initial pressure (0.35 Atm) and high oxygen concentration (65%), the Skylab experimental results are not applicable for understanding the effects of venting on a fire in a space station environmen
   - Explanation: matched terms: behavior, concentration, experiment, flame, nasa, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; quantitative oxygen measurement context; material mismatch penalty
2. `20150022421` **Buoyant Effects on the Flammability of Silicone Samples Planned for the Spacecraft Fire Experiment (Saffire)** | score `0.0844` | URL `https://ntrs.nasa.gov/citations/20150022421` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Flammability experiments on silicone samples were conducted in anticipation of the Spacecraft Fire Experiment (Saffire). The sample geometry was chosen to match the NASA 6001 Test 1 specification, namely 5 cm wide by 30 cm tall. Four thicknesses of silicone (0.25, 0.36, 0.61 and 1.00 mm) were examined. Tests included traditional upward buoyant flame spread using Test 1 procedures, downward opposed-flow flame spread, horizontal and angled flame spread, and forced-flow upward and downward flame sp
   - Explanation: matched terms: behavior, concentration, experiment, flame, nasa, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; material mismatch penalty; quantitative measurement context missing
3. `20150022123` **Buoyant Effects on the Flammability of Silicone Samples Planned for the Spacecraft Fire Experiment (Saffire)** | score `0.0844` | URL `https://ntrs.nasa.gov/citations/20150022123` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: Flammability experiments on silicone samples were conducted in anticipation of the Spacecraft Fire Experiment (Saffire). The sample geometry was chosen to match the NASA 6001 Test 1 specification, namely 5 cm wide by 30 cm tall. Four thicknesses of silicone (0.25, 0.36, 0.61 and 1.00 mm) were examined. Tests included traditional upward buoyant flame spread using Test 1 procedures, downward opposed flow flame spread, horizontal and angled flame spread, forced flow upward and downward flame spread
   - Explanation: matched terms: behavior, concentration, experiment, flame, nasa, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; material mismatch penalty; quantitative measurement context missing
4. `20040161260` **Transition from Ignition to Flame Growth under External Radiation in 3D** | score `0.0759` | URL `https://ntrs.nasa.gov/citations/20040161260` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This study focuses on localized ignition by external radiant flux and subsequent flame growth over thin polymeric materials (plastic and paper) in microgravity. Two transition stages were observed. The first transition stage covers the period from the onset of ignition to the formation of stabilized flame near the ignited area. This is followed by the second transition of the flame growth stage from the initial stabilized flame to sustained fire growth away from the ignited area. For the first s
   - Explanation: matched terms: behavior, concentration, experiment, flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; material mismatch penalty; quantitative measurement context missing
5. `20000005087` **Candle Flames in Non-Buoyant Atmospheres** | score `0.0759` | URL `https://ntrs.nasa.gov/citations/20000005087` | evidence `bibliographic_metadata_and_abstract` | review `not_scientifically_reviewed`
   - Excerpt/fields: This paper addresses the behavior of a candle flame in a long-duration, quiescent microgravity environment both on the space Shuttle and the Mir Orbiting Station (OS). On the Shuttle, the flames became dim blue after an initial transient where there was significant yellow (presumably soot) in the flame. The flame lifetimes were typically less than 60 seconds. The safety-mandated candlebox that contained the candle flame inhibited oxygen transport to the flame and thus limited the flame lifetime.
   - Explanation: matched terms: behavior, concentration, experiment, flame, oxygen; scientific concepts: flame spread, oxygen concentration; conditions: oxygen; material mismatch penalty; quantitative measurement context missing

**Final BASS-II top five:**
No records returned.

**Final:** local 5, NASA 5, BASS-II 0, combined 10, unique sources 9, duplicates 1, fallback `True` (too_few_local_passages, insufficient_local_source_coverage, required_scientific_concepts_not_covered), latency local/combined/BASS-II `35.05/2394.79/31.93 ms`.

**Assessment:** Results remain provisional. Generic lexical matches without requested material, environment, gravity, or quantitative oxygen context are not treated as directly applicable evidence.
