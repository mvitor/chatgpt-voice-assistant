import subprocess
import speech_recognition as sr
import configparser
import time
import json, openai, config, subprocess, argparse, os
from silence_detect import record_on_detect
import threading
from typing import Any, List, Dict

# create a configparser instance and read the config file
config = configparser.ConfigParser()
config.read("config.ini")

# get the language and keywords from the config file
language = config.get("speech_recognition", "language")
keywords = config.get("speech_recognition", "keywords").split(",")

openai.api_key = config.get("openai_api", "apy_key")

parser = argparse.ArgumentParser()
parser.add_argument(
    "role",
    help="Role name",
    nargs="?",
    default="Baba",
    const="Baba",
    type=str,
)
args = parser.parse_args()

# a recognizer instance
r = sr.Recognizer()

# create a microphone instance
mic = sr.Microphone()

# define the callback function
def callback(recognizer, audio):
    try:
        # recognize speech using Google Speech Recognition and return all possible recognition results
        possible_results = recognizer.recognize_google(
            audio, language=language, show_all=True
        )
        print(f"Possible Results: {possible_results}")

        if len(possible_results) > 0:
            # check if the keyword is present in the possible recognition results
            for keyword in keywords:
                if any(
                    keyword.lower() in result["transcript"].lower()
                    for result in possible_results["alternative"]
                ):
                    print(f"Keyword '{keyword}' detected!")
                    # Using separate script because in macos runAndWait is blocking the thread even with Threads
                    time.sleep(1)
                    bot_talk()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")



def get_role() -> List[Dict[str, str]]:
    messages: List[Dict[str, str]] = []
    with open("roles.json", "r") as f:
        data = json.load(f)
        for role in data:
            if role["name"].lower() == args.role.lower():
                messages = [role]
    print (messages)
    return messages
                

def bot_talk(messages: List[Dict[str, str]]) -> None:
    audio_filename = "teste.wav"
    record_on_detect("teste")
    print(f"Recorded file saved as {audio_filename}")

    audio_file = open(audio_filename, "rb")
    
    if not messages:
        print(f"Provided role {args.role} did not match any entry in roles file")
        return
    if not os.path.getsize(audio_filename) > 150000:
        print(f"{audio_filename} is not larger than 150KB")
        return 
        
    print("Querying Transcribe API")
    #transcript = openai.Audio.transcribe("whisper-1", audio_file, language='en')
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language='pt')

    try:
        os.remove(audio_filename)
    except PermissionError as e:
        print(f"Unable to delete file {audio_filename}: {e}")

    print(f"\nTranscribe API response: {transcript['text']}")
    messages.append({"role": "user", "content": transcript["text"]})
    print(f"Pergunta:\n{transcript['text']}")
    
    print("Querying ChatCompletion API")
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    system_message = response["choices"][0]["message"]
    messages.append(system_message)
    
    print(f"messages: {messages}")
    print(f"Resposta:\n{system_message['content']}")
    print(f"Chatcompletion Response: {system_message['content']}")
    
    call_pytts(message=system_message['content'])


def call_pytts(message:str):
   
    subprocess.call(["python", "pytts.py", message])

def greet_msg(role_name: str):
    greeting_msg = config.get("speech_recognition", "greeting_msg")
    # create a new thread
    greeting_msg = f"Sou uma {role_name}, {greeting_msg}" 
    t = threading.Thread(target=call_pytts(message=greeting_msg))
    # start the thread
    t.start()

# start listening in the background
#stop_listening = r.listen_in_background(mic, callback)
print(args)
messages = get_role()
greet_msg(role_name=messages[0].get('name'))

print ()
# keep the program running
while True:
   bot_talk(messages=messages)
