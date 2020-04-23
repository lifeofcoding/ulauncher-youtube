import requests
import logging
import json
import os, sys
bspath = os.path.join(os.path.dirname(os.path.abspath(__file__)),"beautifulsoup4-4.9.0")
sys.path.append(bspath)
from bs4 import BeautifulSoup
import urllib.parse
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

class YoutubeExtension(Extension):

    def __init__(self):
        super(YoutubeExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        url = "https://youtube.com/results?search_query=" + str(encoded_search) + "&pbj=1"
        response = BeautifulSoup(requests.get(url).text, "html.parser")
        results = self.parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[:self.max_results]
        return results

    def parse_html(self, soup):
        results = []
        for video in soup.select(".yt-uix-tile-link"):
            if video["href"].startswith("/watch?v="):
                vid = video["href"][video["href"].index("=")+1:]

                video_info = {
                    "title": video["title"],
                    "link": video["href"],
                    "id": vid,
                    "thumbnail": "https://img.youtube.com/vi/" + str(vid) + "/default.jpg"
                }
                results.append(video_info)
        return results

    def to_dict(self):
        return self.videos

    def to_json(self):
        return json.dumps({"videos": self.videos})

    def on_event(self, event, extension):
        searchKeyword = event.get_argument()

        if not searchKeyword:
            return

        self.search_terms = searchKeyword
        self.max_results = 10
        self.videos = self.search()
        results = self.videos

        items = []
        for result in results:
            package = result
            logger.debug(result['title'])
            items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=package['title'],
                                         description='',
                                         on_enter=OpenUrlAction("https://youtube.com" + package['link'])))

        return RenderResultListAction(items)

if __name__ == '__main__':
    YoutubeExtension().run()
