import argparse
import boto3
import json
from botocore.exceptions import NoCredentialsError, ClientError
from tabulate import tabulate
import fnmatch
import csv

RISKY_PATTERNS = [
    "AdministratorAccess",
    "*admin*",
    "custom-admin-*",
    "custom-*"
]

def load_sample_data():
    """Load IAM user-policy mappings from local mock file."""
    with open("mock_data.json", "r") as f:
        return json.load(f)

def fetch_iam_user_policies():
    """Fetch IAM users and their attached policies using boto3."""
    iam = boto3.client("iam")
    users = iam.list_users()["Users"]

    user_policies = []
    for user in users:
        username = user["UserName"]
        attached = iam.list_attached_user_policies(UserName=username)["AttachedPolicies"]
        for policy in attached:
            user_policies.append({
                "User": username,
                "Policy": policy["PolicyName"]
            })

    return user_policies

def is_risky(policy_name):
    """Check if a policy name matches any of the risky patterns using wildcards."""
    name = policy_name.lower()
    for pattern in RISKY_PATTERNS:
        if fnmatch.fnmatch(name, pattern.lower()):
            return True
    return False


def filter_risky_policies(user_policies):
    """Filter risky users and tag them with a risk level."""
    results = []
    for entry in user_policies:
        if is_risky(entry["Policy"]):
            entry_with_risk = {
                "User": entry["User"],
                "Policy": entry["Policy"],
                "Risk": classify_risk(entry["Policy"])
            }
            results.append(entry_with_risk)
    return results

def write_csv(data, output_file):
    """Write data to a CSV file."""
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def write_json(data, output_file):
    """Write data to a JSON file."""
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

def write_markdown(data, output_file):
    """Write data to a markdown file using GitHub-flavored table."""
    with open(output_file, "w") as f:
        f.write(tabulate(data, headers="keys", tablefmt="github"))

def has_valid_aws_session():
    """Check if AWS credentials are configured and valid."""
    try:
        boto3.client("sts").get_caller_identity()
        return True
    except ClientError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Scan IAM users for risky policies")
    parser.add_argument("--use-sample", action="store_true", help="Force use of mock data from mock_data.json")
    parser.add_argument("--output", help="Path to output file (auto-determined if not provided)")
    parser.add_argument("--format", choices=["md", "csv", "json"], help="Output format: md, csv, or json")
    args = parser.parse_args()

    # Prompt if format not provided
    if not args.format:
        print("Select an output format:")
        print("  1. Markdown (.md)")
        print("  2. CSV (.csv)")
        print("  3. JSON (.json)")
        choice = input("Enter format [1-3]: ").strip()
        format_map = {"1": "md", "2": "csv", "3": "json"}
        args.format = format_map.get(choice)

    if not args.format:
        print("[-] Invalid format selected. Exiting.")
        return

    # Dynamically set output file if not provided
    if not args.output:
        args.output = f"output.{args.format}"

    # Fetch data
    if args.use_sample:
        print("[!] Forcing sample mode (--use-sample enabled)\n")
        raw_data = load_sample_data()
    elif not has_valid_aws_session():
        print("[-] AWS credentials not found or invalid.")
        print("    Please run `aws configure`, `aws sso login`, or use your preferred session method.\n")
        print("[!] Falling back to sample data...\n")
        raw_data = load_sample_data()
    else:
        try:
            print("[✓] Fetching IAM users via AWS API...\n")
            raw_data = fetch_iam_user_policies()
        except ClientError as e:
            print(f"[-] AWS error during fetch: {e}")
            print("[!] Falling back to sample data...\n")
            raw_data = load_sample_data()

    # Analyze
    risky_users = filter_risky_policies(raw_data)
    if not risky_users:
        print("[✓] No risky IAM users found.")
        return

    # Print summary
    print("\n[!] Risky IAM Users Found:\n")
    print(tabulate(risky_users, headers="keys", tablefmt="github"))

    # Write to file
    if args.format == "md":
        write_markdown(risky_users, args.output)
    elif args.format == "csv":
        write_csv(risky_users, args.output)
    elif args.format == "json":
        write_json(risky_users, args.output)
    else:
        print(f"[-] Unsupported format: {args.format}")
        return

    print(f"\n[✓] Summary written to: {args.output} ({args.format.upper()})")


def classify_risk(policy_name):
    name = policy_name.lower()

    if name == "administratoraccess":
        return "High"
    elif fnmatch.fnmatch(name, "*admin*"):
        return "High"
    elif fnmatch.fnmatch(name, "custom-*"):
        return "Medium"
    elif fnmatch.fnmatch(name, "readonlyaccess"):
        return "Low"
    else:
        return "Medium"


if __name__ == "__main__":
    main()
