# JiraTagger

An application to go through a list of issue keys and write information about them to be applied in bulk by other scripting tools.

I started out with `tkinter`, gave up and then switched to a browser extension.

Most of this code was written by ChatGPT, I just made it work so that I can go on with my task.

## Context and Scope

I created this application, because we had a huge migration **(about 884 issues)** of manual test cases which needed to be reviewed for test automation.

Since clicking through the Jira UI is very cumbersome for such a bulk review task, I created this tool to make it easier and efficient.

The goal was not to perform the bulk-edit itself, since there already are tools or scripting possibilities for that, but to make the review process easier and more streamlined.

Our review process was mainly concerned with labeling test cases for their automatability and writing a comment for the manual testers on what will be automated/changed.

So, in that regard, there are no features beyond that. The tool is very simple and straightforward.

## Roadmap

- [ ] Loads a list of Jira issue keys from a text file
- [ ] Accepts a Jira instance URL to use for browsing the issues
- [ ] Opens a new tab for each issue key in sequence of the review process (i.e. only one issue key at a time)
- [ ] Allows the user to write information about the issue (i.e. labels to give, comments to write, etc.)
- [ ] Allows the user to either submit their information or skip the issue
- [ ] Saves the information into a dictionary format to be used in further processing (i.e. Jira API calls / bulk update)
- [ ] Allows the user to export the information to a file
- [ ] Allows to user to halt the process and resume where they left off at a later time (i.e. save the state to a file and load it back up)
