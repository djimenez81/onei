# File name: interface.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import  AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory
from kivy.uix.filechooser import FileChooserIconLayout
from kivy.uix.filechooser import FileChooserListLayout

Builder.load_file('menu.kv')
Builder.load_file('file.kv')

class Interface(AnchorLayout):
    pass

#class Interface(AnchorLayout):
 #  pass
#class Files(BoxLayout):
 #   pass
    #load = ObjectProperty(None)
    #cancel = ObjectProperty(None)

#class Interface(FileChooserListLayout):
 #   pass

class InterfaceApp(App):
    def build(self):
        return Interface()

#Factory.register('Root', cls=Root)
#Factory.register('Files', cls=Files)

if __name__=="__main__":
    InterfaceApp().run()