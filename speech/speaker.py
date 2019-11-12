import time
from gtts import gTTS
from pygame import mixer
import tempfile

class speaker():

    def __init__(self, lang = 'zh-TW'):

        self.lang = lang

    def speak(self, sentence):
        with tempfile.NamedTemporaryFile(delete = True) as fp:
            tts = gTTS(text = sentence, lang = self.lang)
            tts.save('{}.mp3'.format(fp.name))
            mixer.init()
            mixer.music.load('{}.mp3'.format(fp.name))
            mixer.music.play()
            time.sleep(len(sentence)/2)
        return
