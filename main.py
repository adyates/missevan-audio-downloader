import argparse
import os

from dotenv import load_dotenv

from download import download_binary, download_text
from missevan import MissevanAPI

# Load environment variables from .env file
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description="Download audio episodes from Missevan")
parser.add_argument(
    "episode_id", help="The episode ID to download (typically 7 digits long)"
)
args = parser.parse_args()


def parse_cookie_file(filename):
    """Parse cookie file and return a cookies dictionary with URL-decoded values"""
    import urllib.parse

    cookies = {}
    try:
        with open(filename, "r") as f:
            cookie_string = f.read().strip()
            # Split by semicolon and parse each cookie
            for cookie in cookie_string.split(";"):
                if "=" in cookie:
                    key, value = cookie.strip().split("=", 1)
                    # URL decode the value
                    decoded_value = urllib.parse.unquote(value)
                    cookies[key] = decoded_value
        return cookies
    except FileNotFoundError:
        return None


# Try to load cookies from cookie_copy file, fallback to environment variable
COOKIES = parse_cookie_file("cookie_copy")
if COOKIES is None:
    COOKIES = {
        "token": os.getenv("TOKEN"),
    }
    print("Using token from environment variable")
else:
    print("Using cookies from cookie_copy file")

EPISODE_ID = args.episode_id

print(COOKIES)
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
        "filename": e["name"] + ".m4a",
    }
    for e in episode_list
]

# Filter all audio files without a url
valid_audio_urls = [a for a in audio_urls if a["url"]]
invalid_audio_urls = [a for a in audio_urls if not a["url"]]

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
        output_directory = EPISODE_OUTPUT_DIRECTORY % (
            drama_name,
            a["id"],
        )
        os.makedirs(output_directory, exist_ok=True)

        referrer = f"https://www.missevan.com/sound/player?id={a['id']}"
        download_binary(a["url"], output_directory + a["filename"], COOKIES, referrer)
    except e:
        print(f"[ERROR] {e}")


print("==============================")
print("Downloads complete.")
