from tf_plan_checker.cli import parse_args
from tf_plan_checker.parsers.json_parser import parse_plan_file, extract_resource_changes

def main():
    args = parse_args()

    print("Terraform Plan Diff Checker")
    plan = parse_plan_file(args.input)
    changes = extract_resource_changes(plan)

    print(f"\n🔍 Found {len(changes)} resource changes:\n")
    for change in changes:
        print(f"- {change['address']}: {', '.join(change['actions'])}")
