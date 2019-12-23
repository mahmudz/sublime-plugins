import sublime
import sublime_plugin
import re

class SnakeCaseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            selectionText = self.view.substr(region)
            self.view.replace(edit, region, self.convert(selectionText))

    def convert(self, text):
        text = text.replace("'", '')
        text = text.replace('"', '')
        return re.sub(r'[\W_]+', '_', text).lower()
