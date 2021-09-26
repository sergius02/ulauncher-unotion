from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from UNotion import UNotion


class NotionNotes(Extension):
    UNOTION = None

    def __init__(self):
        super(NotionNotes, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        if not extension.UNOTION:
            extension.UNOTION = UNotion(extension.preferences.get("notion_token"))

        for database in extension.UNOTION.get_databases_linked():
            if database["object"] == "database":
                item_name = database["title"][0]["text"]["content"]
                data = {
                    'note': event.get_argument(),
                    'database_id': database["id"]
                }
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name='%s' % item_name,
                                                 description='Add this note to %s' % item_name,
                                                 on_enter=ExtensionCustomAction(data)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([
            ExtensionResultItem(on_enter=extension.UNOTION.upload_to_notion(data['database_id'], data['note']))
        ])


if __name__ == '__main__':
    NotionNotes().run()
