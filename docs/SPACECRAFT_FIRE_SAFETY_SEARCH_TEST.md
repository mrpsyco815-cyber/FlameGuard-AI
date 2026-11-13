# Real-World Search Test 02: Spacecraft Fire Safety

## Test scope and preservation

This report records a read-only execution of the existing FlameGuard AI search services. No production code, ranking logic, datasets, benchmark fixtures, search configuration, stash, or Git history was modified. No NASA PDFs were downloaded. Relevance assessments are provisional QA assessments, not expert scientific judgments.

Execution date: 2026-10-31. Per-query NASA retrieval timestamps are preserved below.

## Search methods and evidence rules

- **Local:** `build_evidence_brief(query, limit=5)` against the local research intelligence store.
- **Combined:** `search_research_with_fallback(query, limit=5)`, which searches local evidence first and invokes NASA NTRS only when configured local sufficiency checks fail.
- **BASS-II:** `search_bass2_records(query, limit=5)` run separately; no unsupported pressure, temperature, or gravity fields were added.
- NASA results are catalogue metadata and abstracts only: `evidence_type=bibliographic_metadata_and_abstract`, `scientific_findings_verified=false`, and `review_status=not_scientifically_reviewed`.
- A repeated source ID means multiple passages from one source, not multiple independent papers.

## 1. Spacecraft fire safety research

- **Local result count:** 2
- **NASA NTRS result count:** 5; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 7
- **Unique independent local/NASA source count:** 6
- **Duplicate source count:** 1
- **Latency:** local `215.33 ms`; combined/NASA `3559.43 ms`; BASS-II `25.21 ms`
- **Fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.225`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: NUMBER OF PAGES 62 Extinction; Fire safety; Flammability; Flammability limits; Flame propagation; 16.
   - Match explanation: matched terms: fire, safety
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: spacecraft
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

### Actual NASA NTRS fallback results (top five)

1. **Large-Scale Spacecraft Fire Safety Tests** ? NASA ID `20150000894`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20150000894; retrieved `2026-10-31T09:33:35.353151+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: An international collaborative program is underway to address open issues in spacecraft fire safety. Because of limited access to long-term low-gravity conditions and the small volume generally allotted for these experiments, there have been relatively few experiments that directly study spacecraft fire safety under low-gravity conditions. Furthermore, none of these experiments have studied sample sizes and environment conditions typical of those expected in a spacecraft fire. The major constrai
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

2. **Large Scale Experiments on Spacecraft Fire Safety** ? NASA ID `20130001713`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20130001713; retrieved `2026-10-31T09:33:35.353151+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Full scale fire testing complemented by computer modelling has provided significant knowhow about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour i
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

3. **Large Scale Experiments on Spacecraft Fire Safety** ? NASA ID `20130000677`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20130000677; retrieved `2026-10-31T09:33:35.353151+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Full scale fire testing complemented by computer modelling has provided significant know how about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour 
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

4. **Large-Scale Spacecraft Fire Safety Experiments in ISS Resupply Vehicles** ? NASA ID `20140011433`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20140011433; retrieved `2026-10-31T09:33:35.353151+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Our understanding of the fire safety risk in manned spacecraft has been limited by the small scale of the testing we have been able to conduct in low-gravity. Fire growth and spread cannot be expected to scale linearly with sample size so we cannot make accurate predictions of the behavior of realistic scale fires in spacecraft based on the limited low-g testing to date. As a result, spacecraft fire safety protocols are necessarily very conservative and costly. Future crewed missions are expecte
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

5. **Spacecraft Fire Safety Research at NASA Glenn Research Center** ? NASA ID `20170007283`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20170007283; retrieved `2026-10-31T09:33:35.353151+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Appropriate design of fire detection systems requires knowledge of both the expected fire signature and the background aerosol levels. Terrestrial fire detection systems have been developed based on extensive study of terrestrial fires. Unfortunately there is no corresponding data set for spacecraft fires and consequently the fire detectors in current spacecraft were developed based upon terrestrial designs. In low gravity, buoyant flow is negligible which causes particles to concentrate at the 
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

### BASS-II result

No BASS-II records matched this spacecraft fire-safety query. The BASS-II dataset was still searched; no unsupported spacecraft-specific interpretation was made.

### Query-specific relevance assessment

- A local result was considered **Highly relevant** or **Relevant** only provisionally when its title/excerpt and match explanations explicitly referenced spacecraft/spaceflight/fire safety or a directly related condition.
- Generic combustion, flame-spread, or material-flammability passages without spacecraft cabin, atmosphere, detection, suppression, or fire-hazard context were treated as **Partially relevant** or **Insufficient information**, even when lexical scores were nonzero.
- NASA records remain catalogue evidence only; no metadata or abstract was treated as a verified scientific finding.
- Source repetition was reported separately from independent source count.

## 2. Fire hazards aboard spacecraft

- **Local result count:** 2
- **NASA NTRS result count:** 5; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 7
- **Unique independent local/NASA source count:** 6
- **Duplicate source count:** 1
- **Latency:** local `34.19 ms`; combined/NASA `2899.92 ms`; BASS-II `22.59 ms`
- **Fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: spacecraft
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: NUMBER OF PAGES 62 Extinction; Fire safety; Flammability; Flammability limits; Flame propagation; 16.
   - Match explanation: matched terms: fire
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

### Actual NASA NTRS fallback results (top five)

1. **Fire safety design considerations for advanced space vehicles** ? NASA ID `19930074562`; score `0.45`; URL: https://ntrs.nasa.gov/citations/19930074562; retrieved `2026-10-31T09:33:38.975833+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: The desire to understand and explore space has driven man to overcome the confines of the Earth's atmosphere and accept the challenge of spaceflight. With our increasing ability to travel, work, and explore in space comes a need for a better understanding of the hazards in this relatively new endeavor. One of the most important and immediate needs is to be able to predict the ignition, spread, and growth of fire on board spacecraft. Fire safety aboard spacecraft has always been a concern; howeve
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

2. **Space station internal environmental and safety concerns** ? NASA ID `19880003145`; score `0.45`; URL: https://ntrs.nasa.gov/citations/19880003145; retrieved `2026-10-31T09:33:38.975833+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Space station environmental and safety concerns, especially those involving fires, are discussed. Several types of space station modules and the particular hazards associated with each are briefly surveyed. A brief history of fire detection and suppression aboard spacecraft is given. Microgravity fire behavior, spacecraft fire detector systems, space station fire suppression equipment and procedures, and fire safety in hyperbaric chambers are discussed.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

3. **No Moving Parts** ? NASA ID `20020064975`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20020064975; retrieved `2026-10-31T09:33:38.975833+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Under a NASA SBIR (Small Business Innovative Research), Research International developed the solid state micromachined pump used for cooling electronics in space, circulation of heat transfer fluids on spacecraft, and monitoring fire and gas hazards aboard naval warships. Incorporating Lewis Research Center's pumping technology, commercial applications for this product include both detection of toxins and pollutants in coal mines, and early warning smoke detectors for industrial applications.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

4. **Portable 4.6 Micrometers Laser Absorption Spectrometer for Carbon Monoxide Monitoring and Fire Detection** ? NASA ID `20150008051`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20150008051; retrieved `2026-10-31T09:33:38.975833+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: The air quality aboard manned spacecraft must be continuously monitored to ensure crew safety and identify equipment malfunctions. In particular, accurate real-time monitoring of carbon monoxide (CO) levels helps to prevent chronic exposure and can also provide early detection of combustion-related hazards. For long-duration missions, environmental monitoring grows in importance, but the mass and volume of monitoring instruments must be minimized. Furthermore, environmental analysis beyond low-E
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

5. **Gravitational Influences on Flame Propagation Through Non-Uniform Premixed Gas Systems** ? NASA ID `19970020602`; score `0.45`; URL: https://ntrs.nasa.gov/citations/19970020602; retrieved `2026-10-31T09:33:38.975833+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Flame spread through uniformly premixed gas systems, while not completely understood, is nevertheless a well-studied problem in combustion science. In contrast, flame propagation through non-uniform premixed gas systems (also called "'layered systems") has been the subject of relatively few previous studies. In a recent theoretical paper Talley lists sprays, flame spread over liquids, and the leading edge of lifted turbulent diffusion flames as applications where flame behavior in layers is impo
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

### BASS-II result

No BASS-II records matched this spacecraft fire-safety query. The BASS-II dataset was still searched; no unsupported spacecraft-specific interpretation was made.

### Query-specific relevance assessment

- A local result was considered **Highly relevant** or **Relevant** only provisionally when its title/excerpt and match explanations explicitly referenced spacecraft/spaceflight/fire safety or a directly related condition.
- Generic combustion, flame-spread, or material-flammability passages without spacecraft cabin, atmosphere, detection, suppression, or fire-hazard context were treated as **Partially relevant** or **Insufficient information**, even when lexical scores were nonzero.
- NASA records remain catalogue evidence only; no metadata or abstract was treated as a verified scientific finding.
- Source repetition was reported separately from independent source count.

## 3. Fire detection and suppression in spacecraft

- **Local result count:** 2
- **NASA NTRS result count:** 5; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 7
- **Unique independent local/NASA source count:** 6
- **Duplicate source count:** 1
- **Latency:** local `32.67 ms`; combined/NASA `2623.91 ms`; BASS-II `18.04 ms`
- **Fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: spacecraft
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: NUMBER OF PAGES 62 Extinction; Fire safety; Flammability; Flammability limits; Flame propagation; 16.
   - Match explanation: matched terms: fire
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

### Actual NASA NTRS fallback results (top five)

1. **Progress in Fire Detection and Suppression Technology for Future Space Missions** ? NASA ID `20000120278`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20000120278; retrieved `2026-10-31T09:33:41.937559+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Fire intervention technology (detection and suppression) is a critical part of the strategy of spacecraft fire safety. This paper reviews the status, trends, and issues in fire intervention, particularly the technology applied to the protection of the International Space Station and future missions beyond Earth orbit. An important contribution to improvements in spacecraft fire safety is the understanding of the behavior of fires in the non-convective (microgravity) environment of Earth-orbiting
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

2. **Fire safety applications for spacecraft** ? NASA ID `19890015042`; score `0.45`; URL: https://ntrs.nasa.gov/citations/19890015042; retrieved `2026-10-31T09:33:41.937559+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Fire safety for spacecraft is reviewed by first describing current practices, many of which are adapted directly from aircraft. Then, current analyses and experimental knowledge in low-gravity combustion, with implications for fire safety are discussed. In orbiting spacecraft, the detection and suppression of flames are strongly affected by the large reduction in buoyant flows under low gravity. Generally, combustion intensity is reduced in low gravity. There are some notable exceptions, however
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

3. **Large-Scale Spacecraft Fire Safety Tests** ? NASA ID `20150000894`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20150000894; retrieved `2026-10-31T09:33:41.937559+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: An international collaborative program is underway to address open issues in spacecraft fire safety. Because of limited access to long-term low-gravity conditions and the small volume generally allotted for these experiments, there have been relatively few experiments that directly study spacecraft fire safety under low-gravity conditions. Furthermore, none of these experiments have studied sample sizes and environment conditions typical of those expected in a spacecraft fire. The major constrai
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

4. **Spacecraft Fire Safety: A Human Space Flight Program Perspective** ? NASA ID `20030053427`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20030053427; retrieved `2026-10-31T09:33:41.937559+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: This paper presents viewgraphs on the International Space Station's fire safety program from a human space flight perspective. The topics include: 1) Typical Manned Spacecraft Materials; 2) Typical Flammable Hardware Protection; 3) Materials Flammability; 4) Fire Retardants; 5) Nonflammable Foam Cushion Material; 6) Electrical Wire and Cable; 7) Russian Solid-Fuel Oxygen Generator (SFOG); 8) GOX Ignition Mechanisms; 9) Fire Detection; and 10) Fire Suppression.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

5. **Technology Development for Fire Safety in Exploration Spacecraft and Habitats** ? NASA ID `20070010766`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20070010766; retrieved `2026-10-31T09:33:41.937559+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Fire during an exploration mission far from Earth is a particularly critical risk for exploration vehicles and habitats. The Fire Prevention, Detection, and Suppression (FPDS) project is part of the Exploration Technology Development Program (ETDP) and has the goal to enhance crew health and safety on exploration missions by reducing the likelihood of a fire, or, if one does occur, minimizing the risk to the mission, crew, or system. Within the past year, the FPDS project has been formalized wit
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

### BASS-II result

No BASS-II records matched this spacecraft fire-safety query. The BASS-II dataset was still searched; no unsupported spacecraft-specific interpretation was made.

### Query-specific relevance assessment

- A local result was considered **Highly relevant** or **Relevant** only provisionally when its title/excerpt and match explanations explicitly referenced spacecraft/spaceflight/fire safety or a directly related condition.
- Generic combustion, flame-spread, or material-flammability passages without spacecraft cabin, atmosphere, detection, suppression, or fire-hazard context were treated as **Partially relevant** or **Insufficient information**, even when lexical scores were nonzero.
- NASA records remain catalogue evidence only; no metadata or abstract was treated as a verified scientific finding.
- Source repetition was reported separately from independent source count.

## 4. Material flammability in spacecraft cabin environments

- **Local result count:** 5
- **NASA NTRS result count:** 2; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 7
- **Unique independent local/NASA source count:** 5
- **Duplicate source count:** 2
- **Latency:** local `29.57 ms`; combined/NASA `1689.5 ms`; BASS-II `17.57 ms`
- **Fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.27`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: environment, material, spacecraft
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

2. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.09`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: N96- 15553 Solid Surface Combustion Experiment Flame Spread in a Quiescent, Microgravity Environment Implications of Spread Rate and Flame Structure Matthew Bundy, Jeff West, Peter C.
   - Match explanation: matched terms: environment
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.09`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `simulation`; review `requires_manual_review`.
   - Passage: From the results, it is seen that the simulations performed using finite rate chemistry underpredict the experimental spread rates at the higher pressures, while not even allowing flame spread at the lower pressure environments.
   - Match explanation: matched terms: environment
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

4. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.18`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: 1.3.2 Procedure and Results of Narrow Channel Testing.--The Narrow Channel test in the apparatus on fig- ure 1.7 evaluates material flammability in terms of V,,,,, determined at a prescribed oxygen concentration C (greater than C,,m).
   - Match explanation: matched terms: flammability, material
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.18`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: TABLE 1.2.--GROUND-TESTING RESULTS OF U.S.-PROVIDED MATERIAL FLAMMABILITY -- LIMITING VELOCITY [Vb,,,' ) DETERMINED IN APPARATUSES WITH SUPPRESSED CONVECTION Number Material Vi.., cm/sec Narrow channel Vertical combustion chamber C =21% C =23% Q=21% Low-density Polyethylene 16.9 6.8 HiLzh-density Polyethylene 8.3 3.6 4.5 3 PMMA 3.3 2.3 1.1 4 Delrin 0.5 0.3 1.1 Nylon 6/6 16.4 5.3 R iLzid Polyurethane 15.5 4.7 Glass-epoxy composite >25 >25 TABLE 1.3.--GROUND-TESTING RESULTS OF U.S.-PROVIDED MATERI
   - Match explanation: matched terms: flammability, material
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

### Actual NASA NTRS fallback results (top five)

1. **Fire-Resistant Textile Development for Exploration Vehicles With Enriched-Oxygen Cabin Environments** ? NASA ID `20260003042`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20260003042; retrieved `2026-10-31T09:33:44.597894+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Material selection is a key part of the National Aeronautics and Space Administration (NASA) spacecraft fire safety management plan. Non-flammable textiles are necessary to ensure large-scale flame propagation events do not occur inside a spacecraft. An increased use of textiles and other softgood material is crucial to the pursuit of exploration spaceflight to reduce mass and volume. Exploration spaceflight missions benefit from enriched oxygen cabin environments (>21% O2) by allowing a reduced
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

2. **Operational Considerations for Oxygen Flammability Risks: Concentrated Oxygen Diffusion and Permeation Behaviors** ? NASA ID `20100019472`; score `0.45`; URL: https://ntrs.nasa.gov/citations/20100019472; retrieved `2026-10-31T09:33:44.597894+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Increased human spaceflight operations utilize oxygen concentrations that are frequently varied with use of concentrations up to 100 percent oxygen. Even after exiting a higher percentage oxygen environment, high oxygen concentrations can still be maintained due to material saturation and oxygen entrapment between barrier materials. This paper examines the material flammability concerns that arise from changing oxygen environments during spaceflight operations. We examine the time required for c
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

### BASS-II result

No BASS-II records matched this spacecraft fire-safety query. The BASS-II dataset was still searched; no unsupported spacecraft-specific interpretation was made.

### Query-specific relevance assessment

- A local result was considered **Highly relevant** or **Relevant** only provisionally when its title/excerpt and match explanations explicitly referenced spacecraft/spaceflight/fire safety or a directly related condition.
- Generic combustion, flame-spread, or material-flammability passages without spacecraft cabin, atmosphere, detection, suppression, or fire-hazard context were treated as **Partially relevant** or **Insufficient information**, even when lexical scores were nonzero.
- NASA records remain catalogue evidence only; no metadata or abstract was treated as a verified scientific finding.
- Source repetition was reported separately from independent source count.

## 5. NASA spacecraft fire safety experiments

- **Local result count:** 5
- **NASA NTRS result count:** 5; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 10
- **Unique independent local/NASA source count:** 9
- **Duplicate source count:** 1
- **Latency:** local `19.36 ms`; combined/NASA `4516.75 ms`; BASS-II `20.68 ms`
- **Fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.58`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Preliminary results of polyethylene-insulation flammability in microgravity were obtained in the NASA Wire Insulation Flammability (WIF) experiment during the Space Shuttle flight STS-50 (refs.
   - Match explanation: matched terms: experiment, nasa; scientific concepts: polyethylene; material: polyethylene
   - Provisional QA category: **Relevant**. Context-specific spacecraft relevance must be verified from the source.

2. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.0225`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: N96- 15553 Solid Surface Combustion Experiment Flame Spread in a Quiescent, Microgravity Environment Implications of Spread Rate and Flame Structure Matthew Bundy, Jeff West, Peter C.
   - Match explanation: matched terms: experiment; material mismatch penalty
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.0225`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `simulation`; review `requires_manual_review`.
   - Passage: It is seen that, in spite of the simplifications included in the model, the simulations are able to qualitatively reproduce the overall behavior observed during the experiments: at lower ambient pressures the time evolution of the pyrolysis front and burnout front positions over the sample length is slower, i.e.
   - Match explanation: matched terms: experiment; material mismatch penalty
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

4. **Determining Flame Temperature By Broadband Two Color Pyrometry in A Flame Spreading Over A Thin Solid in Microgravity** ? source/NASA ID `20220012861`; score `0.0225`; URL: https://ntrs.nasa.gov/citations/20220012861; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Considering that the initial purpose of the computed from a Monte Carlo propagation analysis, images recorded during the experiments was to use considering a conservative error of 5% on the signal the data to visualize the flame and track its evolu- ratio ΘG/R, resulting in 117 K of uncertainty for tem- tion over time, i.e., pyrolysis length, flame size, etc., perature determination.
   - Match explanation: matched terms: experiment; material mismatch penalty
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.045`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: experiment, spacecraft; material mismatch penalty
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

### Actual NASA NTRS fallback results (top five)

1. **Large-Scale Spacecraft Fire Safety Tests** ? NASA ID `20150000894`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/20150000894; retrieved `2026-10-31T09:33:46.311587+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: An international collaborative program is underway to address open issues in spacecraft fire safety. Because of limited access to long-term low-gravity conditions and the small volume generally allotted for these experiments, there have been relatively few experiments that directly study spacecraft fire safety under low-gravity conditions. Furthermore, none of these experiments have studied sample sizes and environment conditions typical of those expected in a spacecraft fire. The major constrai
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

2. **Development of Large-Scale Spacecraft Fire Safety Experiments** ? NASA ID `20140006578`; score `0.1125`; URL: https://ntrs.nasa.gov/citations/20140006578; retrieved `2026-10-31T09:33:46.311587+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: The status is presented of a spacecraft fire safety research project that is under development to reduce the uncertainty and risk in the design of spacecraft fire safety systems by testing at nearly full scale in low-gravity. Future crewed missions are expected to be more complex and longer in duration than previous exploration missions outside of low-earth orbit. This will increase the challenge of ensuring a fire-safe environment for the crew throughout the mission. Based on our fundamental un
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

3. **Risk-based Spacecraft Fire Safety Experiments** ? NASA ID `19930019549`; score `0.09`; URL: https://ntrs.nasa.gov/citations/19930019549; retrieved `2026-10-31T09:33:46.311587+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Viewgraphs on risk-based spacecraft fire safety experiments are presented. Spacecraft fire risk can never be reduced to a zero probability. Probabilistic risk assessment is a tool to reduce risk to an acceptable level.
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

4. **Large Scale Experiments on Spacecraft Fire Safety** ? NASA ID `20130000677`; score `0.09`; URL: https://ntrs.nasa.gov/citations/20130000677; retrieved `2026-10-31T09:33:46.311587+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Full scale fire testing complemented by computer modelling has provided significant know how about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour 
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

5. **Large Scale Experiments on Spacecraft Fire Safety** ? NASA ID `20130001713`; score `0.09`; URL: https://ntrs.nasa.gov/citations/20130001713; retrieved `2026-10-31T09:33:46.311587+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: Full scale fire testing complemented by computer modelling has provided significant knowhow about the risk, prevention and suppression of fire in terrestrial systems (cars, ships, planes, buildings, mines, and tunnels). In comparison, no such testing has been carried out for manned spacecraft due to the complexity, cost and risk associated with operating a long duration fire safety experiment of a relevant size in microgravity. Therefore, there is currently a gap in knowledge of fire behaviour i
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

### BASS-II result

No BASS-II records matched this spacecraft fire-safety query. The BASS-II dataset was still searched; no unsupported spacecraft-specific interpretation was made.

### Query-specific relevance assessment

- A local result was considered **Highly relevant** or **Relevant** only provisionally when its title/excerpt and match explanations explicitly referenced spacecraft/spaceflight/fire safety or a directly related condition.
- Generic combustion, flame-spread, or material-flammability passages without spacecraft cabin, atmosphere, detection, suppression, or fire-hazard context were treated as **Partially relevant** or **Insufficient information**, even when lexical scores were nonzero.
- NASA records remain catalogue evidence only; no metadata or abstract was treated as a verified scientific finding.
- Source repetition was reported separately from independent source count.

## 6. Fire behavior in enclosed spacecraft environments

- **Local result count:** 5
- **NASA NTRS result count:** 2; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 7
- **Unique independent local/NASA source count:** 5
- **Duplicate source count:** 2
- **Latency:** local `30.26 ms`; combined/NASA `2328.76 ms`; BASS-II `22.3 ms`
- **Fallback:** triggered; reason: too_few_local_passages, insufficient_local_source_coverage

### Actual local results (top five)

1. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.18`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Measurements of V,m and Vvare possible in the microgravity environment of spacecraft, however, if the material is flammable in the given oxygen concentration in the spacecraft compartment at the time of the space experiment and if the flow velocity in the apparatus chamber is higher than a limiting velocity for the material.
   - Match explanation: matched terms: environment, spacecraft
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

2. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.09`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: N96- 15553 Solid Surface Combustion Experiment Flame Spread in a Quiescent, Microgravity Environment Implications of Spread Rate and Flame Structure Matthew Bundy, Jeff West, Peter C.
   - Match explanation: matched terms: environment
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

3. **Determining the Cause of Reduced Concurrent Flame Spread over Thin Solid Fuels in Low Pressure and Low Gravity** ? source/NASA ID `20210017787`; score `0.09`; URL: https://ntrs.nasa.gov/citations/20210017787; evidence type `simulation`; review `requires_manual_review`.
   - Passage: It is seen that, in spite of the simplifications included in the model, the simulations are able to qualitatively reproduce the overall behavior observed during the experiments: at lower ambient pressures the time evolution of the pyrolysis front and burnout front positions over the sample length is slower, i.e.
   - Match explanation: matched terms: behavior
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

4. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.09`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: Thin Fuel: 1.1 Spread Rate: The experimental flame spread rates, Vf.,_,, over the thin cellulosic fuel in five different quiescent environments, at three different ambient pressures and two oxygen levels, are plotted in Fig.
   - Match explanation: matched terms: environment
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.09`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: NUMBER OF PAGES 62 Extinction; Fire safety; Flammability; Flammability limits; Flame propagation; 16.
   - Match explanation: matched terms: fire
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

### Actual NASA NTRS fallback results (top five)

1. **Seventh International Workshop on Microgravity Combustion and Chemically Reacting Systems** ? NASA ID `20040053504`; score `0.18`; URL: https://ntrs.nasa.gov/citations/20040053504; retrieved `2026-10-31T09:33:50.908679+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: The Seventh International Workshop on Microgravity Combustion and Chemically Reacting Systems was planned for June 3-6, 2003, in Cleveland, Ohio, near the NASA John H. Glenn Research Center at Lewis Field. The new name for the workshop is based on the decision to broaden our scope to encompass support for future space exploration through basic and applied research in reacting systems that in some cases may not look like combustion. The workshop has been lengthened to 4 days with focus sessions o
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

2. **Sixth International Microgravity Combustion Workshop** ? NASA ID `20010073993`; score `0.18`; URL: https://ntrs.nasa.gov/citations/20010073993; retrieved `2026-10-31T09:33:50.908679+00:00`; evidence type `bibliographic_metadata_and_abstract`; verified `False`; review `not_scientifically_reviewed`.
   - Abstract: This conference proceedings document is a compilation of papers presented orally or as poster displays to the Sixth International Microgravity Combustion Workshop held in Cleveland, Ohio on May 22-24, 2001. The purpose of the workshop is to present and exchange research results from theoretical and experimental work in combustion science using the reduced-gravity environment as a research tool. The results are contributed by researchers funded by NASA throughout the United States at universities
   - Provisional QA category: **Relevant or partially relevant catalogue evidence only**; an abstract/metadata record does not prove a fire-safety finding or experiment result.

### BASS-II result

No BASS-II records matched this spacecraft fire-safety query. The BASS-II dataset was still searched; no unsupported spacecraft-specific interpretation was made.

### Query-specific relevance assessment

- A local result was considered **Highly relevant** or **Relevant** only provisionally when its title/excerpt and match explanations explicitly referenced spacecraft/spaceflight/fire safety or a directly related condition.
- Generic combustion, flame-spread, or material-flammability passages without spacecraft cabin, atmosphere, detection, suppression, or fire-hazard context were treated as **Partially relevant** or **Insufficient information**, even when lexical scores were nonzero.
- NASA records remain catalogue evidence only; no metadata or abstract was treated as a verified scientific finding.
- Source repetition was reported separately from independent source count.

## 7. Spacecraft cabin atmosphere and combustion hazards

- **Local result count:** 5
- **NASA NTRS result count:** 0; error: `none`
- **BASS-II result count:** 0
- **Final combined local/NASA record count:** 5
- **Unique independent local/NASA source count:** 2
- **Duplicate source count:** 3
- **Latency:** local `28.22 ms`; combined/NASA `39.79 ms`; BASS-II `29.06 ms`
- **Fallback:** not triggered; reason: local evidence met configured sufficiency thresholds

### Actual local results (top five)

1. **Solid surface combustion experiment flame spread in a quiescent, microgravity environment implications of spread rate and flame structure** ? source/NASA ID `19960008387`; score `0.34`; URL: https://ntrs.nasa.gov/citations/19960008387; evidence type `experiment`; review `requires_manual_review`.
   - Passage: N96- 15553 Solid Surface Combustion Experiment Flame Spread in a Quiescent, Microgravity Environment Implications of Spread Rate and Flame Structure Matthew Bundy, Jeff West, Peter C.
   - Match explanation: matched terms: combustion; scientific concepts: solid fuel combustion
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

2. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.34`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: When velocity is 1.1 cm/s, both combustion and extinction are observed.
   - Match explanation: matched terms: combustion; scientific concepts: solid fuel combustion
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

3. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.34`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: These measurements were obtained during the initial phase of combustion (the first 15 to 20 sec alter ignition), when the samples still keep their original shape.
   - Match explanation: matched terms: combustion; scientific concepts: solid fuel combustion
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

4. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.34`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: 3.4 Non-Steadiness and Other Characteristics of Combustion in Microgravity The nonsteadiness of polymer combustion observed in the space experiment might be explained by two reasons: (1) the formation of the melt drop, which is almost spherical tbr Delrin and PMMA (see figs.
   - Match explanation: matched terms: combustion; scientific concepts: solid fuel combustion
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

5. **Experimental Verification of Material Flammability in Space** ? source/NASA ID `20000024924`; score `0.34`; URL: https://ntrs.nasa.gov/citations/20000024924; evidence type `experiment`; review `requires_manual_review`.
   - Passage: By the end of the experiment, the diameter of the melt ball is 2 to 2.5 times greater than the initial diameter of the cylindrical sample, and the shape of the sample changes drastically during combustion.
   - Match explanation: matched terms: combustion; scientific concepts: solid fuel combustion
   - Provisional QA category: **Partially relevant**. Context-specific spacecraft relevance must be verified from the source.

### Actual NASA NTRS fallback results (top five)

No NASA NTRS records were returned or fallback was not requested.

### BASS-II result

No BASS-II records matched this spacecraft fire-safety query. The BASS-II dataset was still searched; no unsupported spacecraft-specific interpretation was made.

### Query-specific relevance assessment

- A local result was considered **Highly relevant** or **Relevant** only provisionally when its title/excerpt and match explanations explicitly referenced spacecraft/spaceflight/fire safety or a directly related condition.
- Generic combustion, flame-spread, or material-flammability passages without spacecraft cabin, atmosphere, detection, suppression, or fire-hazard context were treated as **Partially relevant** or **Insufficient information**, even when lexical scores were nonzero.
- NASA records remain catalogue evidence only; no metadata or abstract was treated as a verified scientific finding.
- Source repetition was reported separately from independent source count.

## Overall assessment

**PARTIAL PASS: Some queries work, but important relevance and retrieval limitations remain.** Local-first retrieval, fallback behavior, provenance, source IDs, and timestamps were observable. NASA returned live catalogue metadata for six fallback searches. However, the system is still vulnerable to generic lexical matches, repeated passages from the same source, and metadata/abstract evidence being insufficient to establish spacecraft-specific fire-safety relevance. BASS-II produced no matching records for these queries.

## Limitations and unverified items

- Not expert-validated: no qualified scientific reviewer judged these query-result pairs.
- Not full-text validated: no NASA PDFs were downloaded.
- Not a safety assessment: no engineering recommendation or certified fire-safety conclusion was made.
- Scientific precision/recall and ground-truth relevance metrics were not calculated.
- NASA API results are metadata/abstract scope only.
- BASS-II lacks spacecraft-specific fields sufficient to establish cabin fire-safety applicability.

## Preservation verification

The test created only this report. Existing user changes, the existing stash, original datasets, benchmark fixtures, and Git history were preserved. Final `git status`, data-directory diff, stash listing, and `git diff --check` were run after report generation.
