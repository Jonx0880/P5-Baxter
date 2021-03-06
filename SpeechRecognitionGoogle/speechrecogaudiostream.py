from __future__ import division
import re
import sys
import os
from google.cloud import speech
import pyaudio
from six.moves import queue
import TCP_client


'''
You have to sign up at google API to use this script. Lots of great tutorials available online. You need to make a json file with your private token. 
DO NOT PUSH THAT TOKEN TO GITHUB.
'''
#Open Windows Power Shell and write below
#then run this python script (In my, Victors, case:)
 #$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\victo\Desktop\P5-Baxter\SpeechRecognitionGoogle\baxtervoice-ed6f37715517.json"

# Audio recording parameters (Standard google stuff, from tutorial)
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

#This is just how the API is used
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio() #Setting pyaudio.PyAudio as interface
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self
    #Close function
    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break
            yield b"".join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if not result.is_final:
            #If sentence is not done, it will still write words it hears real time
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            #Prints the entire finished sentence
            print(transcript + overwrite_chars)
            #Checks if "hello baxter" is in sentence. Runs tcp_client if it is
            if ("hello baxter" in transcript.lower()):
                print(transcript)
                TCP_client.sendData(transcript)
            elif ("switch" in transcript.lower() and "text" in transcript.lower()):
                #Checks if it is asked to switch to text instead, and will run the function called textBased
                textBased()
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0
def textBased():
    #Print a lot of blank lines, and a welcome messege
    print("\n\n\n\n\n\n\n\n\n\nHello I am Baxter. \n")
    while True:
        #Will forever loop, and wait for a messege from user. Will send this messege to TCP_client, unless it is asked to switch to voice. In that case it will stop the loop.
        transcript = input("What do you want me to do? \n")
        if ("switch" in transcript and "voice" in transcript):
            return False
        TCP_client.sendData(transcript)

def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = "en-US"  # a BCP-47 language tag
    #Setting up client and configurations
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
    )
    #Enables streaming and interim(temporary) results, like mentioned earlier.
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )
    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)



if __name__ == "__main__":
    main()
