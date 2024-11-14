# JiraTagger

An application to go through a list of issue keys and write information about them to be applied in bulk by other scripting tools.

![grafik](https://github.com/user-attachments/assets/298645fc-315d-4ba7-826d-6dc434829555)

Most of the initial code was written by ChatGPT, I just made it work so that I can go on with my task.

**This code does not follow any best-practices, the goal was to make it work quickly.**

The application assumes the Firefox Browser for proper positioning, but adding another Browser Calls to the utility would be easy, I just had no need to do it.

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
