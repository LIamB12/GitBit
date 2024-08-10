import sys
import requests
import os
from dotenv import load_dotenv
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
    print(event_data)

