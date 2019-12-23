import sublime
import sublime_plugin
import re

class GenerateTranslationsCommand(sublime_plugin.TextCommand):
    pattern = r'(trans(?:_choice)?|Lang::(?:get|choice|trans(?:Choice)?)|@(?:lang|choice)|(__))\(([\'"]([^\'"]+)[\'"])[)\]];?'

    #__\(([\'"]([^\'"]+)[\'"])[)\]];?       :Extract transltion methods
    # {{ __[^)]*
    def run(self, view):
        selection = self.view.sel()
        for region in selection:
            selectionText = self.view.substr(region)
            match = re.findall(r'(trans(?:_choice)?|Lang::(?:get|choice|trans(?:Choice)?)|@(?:lang|choice)|(__))\(([\'"]([^\'"]+)[\'"])[)\]];?', selectionText)
            translations = "" 
            for x in match:
                translations += '{0} => {1},\n'.format(x[3], x[3])
            print(translations)
    
    def scan(self):
        pass

    def export(self, text):
        view = self.view.window().new_file()
        view.run_command('requester_replace_view_text',
                         {'text': text, 'point': 0})

class TransCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        for region in selection:
            selectionText = self.view.substr(region)
            self.view.replace(edit, region, self.convert(selectionText))

    def convert(self, text):
        text = text.replace("'", '')
        text = text.replace('"', '')
        return "{{ __('translations." + re.sub(r'[\W_]+', '_', text).lower() + "') }}"


class AssetingSourceCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        def on_done(input_string):
            self.view.run_command( 'asseting_source_helper', { 'location' : input_string } )

        def on_change(input_string):
            pass

        def on_cancel():
            print("User cancelled the input")
                    
        window = self.view.window()
        window.show_input_panel("Text to Insert:", "", on_done, on_change, on_cancel)       
    

class AssetingSourceHelperCommand(sublime_plugin.TextCommand):
    def run(self, edit, location = ''):
        reg = sublime.Region(0, self.view.size())
        content = self.view.substr(reg)
        
        links = re.findall(r'<link\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1', content)
        for link in links:
          content = content.replace(link[1], "{{ asset('" + location + "/" + link[1] +"') }}")

        links = re.findall(r'<script\s+(?:[^>]*?\s+)?src=(["\'])(.*?)\1', content)
        for link in links:
          content = content.replace(link[1], "{{ asset('" + location + "/" + link[1] +"') }}")

        links = re.findall(r"\<img.+src\=(?:\"|\')(.+?)(?:\"|\')(?:.+?)\>", content)
        for link in links:
          content = content.replace(link, "{{ asset('" + location + "/" + link +"') }}")

        content = content.replace("{{ asset('"+location+"/{{", "{{")
        content = content.replace("}}') }}", "}}")
        content = content.replace("{{ asset('"+location+"/{{ asset('"+location+"/{{", "{{")
        content = content.replace("}}') }}') }}", "}}")              
        
        self.view.erase(edit, reg)
        self.view.insert(edit, 0, content)