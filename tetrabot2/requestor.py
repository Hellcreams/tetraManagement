import requests
import json
import os

url = "https://discord.com/api/v10/applications/1019903151639384084/commands"

# Read Token
file_name = "token.man"
with open(file_name, 'r', encoding="utf-8") as file:
    TOKEN = file.read()
headers = {
    "Authorization": "Bot " + TOKEN
}

os.chdir("cogs")
for f in os.listdir("."):
    if f.endswith(".json"):
        json_file = json.load(open(f))
        for c in json_file["commands"]:
            r = requests.post(url, headers=headers, json=c)
            print(f, ":", r)
