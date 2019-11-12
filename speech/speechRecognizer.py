import pyaudio
import wave
import speech_recognition as sr
import datetime
from collections import deque
import math
import audioop
import os
from chinese import ChineseAnalyzer

OUTPUT_DIR = "./results/"
time_string = "_{:D%Y%m%dT%H%M%S}".format(datetime.datetime.now())

recording_seconds = 5
audio_filename = OUTPUT_DIR + "record.wav"


# Microphone stream config.
chunk = 1024  # CHUNKS of bytes to read each time from mic
sample_format = pyaudio.paInt16
channels = 1
fs = 16000
THRESHOLD = 1500  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

SILENCE_LIMIT = 3  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.

PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.
wants = ["一杯", "一個", "想要吃", "想要喝", "想要", "想吃", "想喝", "要", "吃"]

class listener():

	def __init__(self, language = "zh-TW"):
		self.language = language

	def record_audio(self, num_phrases = -1):
		p = pyaudio.PyAudio()

		stream = p.open(format=sample_format,
						channels = channels,
						rate = fs,
						frames_per_buffer = chunk,
						input = True)

		print("*Listening...")
		audio2send = []
		cur_data = ''
		rel = fs/chunk
		slid_win = deque(maxlen = int(SILENCE_LIMIT*rel))
		#prepend audio from 0.5 seconds before noise was detected
		prev_audio = deque(maxlen = int(PREV_AUDIO*rel))
		started = False
		n = num_phrases
		response = []

		while (num_phrases == -1 or n > 0):
			cur_data = stream.read(chunk)
			slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
	    #print slid_win[-1]
			if(sum([x > THRESHOLD for x in slid_win]) > 0):
				if(not started):
					#print("Starting record of phrase")
					started = True
				audio2send.append(cur_data)
			elif (started is True):
				# print("Finished")
				# The limit was reached, finish capture and deliver.
				filename = self.save_speech(list(prev_audio) + audio2send, p)
				started = False
				slid_win = deque(maxlen=int(SILENCE_LIMIT * rel))
				prev_audio = deque(maxlen=int(0.5 * rel))
				audio2send = []
				n -= 1
				print("* Done recording")
				break
			else:
				prev_audio.append(cur_data)

		# Stop and close the stream 
		stream.stop_stream()
		stream.close()
		# Terminate the PortAudio interface
		p.terminate()
		# print('Finished recording')
		return

	def save_speech(self, data, p):

		data = b''.join(data)
		wf = wave.open(audio_filename, 'wb')
		wf.setnchannels(channels)
		wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
		wf.setframerate(fs)  # TODO make this value a function parameter?
		wf.writeframes(data)
		wf.close()
		return audio_filename

	def recognize(self):
		r = sr.Recognizer()
		say_something_yet = True

		with sr.Microphone() as source:
			# while True:
			# 	if input("[prepare to start] Type 's' and Enter:\t") == 's':
			# 		print("start recording")
			# 		break

			while(say_something_yet):

				#print("Please ordering Food")

				self.record_audio()
				harvard = sr.AudioFile(audio_filename)
				with harvard as source:
					audio = r.record(source)

				try:
					#print(speech_count, "\tPlease Speak Anything :")
					#audio = r.listen(source, timeout=5.0)
					#print("Stop listening!")
					text = r.recognize_google(audio, language = self.language)
					#text = r.recognize(audio)
					#print("You said : {}".format(text))
					say_something_yet = False
				except sr.RequestError as e:
					say_something_yet = True
					print("No response from Google service: {0}.".format(e))
					text = '我想吃義大利麵'
				except:
					say_something_yet = True
					print("Sorry could not recognize what you said")

				say_something_yet = False

		return text

	def textParsing(self, text):

		analyzer = ChineseAnalyzer()
		result = analyzer.parse(text, traditional = True)
		return result.tokens()

	def get_reply(self):

		sentence = self.recognize()
		analyzer = ChineseAnalyzer()
		result = analyzer.parse(sentence, traditional = True)

		return result.tokens()

	def split_(self, text):
		final = ""
		for want in wants:
			food = text.split(want)
			if len(food) != 1:
				final = food[len(food)-1]
				break
			else:
				final = text
		return final


	def find_food_to_foodpanda(self):
		food = self.recognize()

		parsing = self.textParsing(food)
		print(parsing)
		food_text = False
		finding_dish = False
		food_send2panda = ""
		for i in wants:
			for j in parsing:
				if food_text:
					food_send2panda += j
				if i == j:
					food_text = True
			if food_text:
				break
		
		food_send2panda = self.split_(food_send2panda)
		return food_send2panda
	

# listen = listener()
# food = listen.find_food_to_foodpanda()
# print(food)



