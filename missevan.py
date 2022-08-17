import json
from typing import Dict

import requests


BASE_URL = "https://www.missevan.com"


class MissevanAPI:
    def __init__(self, cookies: Dict):
        self.cookies = cookies


    def _call_web_service(self, url):
        r = requests.get(url, cookies=self.cookies)

        if not r:
            raise Exception(f"Call failed. {r}")

        return json.loads(r.text)


    def get_drama_info(self, episode_id):
        url = f"{BASE_URL}/dramaapi/getdramabysound?sound_id={episode_id}"
        drama_info = self._call_web_service(url)
        return drama_info


    def get_episodes(self, episode_id):
        info = self.get_drama_info(episode_id)
        return [
            {"id": e["sound_id"], "name": e["name"]}
            for e in info['info']['episodes']['episode']
        ]


    def get_audio_url(self, episode_id):
        url = f"{BASE_URL}/sound/getsound?soundid={episode_id}"
        episode_info = self._call_web_service(url)

        if "redirect" in episode_info["info"].keys():
            return self.get_audio_url(episode_info["info"]["redirect"])

        return episode_info['info']['sound']['soundurl']


    def get_comments_url(self, episode_id):
        return f"{BASE_URL}/site/getcomment?type=1&eId={episode_id}&order=3&p=1&pagesize=999999"
