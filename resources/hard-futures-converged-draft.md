# Hard Futures

**An open-source graph of Europe's most critical deep tech companies.**

Branded by Inflection. Open to everyone.

---

## What It Is

Hard Futures maps 200-300 European companies solving problems that were previously only possible for nation-states or Tier 1 defense primes. Each company is tagged to one or more of 28 capabilities across 7 domains. The graph shows relationships between companies: shared investors, co-participation in government programs, supply chain links, and competitive positioning.

**Litmus test for inclusion:** "Was this previously only possible for a nation-state or a Tier 1 defense prime?"

**Four inclusion rules:**
1. European HQ (EU27, UK, Switzerland, Norway)
2. Founded in the last 10 years
3. Solving at least one Hard Futures capability
4. Raised institutional capital (VC, government grant >500K, or defense contract)

---

## Data Sources

Hard Futures sources company data from public, structured programs. No commercial API subscriptions required for v1.

### Tier 1 - Structured Databases (High Quality)

| Source | Coverage | Access |
|---|---|---|
| **EIC Data Hub** | 1,000+ EIC Accelerator companies, searchable by sector/country | Free, public |
| **CORDIS** | 10,000+ Horizon Europe participants, downloadable open data | Free, public API |
| **NATO DIANA** | 200-300 companies across 10 defense challenge areas | Annual cohort announcements |
| **ESA BIC Network** | 1,950+ space startups across 33 hubs in 22 countries | Regional BIC websites |

### Tier 2 - Government Programs (Manual Compilation)

| Source | Coverage | Notes |
|---|---|---|
| **SPRIND** | 163 funded projects, 21 large-scale | Press releases, annual reports |
| **IPCEI** | 283 companies across 10 programs (chips, batteries, hydrogen, cloud) | EC press releases |
| **European Defence Fund** | 500+ companies, 33 call topics per year | EC Funding & Tenders Portal |
| **Quantum Flagship** | 100-200 companies across communication, computation, sensing | qt.eu project consortia |
| **ARIA (UK)** | 50-100 funded companies | aria.org.uk |
| **BPI France Deeptech** | 1,000+ companies | bpifrance.com |
| **Innovate UK / DASA** | 500+ defense/security companies | iuk-business-connect.org.uk |

### Tier 3 - Competition Winners & Awards

| Source | Coverage | Notes |
|---|---|---|
| **Hello Tomorrow** | 500+ finalists cumulative (80/year) | Annual deep tech competition |
| **EIT KIC Portfolios** | 3,100+ startups across 9 KICs | InnoEnergy, RawMaterials, Manufacturing most relevant |
| **ESA Launcher Challenge** | 5 finalists, EUR 169M contracts | July 2024 selection |
| **Deep Tech Momentum** | 100-200 participants/year | Europe's leading deep tech event |

### Tier 4 - Ecosystem Intelligence

| Source | Type | Notes |
|---|---|---|
| **Atomico State of European Tech** | Annual report (free) | 41 countries, benchmarking data |
| **Sifted / Tech.eu** | Journalism | Company discovery, validation |
| **ASPI Critical Technology Tracker** | 74 technologies, institution-level | Methodology inspiration |
| **Defense VC portfolios** | OTB, Vsquared, Keen, MD One, Expeditions | Public portfolio pages |

### Tier 5 - Self-Submission (Phase 2)

Community-driven model: founders submit companies, validated against government program participation and funding records. Verified badges for companies with EIC/SPRIND/NATO DIANA/ESA BIC participation.

---

## Capabilities

28 capabilities across 7 domains. Each capability represents a technology area where startups are achieving what previously required nation-state resources.

---

### I. COMPUTE (4 capabilities)

#### 1. Sovereign Processors

**Definition:** Novel chip architectures - RISC-V, neuromorphic, edge AI accelerators - designed and manufactured with European IP. Includes advanced packaging and back-end semiconductor capabilities.

**Subcategories:**
- RISC-V & open-architecture processors
- Neuromorphic computing (spiking neural networks)
- Edge AI accelerators (NPUs, vision processors)
- Advanced chip packaging

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| SiPearl | France | Europe's first out-of-order RISC-V processor (eProcessor), Intel 3 node | European Processor Initiative, EUR 270M EU investment |
| Axelera AI | Netherlands | Edge AI accelerators for machine vision, RISC-V based | EUR 68M EU grant for AI chiplets |
| Innatera | Netherlands | Spiking Neural Processor T1, 500x energy savings vs CPU | NATO DIANA 2025 |
| Semidynamics | Spain | RISC-V multicore with tensor units, eliminates separate NPU/GPU | - |
| Openchip | Spain | RISC-V SoC and accelerators for AI/HPC | - |
| SynSense | Switzerland | Neuromorphic vision sensors and processors | - |

---

#### 2. Cryptographic Hardware

**Definition:** Post-quantum cryptography chips, quantum random number generators, and trusted execution environments for hardware-level security.

**Subcategories:**
- Post-quantum cryptography (lattice-based, hash-based)
- Quantum random number generators
- Hardware security modules (HSMs)
- Trusted execution environments

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| PQShield | UK | Post-quantum crypto for embedded devices, Oxford spinout | $37M Series B (2024), first NRC-approved |
| ID Quantique | Switzerland | Quantum-safe crypto, RNG, industry leader since 2001 | Geneva University spinout |
| Crypto Quantique | UK | End-to-end IoT security, quantum-random number generators | - |
| Quantum Blockchains | Poland | Quantum-safe cryptography for blockchain | Founded 2018 |

---

#### 3. Quantum Computing

**Definition:** Building quantum processors across all modalities - superconducting, neutral atom, trapped ion, photonic - for computation beyond classical limits.

**Subcategories:**
- Superconducting qubits
- Neutral atom processors
- Trapped ion systems
- Photonic quantum computers

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| IQM | Finland | Europe's leading superconducting quantum hardware, 20-qubit at LRZ Munich | First EU supercomputer integration |
| PASQAL | France | 100+ qubit neutral atom "Orion" deployed at CEA-GENCI and Julich | $140M raised (Temasek, Aramco, EIC) |
| Quandela | France | Photonic quantum computers | Paris-Saclay |
| Alpine Quantum Technologies | Austria | Trapped ion systems, Innsbruck spinout | - |
| ORCA Computing | UK | Photonic quantum integrated with telecom infrastructure | - |
| Planqc | Germany | Neutral atom quantum computing | Munich-based |
| Universal Quantum | UK | Trapped ion quantum computing | Brighton-based |
| Oxford Quantum Circuits | UK | Superconducting quantum, commercial cloud access | - |

---

#### 4. Photonic Computing

**Definition:** Optical computing using photons instead of electrons for data processing and transmission. Requires advanced chip fabrication at 300mm wafer scale and competes with China's $10B+ national programs.

**Subcategories:**
- Silicon photonics for AI/HPC interconnects
- Photonic neural processing units
- Graphene-based photonic circuits
- Optical switching and routing

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Q.ANT | Germany | Photonic NPU processors, TFLN technology | Shipping 2026 |
| Black Semiconductor | Germany | 300mm graphene photonics pilot line | IPCEI grant |
| Astrape Networks | Netherlands | AI data center photonics | EUR 7.9M including EUR 2.5M EIC grant |
| Alcyon | Spain | Silicon photonics PICs | - |

**Ecosystem:** PhotonDelta tracks 591 European photonics startups (323 funded, 187 Series A+).

---

### II. DEFENSE (6 capabilities)

#### 5. Autonomous Air Defense

**Definition:** Counter-UAS systems, integrated air defense networks, and AESA radar for detection and interception of drones, missiles, and hypersonic threats.

**Subcategories:**
- Counter-UAS (detection, tracking, interception)
- Integrated air/missile defense systems
- AESA radar and phased arrays
- Short-range air defense (SHORAD)

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Alpine Eagle | Austria/Germany | AI-powered autonomous air-to-air counter-UAS "Sentinel" | NATO exercises |
| Origin Robotics | Latvia | Interceptor drones for integrated air defense | - |
| Crown Cyber Defence | TBD | QME electromagnetic weapons, AI-integrated C-UAS | - |

**Note:** EU Commission committed billions for counter-drone infrastructure by 2028. CROWN project (Indra/Thales/Hensoldt/SAAB) developing combined AESA radar/comms/EW across 7 EU countries.

---

#### 6. Military AI & Autonomy

**Definition:** AI systems for command and control, autonomous weapons integration, multi-domain mission planning, and combat decision support.

**Subcategories:**
- Combat AI and autonomous weapons systems
- Multi-domain command and control
- Autonomous target recognition
- Mission planning and logistics AI

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Helsing | Germany | AI-powered "Europa" combat drone, autonomous autopilot for jets | EUR 12B valuation, EUR 1.37B raised, largest European defense startup |
| Harmattan AI | France | Autonomy software for military aircraft/drones | $242M funding, $1.4B valuation (unicorn 2024) |
| Avalor AI | TBD | Multi-domain distributed mission autonomy "Nexus" platform | UxV coordination across air/land/sea |

---

#### 7. Autonomous Unmanned Systems

**Definition:** Drones (air, ground, sea, underwater) with autonomous navigation, mission execution, and coordination capabilities for defense and dual-use applications.

**Subcategories:**
- Fixed-wing and VTOL military UAVs
- Unmanned ground vehicles (UGV)
- Unmanned surface/underwater vehicles
- Autonomous conversion kits for existing platforms

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| ARX Robotics | Germany | "Gereon" mini-tanks, autonomous conversion kits | EUR 10.15M raised, Helsing partnership (Sept 2025) |
| Milrem Robotics | Estonia | THeMIS UGV platform for defense/security | - |
| UDS | Lithuania | "Partisan" recon drones, loitering munitions | Supplied Lithuanian and Ukrainian Armed Forces |
| Sky-Watch | Denmark | RQ-35 Heidrun autonomous fixed-wing mini-UAV | Production since 2009 |
| DeltaQuad | Netherlands | Electric long-range VTOL drones | Defense, oil/gas, mining |
| Delair | France | Primary drone supplier to French Armed Forces | Founded 2011 |
| Exail | France | Autonomous underwater vehicles | Deployed by French, Belgian, Netherlands navies |

---

#### 8. Swarm Robotics

**Definition:** Coordinated autonomous swarms of air/land/sea vehicles with distributed intelligence, emergent collective behavior, and cross-domain synchronization.

**Subcategories:**
- Multi-drone swarm coordination
- Mixed multi-domain swarms (air + ground + sea)
- Distributed decision-making algorithms
- Voice/AI-controlled swarm command

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| SeeByte | UK | Mixed Multi-Domain Swarms architecture | Dstl contract with Blue Bear |
| Blue Bear | UK | Multi-domain swarm software | Dstl Mixed Multi-Domain Swarms contract |

**Programs:** France deploying military drone swarms by 2027. Netherlands Project Steadfast (EUR 2.7M) testing swarm software. MBDA Swarm Drone Challenge 2026. NATO identifies swarm tech as critical capability gap.

---

#### 9. Secure Communications

**Definition:** Communications systems for contested electromagnetic environments - mesh networking, anti-jamming, quantum key distribution, and EW-resilient links.

**Subcategories:**
- Mesh networking for contested environments
- Anti-jam and frequency-hopping systems
- Quantum key distribution (QKD)
- Tactical edge communications

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Hedy | Europe (stealth) | Contested-environment communications for defense | Portfolio company |

**Note:** European mesh networking for defense is dominated by US tech (Silvus, Rajant) and established players (Nokia, Thales). Startup layer is thin. NATO DIANA EW-resilient comms challenge attracted 150+ proposals (2026), indicating emerging landscape.

---

#### 10. Cognitive Electronic Warfare

**Definition:** AI-powered adaptive EW systems with real-time spectrum management, autonomous countermeasures, and predictive threat analysis. The upgrade from traditional EW (reactive) to cognitive EW (predictive/adaptive).

**Subcategories:**
- AI-driven spectrum sensing and classification
- Autonomous jamming and countermeasures
- Cognitive radar and signal intelligence
- Real-time massive data processing for EW

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| XRF.ai | TBD | High-frequency RF analysis, EW detection for NATO | EUR 2.57M (2024) |
| Wild Hornets | TBD | Communication repeaters to minimize EW interference | Combat unit systems |

**Market:** European cognitive EW market EUR 6.8B (2025) to EUR 28.5B by 2035. Leonardo/Faculty AI partnership (May 2025) for Cognitive Intelligent Sensing. NATO identifies EW/Cyber as 1 of 7 critical technology priorities.

---

### III. SPACE (4 capabilities)

#### 11. Launch & Re-entry

**Definition:** European sovereign access to orbit via commercial launch vehicles - small launchers, reusable rockets, and advanced propulsion including nuclear thermal for deep space.

**Subcategories:**
- Small/micro launchers (150-500kg to LEO)
- Medium-lift launch vehicles
- Reusable rocket technology
- Nuclear/ion propulsion for deep space

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Isar Aerospace | Germany | "Spectrum" rocket, largest European NewSpace company | ESA Launcher Challenge finalist, EUR 169M available |
| RFA | Germany | "RFA ONE" rocket, Block 2 upgrade planned | ESA Launcher Challenge finalist |
| PLD Space | Spain | "Miura 5" orbital vehicle, successful Miura 1 suborbital flight | EUR 82.7M government loans (2024) |
| Orbex | UK | "Prime" microlauncher, 3D-printed engines, 150kg to LEO | First flight 2025 from SaxaVord |
| MaiaSpace | France | ArianeGroup spinout | ESA Launcher Challenge finalist |
| Skyrora | UK | "Skyrora XL" three-stage, 315kg to LEO | Founded 2017 |
| HyImpulse | Germany | "SL1" hybrid propulsion, 500kg to LEO | Founded 2018 |

---

#### 12. In-Space Manufacturing & Servicing

**Definition:** Orbital robotics, active debris removal, satellite servicing, and microgravity manufacturing. Capabilities that extend useful life of space assets and create new space-based industries.

**Subcategories:**
- Active debris removal (ADR)
- On-orbit satellite servicing
- Microgravity manufacturing (semiconductors, materials)
- Orbital transportation

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| ClearSpace | Switzerland | First commercial debris removal mission | EUR 86M ESA contract, 2025 launch |
| Space Forge | UK | "ForgeStar" microgravity semiconductor manufacturing | UK's first in-space manufacturing license, ForgeStar-1 launched June 2025 |
| Astroscale UK | UK | In-Orbit Refurbishment and Upgrading Service | EUR 399K ESA contract, GBP 1.7M multi-debris mission |
| D-Orbit | Italy | ION Satellite Carrier, orbital transportation | - |

---

#### 13. Earth Observation & SSA

**Definition:** Satellite constellations for Earth observation (SAR, hyperspectral, optical) and Space Situational Awareness for tracking debris, satellites, and threats.

**Subcategories:**
- Synthetic Aperture Radar (SAR) constellations
- Hyperspectral imaging
- Space Situational Awareness (SSA)
- Data analytics and fusion

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| ICEYE | Finland | World's largest commercial SAR constellation (48 satellites) | 60/40 JV with Rheinmetall |
| U-Space | France | Europe's first SSA satellite, small satellite constellation | EUR 24M Series A (2025) |

---

#### 14. Stratospheric Platforms

**Definition:** High-altitude pseudo-satellites (HAPS) operating at 18-20km for persistent surveillance, communications relay, and environmental monitoring without orbital launch.

**Subcategories:**
- Solar-powered airships
- Hydrogen fuel cell platforms
- Stratospheric balloons
- Laser/RF relay payloads

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Stratospheric Platforms Ltd | UK | 60m wingspan hydrogen fuel cell HAP | Cambridge-based |
| Voltitude | UK | HAPS research | Farnborough-based |

**Programs:** Thales Alenia Space "Stratobus" (EUR 43M EuroHAPS), 140m helium airship at 18-20km. HAPPIEST Consortium (Spain) for environmental monitoring/border security.

---

### IV. ENERGY (4 capabilities)

#### 15. Fusion Energy

**Definition:** Controlled fusion reactors across all approaches - stellarator, tokamak, inertial confinement - targeting commercial power generation in the 2030s.

**Subcategories:**
- Stellarator designs
- Inertial confinement (laser-driven)
- Tokamak / magnetic confinement
- Fusion materials and superconductors

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Marvel Fusion | Germany | Laser-based inertial confinement, nano-structured fuel | EUR 385M total (EUR 170M private, EUR 215M public) |
| Proxima Fusion | Germany | Quasi-isodynamic stellarator, Max Planck spinout | EUR 130M Series A (June 2025) |
| Renaissance Fusion | France | High-temperature superconductor stellarator | EUR 32M raised |
| Gauss Fusion | Germany | Magnetic confinement, gigawatt-class architect | - |

---

#### 16. Advanced Fission

**Definition:** Small modular reactors (SMRs), Generation IV reactors, and advanced fuel cycle technologies including spent fuel recycling. Expands from original scope to include waste processing and fuel reprocessing.

**Subcategories:**
- Small Modular Reactors (SMR)
- Lead-cooled fast reactors
- Molten salt reactors
- Advanced fuel recycling and waste management

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Newcleo | Italy/France | Lead-cooled fast reactor recycling spent fuel | 850+ employees, 19 locations, 90+ partnerships, EUR 20M BPI grant |
| Seaborg | Denmark | Molten salt reactors on barges | Founded 2015 |

**Context:** Nine SMR projects selected for EU Industrial Alliance (2025). Finland Posiva operates world's first permanent nuclear waste repository (2025). Sweden repository construction started Jan 2025.

---

#### 17. Grid-Scale Storage

**Definition:** Long-duration energy storage beyond lithium-ion - flow batteries, gravity-based systems, compressed air, and supercapacitors for grid stabilization and renewable integration.

**Subcategories:**
- Vanadium/iron flow batteries
- Gravity and mechanical storage
- Supercapacitors for grid stabilization
- Hybrid storage systems

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| VoltStorage | Germany | Vanadium and Iron-Salt-Battery technology | EUR 38.75M raised, EUR 30M EIB venture loan |
| Energy Vault | Switzerland | Gravity-based energy storage | EUR 200.5M raised |
| Skeleton Technologies | Estonia | World's largest supercapacitor factory (EUR 220M SuperFactory Leipzig) | Expanding to Toulouse |
| Redox One | Cyprus | Iron-Chromium Redox Flow Batteries | EUR 28M raised |
| Unbound Potential | Switzerland | Membraneless redox flow batteries | EUR 6.7M |

---

#### 18. Solid-State Batteries

**Definition:** Beyond lithium-ion electrochemistry - solid-state, sodium-ion, and lithium-metal batteries that require entirely new manufacturing infrastructure and represent strategic sovereignty in energy storage.

**Subcategories:**
- Solid-state electrolytes (sulfide, oxide, polymer)
- Sodium-ion batteries
- Lithium-metal anodes
- Next-gen manufacturing processes

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Basquevolt | Spain | Solid-state battery technology | EUR 2.5M EIC Accelerator (9/9 score), EUR 10M follow-on |
| Ilika | UK | Solid-state battery manufacturing | Commercial production |
| Blue Solutions | France | Solid-state polymer batteries | Bollore Group |

**Context:** BMW/Volkswagen investing EUR 10B+ in European solid-state capacity. China's CATL spending $14B on next-gen battery R&D. MIT Technology Review names sodium-ion as 2026 Breakthrough Technology.

---

### V. MATERIALS & MANUFACTURING (3 capabilities)

#### 19. Critical Minerals

**Definition:** Rare earth extraction, lithium processing, battery recycling, and critical raw material recovery to reduce European dependence on Chinese supply chains.

**Subcategories:**
- Rare earth processing and separation
- Direct Lithium Extraction (DLE)
- Battery material recycling
- Critical raw material recovery

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Vulcan Energy | Germany | Direct Lithium Extraction, first mass-scale DLE in Germany | $2.5B raised |
| Cylib | Germany | End-of-life battery critical material extraction | $64M Series A |
| Tozero | Germany | Lithium-ion battery raw material recovery | $12M |
| Ionic Technologies | UK | Rare earth extraction from industrial magnets | Patented high-purity, low-impact process |
| Pensana | UK | Salt End rare earth processing facility (Yorkshire) | Targeting 5% worldwide Nd/Pr oxide supply |

**Regulatory:** EU Critical Raw Materials Act (2024) mandates 10% mining, 40% processing, 25% recycling by 2030.

---

#### 20. Advanced Manufacturing

**Definition:** Autonomous factories, industrial inspection robotics, and humanoid/cognitive robots for manufacturing - replacing human labor in dangerous, repetitive, or precision-critical tasks.

**Subcategories:**
- Industrial inspection robotics
- Flexible manufacturing automation (SME-focused)
- Humanoid robots for logistics/production
- Cognitive robots (AI + vision + touch)

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Neura Robotics | Germany | "Cognitive" robots with AI/vision/touch/learning | EUR 120M Series B (Jan 2025) |
| 1X | Norway | Humanoid robots "EVE" and "NEO" | Oslo-based |
| RobCo | Germany | Flexible robotic hardware kits for SMEs | TUM spinout 2020 |
| Keybotic | Spain | "Keyper" quadruped for industrial inspections | Barcelona-based |
| PAL Robotics | Spain | First fully autonomous humanoid robot in Europe | Founded 2004 |
| Energy Robotics | Germany | Self-operating robots for industrial inspection | Boston Dynamics Spot integration |

---

#### 21. Novel Materials

**Definition:** Metamaterials, graphene applications, high-temperature superconductors, and advanced composites that enable new physics - from brain implants to hypersonic thermal protection.

**Subcategories:**
- Graphene electronics and bioelectronics
- High-temperature superconductors
- Hypersonic thermal protection materials
- Advanced composites and metamaterials

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Inbrain | Spain | Graphene electrodes for brain stimulation (epilepsy, Parkinson's) | EUR 46M Series B (2024), ICN2 spinout |
| Graphenea | Spain/France | Single-crystal graphene for superconductor foundations | EU FantastiCOF project |
| iCOMAT | UK | High-temperature composites for hypersonic missiles (2,200C) | - |

---

### VI. SENSING & INTELLIGENCE (4 capabilities)

#### 22. Subsurface Intelligence

**Definition:** AI-powered underground mapping, geothermal intelligence, and subsurface infrastructure detection using sensor fusion and machine learning.

**Subcategories:**
- Underground infrastructure mapping
- Geothermal resource intelligence
- Subsurface AI/ML analytics
- Sensor fusion for buried objects

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Exodigo | Israel/Europe | Underground infrastructure mapping | $214M raised, VINCI/GRDF France project |
| 4M Analytics | TBD | AI-powered subsurface mapping from legacy data | - |
| Enerdrape | Switzerland | Geothermal panel technology | EPFL spinout |

---

#### 23. Quantum Sensing

**Definition:** Quantum gravimeters, atomic clocks, and magnetic field sensors using atom interferometry for navigation, resource exploration, and defense applications.

**Subcategories:**
- Quantum gravimeters/gradiometers
- Atomic clocks for positioning
- Magnetic field sensors
- Aerial quantum sensor platforms

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Muquans | France | Gravimeters from atom interferometers | Bordeaux-based |
| Exail Quantum Sensors | France | Portable atom interferometry gravity sensors | Formerly iXblue |

**Programs:** EQUIP-G Consortium (11 EU countries, 20 partners, EUR 25M Horizon Europe) building EU-wide quantum gravimeter network.

---

#### 24. Underwater & Subsea Autonomy

**Definition:** Autonomous underwater vehicles, deep-sea robotics, distributed acoustic sensing on subsea cables, and ocean infrastructure protection. Domain with unique physics (pressure, acoustics, currents) distinct from air/land/space.

**Subcategories:**
- Ultra-deep AUVs (6000m+)
- Distributed Acoustic Sensing (DAS) on cables
- Deep-sea mining robotics
- Subsea cable infrastructure protection

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Exail | France | A6K ultra-deep AUV for >6000m operations | Deployed by multiple NATO navies |

**Programs:** EU ROBUST project for autonomous deep-sea mining robots. UK/Netherlands/Germany/Norway deploying DAS systems for maritime security. Blue Nodules (EU) for AI-driven nodule harvesting.

---

#### 25. Biological Engineering

**Definition:** Synthetic biology, DNA synthesis, protein engineering, and bio-manufacturing platforms that program biology for industrial and defense applications.

**Subcategories:**
- DNA synthesis and genome engineering
- Protein design and engineering
- Bacterial cell factories
- Bio-manufacturing platforms

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Ribbon Biolabs | Austria | Genome synthesis, CRISPR libraries, patented biochemistry | Vienna-based |
| Evonetix | UK | Semiconductor technology for DNA synthesis | Cambridge-based |
| Protera Bio | France | Deep learning for novel food ingredients | Protein sequence-structure-function mapping |
| Cysbio | Denmark | Bacterial cell factories for amino acids | Proprietary synthetic biology processes |
| Salipro Biotech | Sweden | Drug discovery on membrane proteins | - |

---

### VII. INFRASTRUCTURE RESILIENCE (3 capabilities)

#### 26. Privacy-Preserving Computation

**Definition:** Fully Homomorphic Encryption (FHE), Secure Multi-Party Computation (MPC), and Confidential Computing that enable computation on encrypted data - a European strategic advantage given GDPR.

**Subcategories:**
- Fully Homomorphic Encryption (FHE)
- Secure Multi-Party Computation (MPC)
- Confidential Computing (TEEs)
- Privacy-preserving analytics

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Zama | France | World's first FHE unicorn, open-source cryptography | $57M Series B (2025), $1B+ valuation |
| Partisia | Denmark | MPC for facial recognition, digital identity, healthcare | Co-founded by Ivan Damgaard |
| Tune Insight | Switzerland | Privacy-preserving analytics | EPFL spinout |
| Cosmian | France | Functional Encryption + FHE + MPC + Secure Enclaves | $1.5M seed |
| Edgeless Systems | Germany | Confidential computing using TEEs | Runtime encryption |

---

#### 27. Hypersonic Systems

**Definition:** Hypersonic propulsion, thermal management, and weapons systems capable of Mach 5+ flight. Europe's thinnest capability area - one private company versus US and Chinese national programs.

**Subcategories:**
- Hypersonic strike vehicles
- Thermal protection and materials
- Counter-hypersonic defense
- Scramjet / combined-cycle propulsion

**Companies:**

| Company | Country | What They Do | Funding / Validation |
|---|---|---|---|
| Hypersonica | Germany | First privately funded European hypersonic flight | Founded Dec 2023, targeting strike by 2029, costs >80% below incumbents |
| iCOMAT | UK | High-temperature composites for hypersonic missiles | Materials withstand 2,200C |

**Programs:** HYDIS2 consortium (MBDA-led) for hypersonic defense interceptor with EU Commission funding. HYDEF program for counter-hypersonic capabilities.

---

#### 28. Directed Energy

**Definition:** High-energy laser weapons and directed energy systems for counter-drone, counter-missile, and short-range air defense applications.

**Subcategories:**
- High-energy laser weapons (HEL)
- Counter-drone laser systems
- Shipboard directed energy
- Modular/mobile DEW platforms

**Companies / Programs:**

| Entity | Country | What They Do | Validation |
|---|---|---|---|
| DragonFire | UK (MoD + industry) | First successful aerial target engagement | GBP 100M investment |
| TALOS-TWO | 8 EU nations, 21 partners | Operational lasers by 2030 | EUR 25M funding |
| EU DES (PESCO) | EU | Modular DEWs for mobile platforms | May 2025-2029 |

**Note:** Directed energy is currently dominated by established defense primes (Thales, MBDA, Rheinmetall). Startup layer has not yet emerged. German shipboard laser deployed Nov 2022.

---

## Cross-Cutting Patterns

### Geographic Clusters

| Country | Strength Areas |
|---|---|
| **Germany** | Defense AI (Helsing), fusion (Proxima, Marvel), hypersonics (Hypersonica), launch (Isar, RFA), photonics (Q.ANT), critical minerals (Vulcan, Cylib), robotics (Neura, ARX) |
| **France** | Quantum (PASQAL, Quandela), fusion (Renaissance), nuclear (Newcleo), crypto (Zama), space (MaiaSpace, Exail), military AI (Harmattan) |
| **UK** | Post-quantum crypto (PQShield), quantum (OQC, ORCA), orbital manufacturing (Space Forge), launch (Orbex, Skyrora), HAPS, swarm tech (SeeByte, Blue Bear) |
| **Nordics** | Quantum hardware (IQM-Finland), SAR (ICEYE-Finland), defense drones (Denmark, Lithuania), robotics (1X-Norway), nuclear (Seaborg-Denmark), supercapacitors (Skeleton-Estonia) |
| **Spain** | RISC-V (Openchip, Semidynamics), robotics (Keybotic, PAL), materials (Inbrain), launch (PLD Space), batteries (Basquevolt) |
| **Switzerland** | Debris removal (ClearSpace), crypto (ID Quantique), privacy (Tune Insight), neuromorphic (SynSense) |

### Mega-Rounds (>EUR 100M)

| Company | Total Raised | Domain |
|---|---|---|
| Helsing | EUR 1.37B | Defense AI |
| Marvel Fusion | EUR 385M | Fusion |
| Proxima Fusion | EUR 130M | Fusion |
| Neura Robotics | EUR 120M | Robotics |
| PASQAL | $140M | Quantum |

### Portfolio Mapping (Inflection)

8 of 28 capabilities directly covered by Inflection portfolio companies:

| Capability | Portfolio Company |
|---|---|
| Sovereign Processors | Ubitium, Fabric |
| Secure Communications | Hedy |
| Privacy-Preserving Computation | Tune Insight |
| Autonomous Unmanned Systems | Ark |
| Subsurface Intelligence | Deep Earth |
| Stratospheric Platforms | Radical |
| In-Space Manufacturing | Lodestar |
| Critical Minerals | Senken (carbon markets, adjacent) |

71% of companies in Hard Futures will be non-portfolio. Inflection coverage maps to thesis vectors: Scale (Compute, Energy), Resilience (Defense, Infrastructure), Flow (Space, Sensing).

---

## Ecosystem Health

### Strong Signals
- European defense VC +24% in 2024 ($5.2B) despite broader downturn
- Deep tech = 33% of all EU VC (EUR 15B in 2024)
- Novel AI funding +100% YoY ($3.0B)
- Fusion startup funding shattered records (2025)

### Weak Signals
- Battery gigafactory crisis (Northvolt, Freyr, Britishvolt all failed/paused)
- Secure comms/mesh networking dominated by US tech + EU integrators
- Privacy-preserving compute has only 2-3 commercial players vs dozens in US
- Counter-UAS startups fragmented, lack integration
- Hypersonic systems: one private company (Hypersonica) vs US/China national programs

### Gaps vs US/China
- Large-scale semiconductor fabs (no European equivalent to TSMC/Samsung foundry)
- Hypersonic propulsion at scale
- Quantum computing scale (largest EU = 100 qubits vs 1000+ in US)
- Autonomous weapons integration (ethical/regulatory constraints)

---

## Next Steps

This is a working document. Before finalizing:
- [ ] Review capability definitions and boundaries
- [ ] Validate company list completeness (target: 8-15 per capability)
- [ ] Decide on thin capabilities: Stratospheric Platforms, Directed Energy, Hypersonics have <3 startups each
- [ ] Add graph relationship types (shared investors, program co-participation, supply chain)
- [ ] Define v1 technical architecture
