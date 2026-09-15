# ==========================================================
# KNOWLEDGE BASE FOR ORGAN TRANSPLANT MATCHING SYSTEM
# ==========================================================

# ---------------------------
# FACT BASE
# ---------------------------
donors = {
    "D1": {
        "name": "Rajesh Kumar",
        "blood_type": "O+",
        "age": 34,
        "health_status": "Healthy",
        "consent_status": "Confirmed",
        "location": "Hospital A",
        "organs_available": ["Kidney", "Liver"]
    },
    "D2": {
        "name": "Sunita Verma",
        "blood_type": "AB+",
        "age": 62,
        "health_status": "Healthy",
        "consent_status": "Confirmed",
        "location": "Hospital C",
        "organs_available": ["Heart", "Cornea"]
    },
    "D3": {
        "name": "Arjun Mehta",
        "blood_type": "A-",
        "age": 21,
        "health_status": "Healthy",
        "consent_status": "Pending",
        "location": "Hospital B",
        "organs_available": ["Kidney"]
    }
}

organs = {
    "O1": {"type": "Kidney", "donor_id": "D1", "blood_type": "O+",
           "harvested_hours_ago": 2, "viability_hours": 24,
           "condition": "Good", "location": "Hospital A"},
    "O2": {"type": "Liver", "donor_id": "D1", "blood_type": "O+",
           "harvested_hours_ago": 9, "viability_hours": 12,
           "condition": "Good", "location": "Hospital A"},
    "O3": {"type": "Heart", "donor_id": "D2", "blood_type": "AB+",
           "harvested_hours_ago": 5, "viability_hours": 6,
           "condition": "Good", "location": "Hospital C"},
    "O4": {"type": "Cornea", "donor_id": "D2", "blood_type": "AB+",
           "harvested_hours_ago": 100, "viability_hours": 96,
           "condition": "Good", "location": "Hospital C"}
}

recipients = {
    "P1": {"name": "Anita Sharma", "blood_type": "O+", "organ_needed": "Kidney",
           "urgency_score": 9, "age": 45, "health_status": "Stable",
           "waiting_time_days": 210, "location": "Hospital B"},
    "P2": {"name": "Vikram Singh", "blood_type": "A+", "organ_needed": "Liver",
           "urgency_score": 8, "age": 50, "health_status": "Stable",
           "waiting_time_days": 60, "location": "Hospital A"},
    "P3": {"name": "Meera Iyer", "blood_type": "AB+", "organ_needed": "Heart",
           "urgency_score": 10, "age": 39, "health_status": "Critical",
           "waiting_time_days": 15, "location": "Hospital C"},
    "P4": {"name": "Farhan Ali", "blood_type": "O-", "organ_needed": "Kidney",
           "urgency_score": 6, "age": 55, "health_status": "Poor",
           "waiting_time_days": 300, "location": "Hospital B"},
    "P5": {"name": "Kavya Reddy", "blood_type": "B+", "organ_needed": "Cornea",
           "urgency_score": 4, "age": 29, "health_status": "Stable",
           "waiting_time_days": 30, "location": "Hospital C"}
}

hospitals = {
    "H1": {"name": "Hospital A", "surgeons_available": 2, "transplant_capacity": 5},
    "H2": {"name": "Hospital B", "surgeons_available": 0, "transplant_capacity": 3},
    "H3": {"name": "Hospital C", "surgeons_available": 1, "transplant_capacity": 6}
}

# distance in km between hospital locations
distances = {
    ("Hospital A", "Hospital B"): 40,
    ("Hospital A", "Hospital C"): 250,
    ("Hospital B", "Hospital C"): 300
}


def get_distance(loc1, loc2):
    if loc1 == loc2:
        return 0
    return distances.get((loc1, loc2), distances.get((loc2, loc1)))


# Blood type compatibility chart (donor -> recipients it can donate to)
blood_compatibility = {
    "O-": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    "O+": ["O+", "A+", "B+", "AB+"],
    "A-": ["A-", "A+", "AB-", "AB+"],
    "A+": ["A+", "AB+"],
    "B-": ["B-", "B+", "AB-", "AB+"],
    "B+": ["B+", "AB+"],
    "AB-": ["AB-", "AB+"],
    "AB+": ["AB+"]
}


def blood_compatible(donor_bt, recipient_bt):
    return recipient_bt in blood_compatibility[donor_bt]


# ---------------------------
# INFERENCE ENGINE
# ---------------------------
def infer_donor(donor):
    inferred = set()
    # RULE 1: Age restriction for heart donation
    if donor["age"] > 60 and "Heart" in donor["organs_available"]:
        inferred.add("Age Restricted - Specialist Review Required")
    # RULE 2: Consent pending
    if donor["consent_status"] != "Confirmed":
        inferred.add("Donation On Hold - Awaiting Consent")
    else:
        inferred.add("Eligible Donor")
    return inferred


def infer_organ(organ):
    inferred = set()
    remaining = organ["viability_hours"] - organ["harvested_hours_ago"]
    # RULE 3: Expired
    if remaining <= 0:
        inferred.add("Expired")
    # RULE 4: Near expiry
    elif remaining <= 3:
        inferred.add("Near Expiry - Urgent Transport Required")
    # RULE 5: Viable
    else:
        inferred.add("Viable - Standard Handling")
    return inferred, remaining


def infer_recipient(recipient):
    inferred = set()
    score = recipient["urgency_score"]
    # RULE 7-10: Priority levels
    if score >= 9:
        inferred.add("Critical Priority")
    elif score >= 7:
        inferred.add("High Priority")
    elif score >= 5:
        inferred.add("Moderate Priority")
    else:
        inferred.add("Low Priority")
    # RULE 11: Eligibility based on health
    if recipient["health_status"] == "Poor":
        inferred.add("Not Currently Eligible - Medical Clearance Required")
    # RULE 12: Long waitlist boost
    if recipient["waiting_time_days"] > 180:
        inferred.add("Long-Term Waitlist - Priority Boost")
    # RULE 13: Critical health status
    if recipient["health_status"] == "Critical":
        inferred.add("Immediate Transplant Required")
    return inferred


def infer_hospital(hospital):
    inferred = set()
    # RULE 14: No surgeons
    if hospital["surgeons_available"] == 0:
        inferred.add("Insufficient Surgeons - Reroute Required")
    # RULE 15: Low capacity
    elif hospital["surgeons_available"] == 1:
        inferred.add("Low Surgical Capacity - Schedule With Caution")
    else:
        inferred.add("Hospital Ready")
    return inferred


def find_best_match(organ_id):
    organ = organs[organ_id]
    organ_status, remaining = infer_organ(organ)

    # RULE 3: cannot match an expired organ
    if "Expired" in organ_status:
        return None, organ_status, remaining

    candidates = []
    for rid, r in recipients.items():
        if r["organ_needed"] != organ["type"]:
            continue
        if not blood_compatible(organ["blood_type"], r["blood_type"]):
            continue
        r_status = infer_recipient(r)
        # RULE 11: skip recipients not currently eligible
        if "Not Currently Eligible - Medical Clearance Required" in r_status:
            continue
        candidates.append((-r["urgency_score"], -r["waiting_time_days"], rid))

    if not candidates:
        # RULE 20: no compatible recipient
        return None, organ_status, remaining

    candidates.sort()
    best_rid = candidates[0][2]
    return best_rid, organ_status, remaining


def recommend_transport(organ_id, recipient_id, remaining):
    organ = organs[organ_id]
    recipient = recipients[recipient_id]
    dist = get_distance(organ["location"], recipient["location"])

    # RULE 16: same-hospital transfer
    if dist == 0:
        return "In-House Transfer - No Transport Required", 0

    ground_speed = 40   # km/h
    air_speed = 200      # km/h
    travel_time_ground = dist / ground_speed

    # RULE 17: ground transport sufficient
    if remaining > 2 * travel_time_ground:
        return f"Ground Transport Sufficient (~{travel_time_ground:.1f} hrs)", travel_time_ground

    # RULE 19: transport infeasible
    if remaining <= travel_time_ground:
        return "Transport Infeasible - Organ Will Expire En Route", travel_time_ground

    # RULE 18: helicopter recommended
    travel_time_air = dist / air_speed
    return f"Helicopter Transport Recommended (~{travel_time_air:.1f} hrs)", travel_time_air


def process_organ_donation(organ_id):
    organ = organs[organ_id]
    print(f"\nOrgan ID: {organ_id} | Type: {organ['type']} | Donor: {organ['donor_id']}")

    best_rid, organ_status, remaining = find_best_match(organ_id)
    print("Remaining Viability:", round(remaining, 1), "hours")
    print("Organ Status:", ", ".join(sorted(organ_status)))

    if "Expired" in organ_status:
        print("Result: Organ discarded - not viable for transplant.")
        return

    if best_rid is None:
        # RULE 20
        print("Result: No compatible recipient found - Expand Search Radius / Alert Network")
        return

    recipient = recipients[best_rid]
    r_status = infer_recipient(recipient)
    print(f"Best Match: {best_rid} - {recipient['name']} ({', '.join(sorted(r_status))})")

    transport_msg, _ = recommend_transport(organ_id, best_rid, remaining)
    print("Transport Recommendation:", transport_msg)


def donor_status(donor_id):
    donor = donors[donor_id]
    status = infer_donor(donor)
    print(f"\nDonor ID: {donor_id} | Name: {donor['name']} | Blood Type: {donor['blood_type']} | Age: {donor['age']}")
    print("Inferred Status:", ", ".join(sorted(status)))


def hospital_status(hospital_id):
    hospital = hospitals[hospital_id]
    status = infer_hospital(hospital)
    print(f"\nHospital ID: {hospital_id} | Name: {hospital['name']} | Surgeons Available: {hospital['surgeons_available']}")
    print("Inferred Status:", ", ".join(sorted(status)))


# ---------------------------
# SAMPLE QUERIES
# ---------------------------
if __name__ == "__main__":
    print("ORGAN TRANSPLANT MATCHING SYSTEM")
    print("=" * 55)

    print("\nQUERY 1: Eligibility status of Donor D1")
    donor_status("D1")

    print("\nQUERY 2: Match and transport plan for Organ O1 (Kidney)")
    process_organ_donation("O1")

    print("\nQUERY 3: Match and transport plan for Organ O3 (Heart)")
    process_organ_donation("O3")

    print("\nQUERY 4: Match attempt for Organ O4 (Expired Cornea)")
    process_organ_donation("O4")

    print("\nQUERY 5: Surgical readiness of Hospital C")
    hospital_status("H3")
