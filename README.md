# JiraTagger

An application to go through a list of issue keys and write information about them to be applied in bulk by other scripting tools.

![grafik](https://github.com/user-attachments/assets/298645fc-315d-4ba7-826d-6dc434829555)

Most of the initial code was written by ChatGPT, I just made it work afterwards so that I can go on with my task.

**This code does not follow any best-practices, the goal was to make it work quickly. I tried to keep it somewhat organized, but this was done in quite a rush and might contain a few quirks.**

The application assumes the Firefox Browser for proper positioning, but adding [another Browser Class](https://github.com/HackXIt/JiraTagger/blob/3f758ded4dde9329adf5a3f7e79869c8266e1f81/jiratagger/utils/browser_utils.py#L11) to the utility would be easy, I just had no need to do it.

## Context and Scope

I created this application, because we had a huge migration **(about 890 issues)** of manual test cases which needed to be reviewed for test automation.

Since clicking through the Jira UI is very cumbersome for such a bulk review task, I created this tool to make it easier and efficient.

The goal was not to perform the bulk-edit itself, since there already are tools or scripting possibilities _(Jira API)_ for that, but to make the review process easier and more streamlined.

Our review process was mainly concerned with labeling test cases for their automatability and writing a comment for the manual testers on what will be automated/changed.

So, in that regard, there are no features beyond that. The tool is very simple and straightforward.

## Features

- [x] Loads a list of Jira issue keys from a text file
- [x] Accepts a Jira instance URL to use for browsing the issues
- [x] Opens a new tab for each issue key in sequence of the review process (i.e. only one issue key at a time)
- [x] Allows the user to write information about the issue (i.e. labels to give, comments to write, etc.)
- [x] Allows the user to either submit their information or skip the issue
- [x] Saves the information into a dictionary format to be used in further processing (i.e. Jira API calls / bulk update)
- [x] Allows the user to export the information to a file
- [x] Allows to user to halt the process and resume where they left off at a later time (i.e. save the state to a file and load it back up)
- [x] Adjust window position to the browser window which opened the JIRA issue **(Firefox only)**
- [x] Shortcuts to apply minimal Markdown Formatting of Jira in the Comment Field _(Bold, Italic, Underline, Link, Color)_
- [x] Compare state file with list of issue-keys to determine missing issues in the state file.
- [x] Paste UTF-8 encoded text into comment window and decode it for the view, to be able to copy-paste from previous comments in the state file.
- [x] Statistics about the process (Issues left, issues skipped, issues done, Time Estimate for issue list based on current session performance (i.e. AVG of time-taken per issue in current session))
- [x] Application and issue window will always stay on top, unless minimized. _(There's a lot of unnecessary details in the right side-bar of Jira, so that's where I decided to position the application)_

## How to run

You need [`poetry`](https://python-poetry.org/docs/) to run this application and somewhat of a modern python version, since who knows what these dependencies require. 

The application was used and interactively tested with `python 3.12`, so your mileage and success with the application may vary, if you use something different.

I set the python restrictions to `>=3.8,<3.14`, so it should work for the most part, but compatibility or runtime issues might still exist with other python versions.

Before you start, you need to clone the repository. _Leave a star while you're at it, which lets me know someone uses this and might incentivize me to improve it._
```shell
git clone https://github.com/HackXIt/JiraTagger.git
```

First, install the virtual environment:
```shell
poetry install
```

Then activate the environment:

_(requires `venv` installation in project directory setting applied in `poetry`, otherwise you need to figure out the .venv path yourself or use a poetry command)_
```shell
.venv/Scripts/activate # Linux
.\.venv\Scripts\activate.ps1 # Windows
# Optional to run without activating .venv
poetry run ...
```

Afterwards, the application should be available:
```shell
# (...) indicates your shell has activated the .venv
(jiratagger-py3.12) > jiratagger -h
usage: jiratagger [-h] [--resume JSON_FILE] [--compare CSV_FILE] [issue_keys_file] [jira_url]

JiraTagger - Label Jira issues with tags and comments or compare saved state.

positional arguments:
  issue_keys_file     Path to the file containing Jira issue keys.
  jira_url            Base URL of the Jira instance.

options:
  -h, --help          show this help message and exit
  --resume JSON_FILE  Resume from a saved state file.
  --compare CSV_FILE  Compare a saved state file with a CSV to find missing issues.

# Alternative
poetry run jiratagger -h
```

## Practice

I found it helps to use Notepad++ to have the `jira_tagger_state.json` open while editing. Notepad++ does not interfer (no file lockings or similar) and also automatically asks for a reload of the file if something changes.

That way I can copy the comment text of previous issues and paste it in the comment field. The unicode encoding is automatically handled when done so.

If you edit the state file while using the application, your changes will be overwritten **without intervention.**

To change the state file manually, just exit the application, make your changes, reload from the resume file. Python errors may arise if you write typos or syntax errors.

This is useful to know, since if you later want to add a bunch of issues to the state file (i.e. `issues-left`), you can first compare against the list of issues and then copy/paste from the `missing_issues.json`.

I am well aware that all of this could be in the application, but as already stated, this is such a one-off project that nobody probably cares.

## Notes

I tried creating this application as a browser extension as well but utterly failed at the attempt.

All of this would be much nicer in a browser extension which adds a sidebar to browser window.

I have never written a browser extension and I had no time to do so on the fly. I tried with ChatGPT and decided it was a failure _(garbage-in garbage-out)_, without me learning the ropes of what is necessary.
