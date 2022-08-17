import shutil

import requests


def download_text(url, filename, cookies={}):
    response = requests.get(url)
    if not response:
        print("ERROR")
        print(response.text)
        return

    with open(filename, 'w') as f:
        f.write(response.text)


def download_binary(url, filename, cookies={}):
    response = requests.get(url, stream=True, cookies=cookies)
    if not response:
        raise Exception('[ERROR] Failed to download from {url}')

    with open(filename, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
