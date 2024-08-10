import sys
import requests
import os
from dotenv import load_dotenv

WATCHED_EVENTS = ["CreateEvent", "PushEvent"]
if __name__ == "__main__":
    args = sys.argv
    load_dotenv()
    access_token = os.getenv("GH_API_KEY")

    headers = {
        "Authorization": "Bearer " + str(access_token),
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    event_data = requests.get("https://api.github.com/users/LIamB12/events", headers=headers)
    event_data = event_data.json()
    repo_changes = {}

    for event in event_data:
        if event.get("type") == "PushEvent":
            repo = event.get('repo').get('name')
            commits = event.get('payload').get('commits')
            commit_messages = []
            for commit in commits:
                commit_messages.append(commit.get("message"))
            if repo in repo_changes:
                repo_changes[repo] += commit_messages
            else:
                repo_changes[repo] = commit_messages

    for repo in repo_changes:
        print(repo + ":")
        for message in repo_changes.get(repo): 
            print("-", message)
        print("")
