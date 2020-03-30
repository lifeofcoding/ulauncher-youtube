import requests
import logging
import json
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)

class NpmsExtension(Extension):

    def __init__(self):
        super(NpmsExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        searchKeyword = event.get_argument()

        if not searchKeyword:
            return;

        url = 'https://api.npms.io/v2/search?q={}&size=5'.format(searchKeyword)
        logger.debug(url)

        response = requests.get(url, headers={'User-Agent' : 'ulauncher-npms'})
        data = response.json()

        items = []
        for result in data['results']:
            package = result['package']
            logger.debug(package['name'])
            items.append(ExtensionResultItem(icon='images/icon.png',
                                         name=package['name'],
                                         description=package['description'],
                                         on_enter=OpenUrlAction(package['links']['npm'])))

        return RenderResultListAction(items)

if __name__ == '__main__':
    NpmsExtension().run()
