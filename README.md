# Organ Transplant Matching System - Knowledge Base

A rule-based knowledge repository for matching donated organs to the most
suitable, compatible, and urgent recipient, built as part of Knowledge
Engineering (BCS-405) coursework at IGDTUW.

## Problem Domain

When an organ becomes available from a donor, it must be matched to the most
suitable, medically compatible, and most urgently in-need recipient before the
organ's limited viability window expires. This depends on blood type
compatibility, organ viability time, recipient urgency and eligibility,
hospital surgical capacity, and transport logistics between hospitals.

## Repository Structure

```
organ-transplant-knowledge-base/
│
├── README.md                     # This file
├── facts/
│   ├── donors.json                # Donor fact base
│   ├── organs.json                # Organ fact base
│   ├── recipients.json            # Recipient fact base
│   └── hospitals.json             # Hospital fact base
├── rules/
│   └── production_rules.md        # All 20 IF-THEN production rules
├── engine/
│   └── inference_engine.py        # Forward-chaining inference engine
├── resolution/
│   └── resolution_proof.py        # Resolution-based refutation proof
└── outputs/
    └── sample_queries_output.txt  # Recorded sample query outputs
```

## How to Run

**Inference engine (forward chaining):**
```bash
python engine/inference_engine.py
```

**Resolution proof (refutation resolution):**
```bash
python resolution/resolution_proof.py
```

## Knowledge Engineering Components

- **Fact Base** – donors, organs, recipients, and hospitals, each with their
  key attributes (`facts/`)
- **Rule Base** – 20 production rules covering donor eligibility, organ
  viability, recipient priority, blood compatibility, hospital readiness, and
  transport logistics (`rules/`)
- **Inference Engine** – a forward-chaining, data-driven engine that matches
  organs to recipients and recommends transport logistics (`engine/`)
- **Resolution Proof** – a refutation-resolution program that formally proves
  a sample match decision follows from the knowledge base (`resolution/`)

## Author

Yashika Gupta
B.Tech CSE-3 (B3), Enrollment No. 22501012023
Indira Gandhi Delhi Technical University for Women
