import requests
import json
import os

url = "https://discord.com/api/v10/applications/1019903151639384084/commands"
headers = {
    "Authorization": "Bot MTAxOTkwMzE1MTYzOTM4NDA4NA.GLSkf_.qo4lnsHgD8oEsKG_wfylqe9UW1mzCJ1o-Us3RE"
}

os.chdir("cogs")
for f in os.listdir("."):
    if f.endswith(".json"):
        json_file = json.load(open(f))
        for c in json_file["commands"]:
            r = requests.post(url, headers=headers, json=c)
            print(f, ":", r)
