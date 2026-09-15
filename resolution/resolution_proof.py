# ==========================================================
# KNOWLEDGE RESOLUTION - ORGAN TRANSPLANT MATCHING SYSTEM
# ==========================================================

# Each clause is represented as a set of literals (strings).
# A negated literal is prefixed with '~'.

clauses = [
    {"eligible_donor(D1)"},                                    # C1
    {"viable(O1)"},                                             # C2
    {"compatible(O1,P1)"},                                      # C3
    {"critical_priority(P1)"},                                  # C4
    {"~eligible_donor(D1)", "~viable(O1)",
     "~compatible(O1,P1)", "~critical_priority(P1)",
     "match(O1,P1)"},                                           # C5 - Rule
    {"~match(O1,P1)"}                                            # C6 - Negated Goal
]


def negate(literal):
    return literal[1:] if literal.startswith("~") else "~" + literal


def resolve(clause1, clause2):
    """Try to resolve two clauses. Return the resolvent clause, or None."""
    for lit in clause1:
        if negate(lit) in clause2:
            new_clause = (clause1 - {lit}) | (clause2 - {negate(lit)})
            return new_clause
    return None


def resolution_algorithm(clauses, goal_name):
    kb = clauses[:]
    step = 1
    print(f"Goal to prove: {goal_name}\n")
    print("Initial Clauses:")
    for i, c in enumerate(kb, 1):
        print(f"  C{i}: {c if c else '{}'}")

    new = set()
    while True:
        pairs = [(kb[i], kb[j]) for i in range(len(kb)) for j in range(i + 1, len(kb))]
        resolved_something = False

        for (ci, cj) in pairs:
            resolvent = resolve(ci, cj)
            if resolvent is not None:
                if not resolvent:  # empty clause derived
                    print(f"\nStep {step}: Resolved {ci} with {cj} --> EMPTY CLAUSE {{}}")
                    print(f"\nContradiction found. Therefore, '{goal_name}' is PROVEN TRUE.")
                    return True
                if resolvent not in kb and resolvent not in new:
                    print(f"Step {step}: Resolved {ci} with {cj} --> {resolvent}")
                    new.add(frozenset(resolvent))
                    resolved_something = True
                    step += 1

        if not resolved_something:
            print("\nNo new clauses can be derived. Goal could not be proven.")
            return False

        for nc in new:
            if set(nc) not in kb:
                kb.append(set(nc))
        new = set()


if __name__ == "__main__":
    print("KNOWLEDGE RESOLUTION - ORGAN TRANSPLANT MATCHING SYSTEM")
    print("=" * 60)
    resolution_algorithm(clauses, "match(O1,P1)")
