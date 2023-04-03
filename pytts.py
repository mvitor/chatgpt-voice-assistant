import pyttsx3
import sys

def change_voice(engine, language, gender="VoiceGenderMale"):
    for voice in engine.getProperty("voices"):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty("voice", voice.id)
            return True


engine = pyttsx3.init()

change_voice(engine, "pt_BR", "VoiceGenderFemale")


engine.say(str(sys.argv[1]))
engine.runAndWait()