import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.config import Config
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.core.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import mainthread
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from os import path
from kivy.uix.scatter import Scatter
import cv2
import time
import argparse 
import os
import io
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.cloud import texttospeech_v1
from google.cloud.texttospeech_v1.services import text_to_speech
from google.cloud.texttospeech_v1.types.cloud_tts import SsmlVoiceGender, Voice
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from google.cloud import translate
from imutils.object_detection import non_max_suppression
import numpy as np
import time
import cv2
from kivy.properties import DictProperty 
import six
from google.cloud import translate_v2 as translate
from kivy.clock import Clock
from pathlib import Path
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView 


dir_path = os.path.dirname(os.path.realpath(__file__))




os.environ['GOOGLE_APPLICATION_CREDENTIALS']= r'new.json'
Config.set('graphics', 'resizable', False)
Config.set('graphics','width', '360')
Config.set('graphics', 'height', '540')



class MyMainApp(BoxLayout):
    pass


class MainWindow(Screen):
    pass


class BoxyLayout(BoxLayout):
    pass


class AnchorLayout(AnchorLayout):
    pass


target = ''


class SecondWindow(Screen):

    def spinner_clicked(self, text):
        global target
        print("Text value" + text)
        languagechoice = text
        
        print("This is the language coming from the app" + languagechoice)
        Dict = {"Language":"en", "English": "en", "Afrikaans": "af", "Arabic": "ar", "Bengali": "bn",
                "Bulgarian": "bg", "Catalan": "ca", "Czech": "cs", "Danish": "da", "Dutch": "nl",
                "English": "en", "French": "fr", "German": "de", "Greek": "el", "Gujarati": "gu",
                "Hindi": "hi", "Hungarian": "hu", "Icelandic": "is", "Indonesian": "id",
                "Italian": "it", "Japanese": "ja", "Kannada": "kn",
                "Korean": "ko", "Latvian": "lv", "Malay": "ms", "Malayalam": "ml",
                "Mandarin": "zh", "Norwegian": "no", "Polish": "pl", "Portuguese": "pt",
                "Punjabi": "pa", "Romanian": "ro", "Russian": "ru", "Serbian": "sr",
                "Slovak": "sk", "Spanish": "es", "Swedish": "sv", "Tamil": "ta", "Telugu": "te",
                "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Vietnamese": "vi"}
       
        target = Dict[languagechoice]
        print("Desired language is " + languagechoice +
              ". Lang Code is " + target)

        return target

    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png("img.png")
        print("Captured")

    def imageToAudio(self):
        infile = "img.png"
        outfile = "output.mp3"
        text_to_speak = detectText(infile)
        text_to_speech(text_to_speak, outfile)

    def play_sound(self):
        sound = SoundLoader.load('output.mp3')
        if sound:
            sound.play()


class ThirdWindow(Screen): 
    
    message = StringProperty()

    def retranslate(self, language):
        texts = {"en": "Hello World", "fr": "Salut monde"}
        self.message = texts.get(language, "")

    def on_pre_enter(self):
        self.showtext()
        self.ids.scrollview.scroll_y = 1
        
    def showtext(self):
        with open("transtext.txt","r", encoding="utf-8") as f:
            self.ids['_label'].text = f.read()
        self.ids.scrollview.scroll_y = 1

    def play_sound(self):
        sound = SoundLoader.load('output.mp3')
        if sound:
            sound.play()
    def stop_sound(self):
        sound = SoundLoader.load('output.mp3')
        if sound: 
            sound.stop()
    
    with open('transtext.txt', 'w', encoding="utf-8") as f: 
        f.write('Welcome')
        f.close()
 
    show = open(r"transtext.txt","r", encoding="utf-8") 
    fileoutput = StringProperty(show.read(), encoding="utf-8")
    show.close()
    
        
class WindowManager(ScreenManager):
    pass


class MyLayout(Widget):
    pass


class MyGrid(Widget):
    pass


class CheckScreen(Screen):
    pass


class SoundPlayer(BoxLayout):
    def play_sound(self):
        sound = SoundLoader.load('output.mp3')
        if sound:
            sound.play()


class CameraClick(BoxLayout):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        camera.export_to_png("img.png")
        print("Captured")


class MyMainApp(App):
    def build(self):
        return ThirdWindow()
    def build(self):
        return kv
    Window.clearcolor = (0, 0, 0, 1)
     


def detectText(infile):
    global target
    client = vision_v1.ImageAnnotatorClient()

    with io.open(infile, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)

    response = client.text_detection(image=image)
    text = response.full_text_annotation.text
    print("Detected text: {}".format(text))

    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    result = translate_client.detect_language(text)

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)

    
    
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(
        result["detectedSourceLanguage"]))

    text = format(result["translatedText"])
    with open('transtext.txt', 'w', encoding="utf-8") as f:
        f.write(text)
        f.close() 
           
    return text
  



def text_to_speech(text, outfile):
    """Synthesizes speech from the input file of text."""
    global target
    client = texttospeech_v1.TextToSpeechClient()

    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=target, ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3)

    request = texttospeech_v1.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice, audio_config=audio_config)

    response = client.synthesize_speech(request=request)

    # The response's audio_content is binary.

    with open(outfile, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file ' + outfile)
    
        
class ImageToAudio:
    def imageToAudio():
        infile = "img.png"
        outfile = "output.mp3"
        text_to_speak = detectText(infile)
        text_to_speech(text_to_speak, outfile)


def main():
    infile = "img.png"
    outfile = "output.mp3"
    text_to_speak = detectText(infile)
    text_to_speech(text_to_speak, outfile)


kv = Builder.load_file("my.kv")

if __name__ == '__main__':
    MyMainApp().run()
    main()