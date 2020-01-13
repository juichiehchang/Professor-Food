import time
from gtts import gTTS
from pygame import mixer
import tempfile
import wave

class speaker():

    def __init__(self, lang = 'zh-TW'):

        self.lang = lang

    def speak(self, sentence):

        # open a temporary file to save the mp3 file
        
        with tempfile.NamedTemporaryFile(delete = True) as fp:
            tts = gTTS(text = sentence, lang = self.lang, slow=False)
            tts.save('{}.mp3'.format(fp.name))
            mixer.init(28000)
            mixer.music.load('{}.mp3'.format(fp.name))
            mixer.music.play()
            time.sleep(len(sentence)/2)
        return
