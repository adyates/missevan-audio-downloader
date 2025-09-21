import os
import argparse
from dotenv import load_dotenv
from missevan import MissevanAPI
from download import download_binary, download_text


# Load environment variables from .env file
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description='Download audio episodes from Missevan')
parser.add_argument('episode_id', 
                    help='The episode ID to download (typically 7 digits long)')
args = parser.parse_args()

COOKIES = {
    "token": os.getenv("TOKEN"),
}

EPISODE_ID = args.episode_id


api = MissevanAPI(COOKIES)

print("===Missevan site ripper===")
print("")


print("Episode list to process")
print("-----------------------")

episode_list = api.get_episodes(EPISODE_ID)
drama_name = api.get_drama_name(EPISODE_ID)

for e in episode_list:
    print(f"{e['id']}: {e['name']}")


print("")
print("Audio URLs (may take a moment)")
print("------------------------------")

audio_urls = [
    {
        "id": e["id"],
        "name": e["name"],
        "url": api.get_audio_url(e["id"]),
        "filename": e["name"]+ ".m4a",
    }
    for e in episode_list
]

# Filter all audio files without a url
valid_audio_urls = [a for a in audio_urls if a['url']]
invalid_audio_urls = [a for a in audio_urls if not a['url']]

print("\nSkipping the following audio files:")
print("--------------------------------")
for a in invalid_audio_urls:
    print(f"{a['name']} ({a['id']}): {a['url']}")

print("\nDownloading the following audio files:")
print("--------------------------------")
for a in valid_audio_urls:
    print(f"{a['name']} ({a['id']}): {a['url']}")

# Download all of the audio files to the output directory of
EPISODE_OUTPUT_DIRECTORY = "SavedDramas/%s/%s/"

print("Starting downloads")
print("------------------")
for a in valid_audio_urls:
    print(f"Downloading {a['filename']}")
    try:
        output_directory = EPISODE_OUTPUT_DIRECTORY % (drama_name, a["id"],)
        os.makedirs(output_directory, exist_ok=True)

        referrer = f"https://www.missevan.com/sound/player?id={a['id']}"
        download_binary(a["url"], output_directory + a["filename"], COOKIES, referrer)
    except e:
        print(f"[ERROR] {e}")


print("==============================")
print("Downloads complete.")
