import os
import re

from missevan import MissevanAPI
from download import download_text


EPISODE_ID_LIST = [
    "<TODO: Insert the episode number here (likely 7 digits long)>",
    "<TODO: And another. One per drama you want to download.>",
    "etc.",
]

api = MissevanAPI()


subs_re = r'<d p="\d*\.\d*,4,25,.*">(.*)</d>'


def convert_to_subs(html_file, output_file):
    with open(html_file, 'r') as source:
        with open(output_file, 'w') as target:
            lines = source.readlines()
            for l in lines:
                match = re.search(subs_re, l)
                if match:
                    target.write(match.group(1) + os.linesep)
        
            
def download_subs(episode, name, location):
    output_file = f"{location}/{name}.html"
    print(f"Downloading {name} (ID: {episode})")

    barrage_url = api.get_barrage_url(episode)
    download_text(barrage_url, output_file)

    subs_file = f"{location}/{name}.txt"
    convert_to_subs(output_file, subs_file)


def download_drama(episode):
    drama_name = api.get_drama_name(episode)
    print(f"Downloading {drama_name} (ID: {episode})")
    print(f"----------------------------------------")

    output_dir = f"./{drama_name}"
    os.makedirs(output_dir, exist_ok=True)

    for e in api.get_episodes(episode):
        download_subs(e["id"], e["name"], output_dir)

    print("")
    print(f"{drama_name}: Download complete.")
    print("")


print("===Missevan subs downloader===")
print("")

for episode in EPISODE_ID_LIST:
    download_drama(episode)
    print(api.get_drama_name(episode))