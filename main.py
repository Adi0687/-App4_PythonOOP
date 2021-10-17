from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import time
import webbrowser
from filesharer import FileSharer

# Connect the Python File to the kv file
Builder.load_file('frontend.kv')


# Requirement from kivy, this is for the first window ImageScreen
# Every Screen needs a class
# The WebCam Class
class CameraScreen(Screen):
    def start(self):
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        # Trick of Kivy to set Texture back (._camera.texture)
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera.texture = None

    def capture(self):
        current_time = time.strftime('%Y%m%d-%H%M%S')
        self.filepath = f"images/{current_time}.png"
        self.ids.camera.export_to_png(self.filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filepath


# Requirement from kivy, this is for the second window ImageScreen
class ImageScreen(Screen):
    # link_message is a Class Variable, because it is not defined in the init class
    link_message = "Create a Link First Brov!!"

    def create_link(self):
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        fileshare = FileSharer(filepath=file_path)
        self.url = fileshare.share()
        self.ids.link.text = self.url

    def copy_link(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message


# Class that inherits from ScreenManager Class
# Requirement from kivy
class RootWidget(ScreenManager):
    pass


# Requirement from kivy
class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
