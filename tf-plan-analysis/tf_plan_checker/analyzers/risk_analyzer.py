from typing import List, Dict

# Hardcoded initial ruleset (configurable later)
HIGH_RISK_TYPES = {
    "aws_iam_policy",
    "aws_iam_role",
    "aws_security_group",
    "aws_s3_bucket_public_access_block"
}

DESTRUCTIVE_ACTIONS = {"delete", "replace"}

def classify_risks(resource_changes: List[Dict]) -> List[Dict]:
    """
    Annotate each resource change with a 'risk_level': High, Medium, Low.
    """
    classified = []

    for rc in resource_changes:
        risk = "Low"
        resource_type = rc["type"]
        actions = set(rc["actions"])

        # High risk if sensitive type or destructive actions
        if resource_type in HIGH_RISK_TYPES or actions & DESTRUCTIVE_ACTIONS:
            risk = "High"
        elif "update" in actions:
            risk = "Medium"

        rc_with_risk = rc.copy()
        rc_with_risk["risk_level"] = risk
        classified.append(rc_with_risk)

    return classified
