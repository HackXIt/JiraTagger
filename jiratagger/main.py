from jiratagger.app.jira_tagger import JiraTagger
import argparse
import sys
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='JiraTagger - Label Jira issues with tags and comments.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('issue_keys_file', nargs='?', help='Path to the file containing Jira issue keys.')
    group.add_argument('--resume', help='Resume from a saved state file.')
    parser.add_argument('jira_url', nargs='?', help='Base URL of the Jira instance.')
    args = parser.parse_args()

    if not args.resume and not args.jira_url:
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

def main():
    args = parse_arguments()
    if args.resume:
        app = JiraTagger(resume_file=args.resume)
    else:
        issue_keys, path = read_issue_keys(args.issue_keys_file)
        jira_url = args.jira_url
        app = JiraTagger(path=path, issue_keys=issue_keys, jira_url=jira_url)
    app.start()

if __name__ == '__main__':
    main()
