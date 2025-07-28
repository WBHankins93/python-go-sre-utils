import json
from typing import List, Dict

def parse_plan_file(path: str) -> Dict:
    """Load and return the full JSON content from the plan file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Error reading Terraform plan file: {e}")

def extract_resource_changes(plan_json: Dict) -> List[Dict]:
    """
    Extracts a list of resource changes from the Terraform plan.
    Returns a list of dicts with keys: type, name, actions.
    """
    changes = []

    for rc in plan_json.get("resource_changes", []):
        actions = rc.get("change", {}).get("actions", [])
        if not actions:
            continue

        changes.append({
            "address": rc.get("address"),
            "type": rc.get("type"),
            "name": rc.get("name"),
            "provider": rc.get("provider_name"),
            "actions": actions
        })

    return changes
