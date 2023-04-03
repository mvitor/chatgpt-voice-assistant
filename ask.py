import subprocess
import speech_recognition as sr
import configparser


# create a configparser instance and read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# get the language and keywords from the config file
language = config.get('speech_recognition', 'language')
keywords = config.get('speech_recognition', 'keywords').split(',')


# a recognizer instance
r = sr.Recognizer()

# create a microphone instance
mic = sr.Microphone()


# define the callback function
def callback(recognizer, audio):
    try:
        # recognize speech using Google Speech Recognition and return all possible recognition results
        possible_results = recognizer.recognize_google(audio, language=language,show_all=True)
        print(f"Possible Results: {possible_results}")
        
        if len(possible_results) > 0:
            # check if the keyword is present in the possible recognition results
            keyword = 'Olá Chat'
            for keyword in keywords:
                if any(keyword.lower() in result['transcript'].lower() for result in possible_results['alternative']):
                    print(f"Keyword '{keyword}' detected!")
                    # Using separate script because in macos runAndWait is blocking the thread even with Threads
                    greet_msg = config.get('speech_recognition', 'greet_msg')
                    subprocess.call(["python", "pytts.py", greet_msg])
                    

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# start listening in the background
stop_listening = r.listen_in_background(mic, callback)

# keep the program running
while True:
    pass
