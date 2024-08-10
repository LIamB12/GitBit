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
    commits = []

    for event in event_data:
        if event.get("type") == "PushEvent":
            commit_messages = []
            for commit in event.get('payload').get('commits'):
                commit_messages.append(commit.get('message'))
            commit_data = {
                "repo": event.get('repo').get('name'),
                "commits": commit_messages
            }
            commits.append(commit_data)

    for commit in commits:
        print("____________________________________________________________")
        print("REPO:", commit.get('repo'))
        for message in commit.get("commits"): 
            print(message)
        print("____________________________________________________________")
