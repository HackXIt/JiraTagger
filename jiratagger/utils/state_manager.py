import json
import os
from datetime import datetime

class StateManager:
    state_jira_url = "jira-url"
    state_issue_keys = "issues-left"
    state_results = "issues-done"
    state_issues_skipped = "issues-skipped"
    state_tag_hints = "tag-hints"
    def __init__(self, path, issue_keys, resume_file):
        self.issue_keys = issue_keys or []
        self.results = {}
        self.issues_skipped = []
        self.tag_hints = set()
        self.current_index = 0
        self.state_file = resume_file or os.path.join(path, 'jira_tagger_state.json')

        if resume_file:
            self.load_state()

    def save_state(self):
        # Print timestamp and sanity message to console
        print(f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} Saving state to {self.state_file}")
        # Do not remove issues that are currently processed on manual save
        adjusted_index = self.current_index - 1 if self.issue_keys[self.current_index] not in self.results.keys() else self.current_index
        data = {
            self.state_jira_url: self.jira_url,
            self.state_issue_keys: self.issue_keys[adjusted_index:],
            self.state_results: self.results,
            self.state_issues_skipped: self.issues_skipped,
            self.state_tag_hints: list(self.tag_hints)
        }
        with open(self.state_file, 'w') as file:
            json.dump(data, file, indent=4)

    def load_state(self):
        with open(self.state_file, 'r') as file:
            data = json.load(file)
            self.jira_url = data[self.state_jira_url]
            self.issue_keys = data[self.state_issue_keys]
            self.results = data[self.state_results]
            self.issues_skipped = data[self.state_issues_skipped]
            self.tag_hints = set(data[self.state_tag_hints])

    def export_results(self):
        with open('jira_tagger_results.json', 'w') as file:
            json.dump(self.results, file, indent=4)

    def get_next_issue(self):
        if self.current_index >= len(self.issue_keys):
            return None
        issue_key = self.issue_keys[self.current_index]
        self.current_index += 1
        return issue_key

    def add_result(self, issue_key, tags, comment):
        self.results[issue_key] = {"tags": list(tags), "comment": comment}
        self.tag_hints.update(tags)
        self.save_state()

    def skip_issue(self, issue_key):
        self.issues_skipped.append(issue_key)

    def get_remaining_issues_count(self):
        return len(self.issue_keys) - self.current_index
    
    def get_done_issues_count(self):
        return len(self.results)
    
    def get_skipped_issues_count(self):
        return len(self.issues_skipped)
