from jiratagger.app.jira_tagger import JiraTagger
import argparse
import sys
import os
import json
import csv

def parse_arguments():
    parser = argparse.ArgumentParser(description='JiraTagger - Label Jira issues with tags and comments or compare saved state.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('issue_keys_file', nargs='?', help='Path to the file containing Jira issue keys.')
    group.add_argument('--resume', metavar='JSON_FILE', help='Resume from a saved state file.')
    
    parser.add_argument('--compare', metavar='CSV_FILE', help='Compare a saved state file with a CSV to find missing issues.')
    parser.add_argument('jira_url', nargs='?', help='Base URL of the Jira instance.')
    args = parser.parse_args()

    if args.compare and not args.resume:
        # Ensure both `resume` and `compare` are provided when using `--compare`
        parser.error("Both --resume and --compare are required for comparison.")
    elif not args.resume and not args.jira_url:
        # jira_url is required when not resuming or comparing
        parser.error("jira_url is required when issue_keys_file is provided.")
    
    return args

def read_issue_keys(file_path):
    try:
        with open(file_path, 'r') as file:
            issue_keys = [line.strip() for line in file if line.strip()]
        path = os.path.dirname(file_path)
        return issue_keys, path
    except Exception as e:
        print(f"Error reading issue keys file: {e}")
        sys.exit(1)

def load_csv_issue_keys(csv_path):
    """Load issue keys from the CSV file."""
    try:
        with open(csv_path, 'r') as file:
            csv_reader = csv.reader(file)
            return [row[0].strip() for row in csv_reader if row]  # Assuming issue keys are in the first column
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

def load_state_issue_keys(resume_file):
    """Load combined issue keys from a saved state JSON file."""
    try:
        with open(resume_file, 'r') as file:
            data = json.load(file)
            # Combine 'issues-left', 'issues-done', and 'issues-skipped' from the state
            issues_left = set(data.get("issues-left", []))
            issues_done = set(data.get("issues-done", {}).keys())
            issues_skipped = set(data.get("issues-skipped", []))
            return issues_left | issues_done | issues_skipped  # Union of all sets
    except Exception as e:
        print(f"Error loading state file: {e}")
        sys.exit(1)

def compare_issues(resume_file, csv_file):
    """Compare issues in resume file with those in CSV and output missing ones."""
    state_issue_keys = load_state_issue_keys(resume_file)
    csv_issue_keys = set(load_csv_issue_keys(csv_file))

    # Find missing issues in the CSV that are not in the saved state
    missing_issues = list(csv_issue_keys - state_issue_keys)

    # Output the missing issues to a JSON file
    output_path = os.path.join(os.path.dirname(csv_file), 'missing_issues.json')
    with open(output_path, 'w') as output_file:
        json.dump(missing_issues, output_file, indent=4)

    print(f"Missing issues written to {output_path}")

def main():
    args = parse_arguments()

    if args.compare:
        # Perform comparison and output missing issues
        compare_issues(args.resume, args.compare)
        return
    elif args.resume:
        path = os.path.dirname(args.resume)
        # Resume processing using the saved state
        app = JiraTagger(path=path, resume_file=args.resume)
    else:
        # Start a new session with issue keys from file
        issue_keys, path = read_issue_keys(args.issue_keys_file)
        jira_url = args.jira_url
        app = JiraTagger(path=path, issue_keys=issue_keys, jira_url=jira_url)
    app.start()

if __name__ == '__main__':
    main()
