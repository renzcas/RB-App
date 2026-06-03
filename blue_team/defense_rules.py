import time

# Initial symbolic rules
symbolic_rules = [
    {"name": "HighEntropyBlock", "threshold": 4.0, "trigger_count": 0},
    {"name": "NullTokenBlock", "threshold": None, "trigger_count": 0},
    {"name": "Status403Block", "threshold": 403, "trigger_count": 0},
]

def apply_rules(event):
    """
    event = {"token": str, "status": int, "length": int, "entropy": float}
    """
    decisions = []
    for rule in symbolic_rules:
        if rule["name"] == "HighEntropyBlock" and event["entropy"] > rule["threshold"]:
            decisions.append("Blocked: High Entropy")
            rule["trigger_count"] += 1
        elif rule["name"] == "NullTokenBlock" and event["token"] in ["", "null", None]:
            decisions.append("Blocked: Null Token")
            rule["trigger_count"] += 1
        elif rule["name"] == "Status403Block" and event["status"] == rule["threshold"]:
            decisions.append("Blocked: 403 Response")
            rule["trigger_count"] += 1
    if not decisions:
        decisions.append("Allowed")
    return decisions

def evolve_rules():
    """
    Mutate thresholds if drift persists.
    Example: lower entropy threshold if triggered too often.
    """
    mutation_log = []
    for rule in symbolic_rules:
        if rule["name"] == "HighEntropyBlock" and rule["trigger_count"] > 10:
            old = rule["threshold"]
            rule["threshold"] -= 0.5
            mutation_log.append({
                "Rule": rule["name"],
                "OldThreshold": old,
                "NewThreshold": rule["threshold"],
                "Timestamp": time.time()
            })
            rule["trigger_count"] = 0  # reset after mutation
    return mutation_log