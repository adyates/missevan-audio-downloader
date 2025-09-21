from decimal import Decimal
import os
import re
import argparse
from dotenv import load_dotenv

from missevan import MissevanAPI
from download import download_text

# Load environment variables from .env file
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Download subtitles from Missevan')
parser.add_argument('episode_id', 
                    help='The episode ID to download subtitles for (typically 7 digits long)')
args = parser.parse_args()

COOKIES = {
    "token": os.getenv("TOKEN"),
}

EPISODE_ID = args.episode_id

api = MissevanAPI(COOKIES)


subs_re = r'<d p="(\d*\.\d*),[2-9]\d*,25,.*">(.*)</d>'


def convert_to_subs(html_file, output_file):
    subs = []

    with open(html_file, 'r') as source:
        for l in source.readlines():
            match = re.search(subs_re, l)
            if match:
                timestamp = Decimal(match.group(1))
                timestamp_mod60 = divmod(timestamp, 60)
                subtitle = match.group(2)
                subs.append(
                    (timestamp, f"[{timestamp_mod60[0]}:{int(timestamp_mod60[1]):02}] {subtitle}")
                )

    subs.sort(key=lambda t:t[0])
    
    if subs:  
        with open(output_file, 'w') as target:
            target.write(os.linesep.join([s[1] for s in subs]))
        
            
def download_subs(episode, name, location):
    output_file = f"{location + name}.xml"
    print(f"Downloading {name} (ID: {episode})")

    barrage_url = api.get_barrage_url(episode)
    referrer = f"https://www.missevan.com/sound/player?id={episode}"
    download_text(barrage_url, output_file, COOKIES, referrer)

    subs_file = f"{location + name}.txt"
    convert_to_subs(output_file, subs_file)


def download_drama(episode):
    drama_name = api.get_drama_name(episode)
    print(f"Downloading {drama_name} (ID: {episode})")
    print(f"----------------------------------------")

    # Use same folder structure as main.py
    EPISODE_OUTPUT_DIRECTORY = "SavedDramas/%s/%s/"
    
    for e in api.get_episodes(episode):
        output_directory = EPISODE_OUTPUT_DIRECTORY % (drama_name, e["id"])
        os.makedirs(output_directory, exist_ok=True)
        download_subs(e["id"], e["name"], output_directory)

    print("")
    print(f"{drama_name}: Download complete.")
    print("")


print("===Missevan subs downloader===")
print("")

download_drama(EPISODE_ID)
