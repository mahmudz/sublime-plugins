import sublime
import sublime_plugin

class ReplaceNewViewTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, text, start_index, end_index):
        self.view.replace(edit, sublime.Region(start_index, end_index), text)