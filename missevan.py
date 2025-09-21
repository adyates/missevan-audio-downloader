import json
from typing import Dict

import requests


BASE_URL = "https://www.missevan.com"


class MissevanAPI:
    def __init__(self, cookies: Dict = {}):
        self.cookies = cookies

    def _get_headers(self, referrer=None):
        """Get headers with optional custom referrer"""
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        
        if referrer:
            headers['referer'] = referrer
        else:
            headers['referer'] = 'https://www.missevan.com/sound/player'
            
        return headers

    def _call_web_service(self, url, referrer=None):
        headers = self._get_headers(referrer)
        r = requests.get(url, headers=headers, cookies=self.cookies)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception(f"Call failed for {url}: {r.text}")

    def get_drama_info(self, episode_id):
        url = f"{BASE_URL}/dramaapi/getdramabysound?sound_id={episode_id}"
        referrer = f"https://www.missevan.com/sound/player?id={episode_id}"
        drama_info = self._call_web_service(url, referrer)
        return drama_info

    def get_drama_name(self, episode_id):
        info = self.get_drama_info(episode_id)
        return info['info']['drama']['name']

    def get_episodes(self, episode_id):
        info = self.get_drama_info(episode_id)
        return [
            {"id": e["sound_id"], "name": e["name"]}
            for e in info['info']['episodes']['episode']
        ]

    def get_audio_url(self, episode_id):
        url = f"{BASE_URL}/sound/getsound?soundid={episode_id}"
        referrer = f"https://www.missevan.com/sound/player?id={episode_id}"
        episode_info = self._call_web_service(url, referrer)

        if "redirect" in episode_info["info"].keys():
            return self.get_audio_url(episode_info["info"]["redirect"])

        info_block = episode_info.get('info', {})
        sound_block = info_block.get('sound', {})
        sound_url = sound_block.get('soundurl', None)
        return sound_url

    def get_barrage_url(self, episode_id):
        return f"{BASE_URL}/sound/getdm?soundid={episode_id}"

    def get_comments_url(self, episode_id):
        return f"{BASE_URL}/site/getcomment?type=1&eId={episode_id}&order=3&p=1&pagesize=999999"
    