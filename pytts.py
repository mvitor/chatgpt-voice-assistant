import pyttsx3
import sys

def change_voice(engine, language, gender="VoiceGenderFemale"):
    for voice in engine.getProperty("voices"):
        print (voice.gender)
        if language in voice.languages and gender == voice.gender:
            engine.setProperty("voice", voice.id)
            return True


engine = pyttsx3.init()
# Get the Portuguese voice
voices = engine.getProperty('voices')

print (voices)
# Set the Portuguese voice
#Windows
#engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_ptBR_MariaM")
change_voice(engine, "pt_BR", "VoiceGenderFemale")

engine.say(str(sys.argv[1]))
engine.runAndWait()