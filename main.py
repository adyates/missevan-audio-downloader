from missevan import MissevanAPI
from download import download_binary, download_text


COOKIES = {
    "token": "<TODO: Insert your token here>",
}

EPISODE_ID = "<TODO: Insert the episode number here (likely 7 digits long)>"


api = MissevanAPI(COOKIES)

print("===Missevan site ripper===")
print("")


print("Episode list to process")
print("-----------------------")

episode_list = api.get_episodes(EPISODE_ID)

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

for a in audio_urls:
    print(f"{a['name']} ({a['id']}): {a['url']}")


comments_urls = [
    {
        "id": e["id"],
        "name": e["name"],
        "url": api.get_comments_url(e["id"]),
        "filename": e["name"]+ ".json",
    }
    for e in episode_list
]


print("Starting downloads")
print("------------------")
for a in audio_urls:
    print(f"Downloading {a['filename']}")
    try:
        download_binary(a["url"], a["filename"], COOKIES)
    except e:
        print(f"[ERROR] {e}")

for c in comments_urls:
    print(f"Downloading {c['filename']}")
    try:
        download_text(c["url"], c["filename"], COOKIES)
    except e:
        print(f"[ERROR] {e}")


print("==============================")
print("Downloads complete.")
