from tf_plan_checker.cli import parse_args
from tf_plan_checker.parsers.json_parser import parse_plan_file, extract_resource_changes
from tf_plan_checker.analyzers.risk_analyzer import classify_risks

def main():
    args = parse_args()

    print("Terraform Plan Diff Checker")
    plan = parse_plan_file(args.input)
    changes = extract_resource_changes(plan)
    classified = classify_risks(changes)

    print(f"\n🔍 Found {len(classified)} resource changes:\n")
    for change in classified:
        print(f"- {change['address']}: {', '.join(change['actions'])}")