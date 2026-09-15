# Production Rule Base - Organ Transplant Matching System

| Rule | IF (Condition) | THEN (Inference) |
|------|-----------------|-------------------|
| R1  | Donor age > 60 AND organ = Heart | Age Restricted - Specialist Review Required |
| R2  | Donor consent_status != Confirmed | Donation On Hold - Awaiting Consent |
| R3  | Organ remaining_viability <= 0 | Organ Expired - Discard |
| R4  | 0 < remaining_viability <= 3 hrs | Near Expiry - Urgent Transport Required |
| R5  | remaining_viability > 3 hrs | Viable - Standard Handling |
| R6  | Recipient blood type not in donor's compatibility list | Not Compatible - Reject Match |
| R7  | Recipient urgency_score >= 9 | Critical Priority |
| R8  | 7 <= urgency_score <= 8 | High Priority |
| R9  | 5 <= urgency_score <= 6 | Moderate Priority |
| R10 | urgency_score < 5 | Low Priority |
| R11 | Recipient health_status = Poor | Not Currently Eligible - Medical Clearance Required |
| R12 | waiting_time_days > 180 | Long-Term Waitlist - Priority Boost |
| R13 | Recipient health_status = Critical | Immediate Transplant Required |
| R14 | Hospital surgeons_available = 0 | Insufficient Surgeons - Reroute Required |
| R15 | Hospital surgeons_available = 1 | Low Surgical Capacity - Schedule With Caution |
| R16 | distance(donor, recipient) = 0 | In-House Transfer - No Transport Required |
| R17 | remaining_viability > 2 x ground_travel_time | Ground Transport Sufficient |
| R18 | ground_travel_time < remaining_viability <= 2 x ground_travel_time | Helicopter Transport Recommended |
| R19 | remaining_viability <= ground_travel_time | Transport Infeasible - Organ Will Expire En Route |
| R20 | No eligible, compatible recipient found | Expand Search Radius / Alert Network |

## Notes
- Rules R1-R2 apply to the **Donor** entity.
- Rules R3-R5 apply to the **Organ** entity (viability window).
- Rules R6-R13 apply to the **Recipient** entity (compatibility and priority).
- Rules R14-R15 apply to the **Hospital** entity (surgical readiness).
- Rules R16-R20 apply to the **Transport/Matching** sub-inference (logistics and fallback).
