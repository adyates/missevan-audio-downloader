import shutil

import requests
from missevan import MissevanAPI


def download_text(url, filename, cookies={}, referrer=None):
    api = MissevanAPI(cookies)
    headers = api._get_headers(referrer)
    
    response = requests.get(url, headers=headers, cookies=cookies)
    if not response:
        print("ERROR")
        print(response.text)
        return

    with open(filename, 'w') as f:
        f.write(response.text)


def download_binary(url, filename, cookies={}, referrer=None):
    api = MissevanAPI(cookies)
    headers = api._get_headers(referrer)
    
    response = requests.get(url, stream=True, headers=headers, cookies=cookies)
    if not response:
        raise Exception('[ERROR] Failed to download from {url}')

    with open(filename, 'wb') as f:
        shutil.copyfileobj(response.raw, f)
