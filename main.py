import requests
import os
from dotenv import load_dotenv
import datetime
import sys

COMMIT_GOAL = 15
CURRENT_DATE = datetime.datetime.now()

def main():
    load_dotenv()
    access_token = os.getenv("GH_API_KEY")

    headers = {
        "Authorization": "Bearer " + str(access_token),
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    event_data = requests.get("https://api.github.com/users/LIamB12/events", headers=headers)
    event_data = event_data.json()

    calendar = {}
    for year in range(2000, int(CURRENT_DATE.year) + 1):
        calendar[year] = {}
        months = [i for i in range(1, 13)]
        days = [i for i in range(1, 32)]

        for month in months:
            calendar[year][month] = {}
            for day in days:
                calendar[year][month][day] = {}

    for event in event_data:
        if event.get("type") != "PushEvent":
            continue

        date_string = event.get("created_at").split("T")[0]
        event_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        current_date_changes = calendar[event_date.year][event_date.month][event_date.day]


        repo = event.get('repo').get('name')
        commits = event.get('payload').get('commits')
        commit_messages = []

        for commit in commits:
            commit_messages.append(commit.get("message"))
        if repo in current_date_changes:
            current_date_changes[repo] += commit_messages
        else:
            current_date_changes[repo] = commit_messages

    current_day_commit_count = 0
    current_date = CURRENT_DATE
    if len(sys.argv) > 1:
        try:
            current_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d")
        except:
            print("Usage: python3 main.py [YYYY-MM-DD]")
            return
            

    for repo in calendar[current_date.year][current_date.month][current_date.day]:
        print(repo + ":\n")

        for commit_message in calendar[current_date.year][current_date.month][current_date.day][repo]:
            print("-", commit_message)
            current_day_commit_count += 1
        print("")

    print(current_day_commit_count, "/", COMMIT_GOAL, "Commits Today!")

if __name__ == "__main__":
    main()





