import json
import os
from datetime import datetime

class StateManager:
    state_jira_url = "jira-url"
    state_issues_left = "issues-left"
    state_results = "issues-done"
    state_issues_skipped = "issues-skipped"
    state_tag_hints = "tag-hints"
    def __init__(self, path, issues_left, jira_url, resume_file):
        self.jira_url = jira_url
        self.issues_left = issues_left or []
        self.results = {}
        self.issues_skipped = []
        self.tag_hints = set()
        self.current_issue = None
        self.state_file = resume_file or os.path.join(path, 'jira_tagger_state.json')
        self.results_file = os.path.join(path, 'jira_tagger_results.json')

        if resume_file:
            self.load_state()

    def save_state(self):
        # Print timestamp and sanity message to console
        print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Saving state to {self.state_file}")
        # Do not remove issues that are currently being processed on manual save
        if self.current_issue and self.current_issue not in self.results.keys() and self.current_issue not in self.issues_skipped:
            print("Re-inserting current issue into issues left list")
            self.issues_left.insert(0, self.current_issue)
        sorted_issues_left = sorted(self.issues_left, key=lambda x: int(x.split('-')[1]), reverse=True)
        sorted_results = dict(sorted(self.results.items(), key=lambda x: int(x[0].split('-')[1]), reverse=True))
        data = {
            self.state_jira_url: self.jira_url,
            self.state_issues_left: sorted_issues_left,
            self.state_results: sorted_results,
            self.state_issues_skipped: self.issues_skipped,
            self.state_tag_hints: list(self.tag_hints)
        }
        with open(self.state_file, 'w') as file:
            json.dump(data, file, indent=4)

    def load_state(self):
        with open(self.state_file, 'r') as file:
            data = json.load(file)
            self.jira_url = data[self.state_jira_url]
            self.issues_left = data[self.state_issues_left]
            self.results = data[self.state_results]
            self.issues_skipped = data[self.state_issues_skipped]
            self.tag_hints = set(data[self.state_tag_hints])
        print(f"Loaded state from {self.state_file}: {len(self.issues_left)} issues left, {len(self.results)} issues done, {len(self.issues_skipped)} issues skipped")

    def export_results(self):
        with open(self.results_file, 'w') as file:
            json.dump(self.results, file, indent=4)

    def get_next_issue(self):
        self.current_issue = self.issues_left.pop(0) if self.issues_left else None
        if not self.current_issue:
            print("All issues processed.")
            return None
        print(f"Processing issue {self.current_issue} ({self.remaining_issues_count()} left)")
        return self.current_issue

    def add_result(self, issue_key, tags, comment):
        self.results[issue_key] = {"tags": list(tags), "comment": comment}
        self.tag_hints.update(tags)
        self.issues_left.remove(issue_key)
        self.save_state()

    def skip_issue(self):
        print(f"Skipping issue {self.current_issue}")
        self.issues_skipped.append(self.current_issue)
        if self.current_issue in self.issues_left:
            self.issues_left.remove(self.current_issue)

    def remaining_issues_count(self):
        return len(self.issues_left)
    
    def done_issues_count(self):
        return len(self.results)
    
    def skipped_issues_count(self):
        return len(self.issues_skipped)
